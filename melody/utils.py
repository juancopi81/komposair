import json
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
import music21 as m21

SEQUENCE_LENGTH = 64
MAPPING_PATHS = ["mapping.json", "mapping_europa.json", "mapping_europa.json"]
MODELS = ["lstm-folk-1.h5", "lstm-folk-2.h5", "lstm-folk-3.h5"]


class MelodyGenerator:
    """
    Class to generate melodies based on h5 model

    ...

    Attributes:
    ----------
    model_name : str
        string - name of the model
    model : h5 model
        h5 model to generate a melody

    Methods:
    -------
    generate_melody(seed, num_steps, max_sequence_length, temperature)
    generates melody based on the seed usind the given model
    """

    def __init__(self, model_number):

        DIRNAME = os.path.dirname(__file__)

        self.model_path = os.path.join(DIRNAME, MODELS[model_number])

        self.model = load_model(self.model_path)

        mapping_path = os.path.join(DIRNAME, MAPPING_PATHS[model_number])

        with open(mapping_path, "r") as fp:
            self._mappings = json.load(fp)

        self._start_symbols = ["/"] * SEQUENCE_LENGTH

    def generate_melody(self, seed, num_steps, max_sequence_length, temperature):

        # create seed with start symbols
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        # Map seed to integers
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):
            # Limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]

            # One-hot encode the seed
            onehot_seed = to_categorical(seed, num_classes=len(self._mappings))
            # (New dim, max_sequence_length, number of symbols in the vocab)
            # Add third dimension -> for keras expect multiple samples
            onehot_seed = onehot_seed[np.newaxis, ...]

            # Make a prediction
            probabilities = self.model.predict(onehot_seed)[0]

            # [0.1, 0.2, 0.1, 0.6] add to 1
            output_int = self._sample_with_temperature(probabilities, temperature)

            # updaate the seed
            seed.append(output_int)

            # Map int to our encoding
            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            # Check whether we are at end of melody
            if output_symbol == "/":
                break
            # Update the meelody
            else:
                melody.append(output_symbol)

        return melody

    def _sample_with_temperature(self, probabilities, temperature):
        # Temperature value -> infinite, random picking one of the probabilities
        # Temperature value -> 0, higher gets 1 other 0
        # Temperature value -> 1, nothing changes in probabilities

        predictions = np.log(probabilities.clip(min=0.00000000001)) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))    # [0, 1, 2, 3]
        index = np.random.choice(choices, p=probabilities)

        return index

    def save_melody(self, melody, step_duration=0.25, format="midi", file_name="mel1.mid", bpm=90):

        # Create a music21 stream
        stream = m21.stream.Stream()

        mm = m21.tempo.MetronomeMark(number=bpm)
        stream.append(mm)

        # Parse all the symbols in the melody and create note/rest objects
        # 60 _ _ _ r _ 62 _
        start_symbol = None
        step_counter = 1

        for i, symbol in enumerate(melody):

            # Handle case we have note/rest
            if symbol != "_" or i + 1 == len(melody):

                # Ensure we are dealing with note/rest beyond first one
                if start_symbol is not None:

                    # Calculate duration
                    quarter_length_duration = step_duration * step_counter    # 0.25 * 4

                    # Handle rest
                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength=quarter_length_duration)

                    # Handle note
                    else:
                        m21_event = m21.note.Note(int(start_symbol), quarterLength=quarter_length_duration)

                    stream.append(m21_event)

                    # Reset step counter
                    step_counter = 1

                start_symbol = symbol

            # Handle case we have prolongation sign -> "_"
            else:
                step_counter += 1

        # Write the m21 stream to midi
        midi = stream.write(format)

        # Return the midi file object
        return midi


def parse_motif(motif, time_step=0.25, parser="series"):
    """ Parses the given notes to a string used by the model or by magenta

    Parameters
    ----------
    motif : str
        The notes given in string format
    time_step : float
        Based duration, default 16th note
    parser : string
        String to decide to parse the notes so
        they can be feed to the model or to magenta

    Returns
    -------
    string/dict
        a string (time series ) or dict that can be used to feed the model
        or magenta
    """

    # Initialize and empty list and total duration to zero
    encoded_motif = []
    total_duration = 0

    for notes in motif:
        # Handle notes
        if "r" not in notes["duration"]:
            # Convert pitch to its midi number
            symbol = m21.pitch.Pitch(notes['note']).midi

        # Handle rests
        else:
            symbol = "r"

        # Convert the note/rest into time series notation

        # Remove "r" and "." from the duration
        duration = float(notes["duration"].replace(".", "").replace("r", ""))

        # Calculate duration in quarter length
        duration = 4.0 / duration

        total_duration += duration

        # Update duration if note is dotted
        if (notes['dot']):
            duration += duration / 2.0

        # Calculate number of sixteenth steps
        steps = int(duration / time_step)

        # Create "_" based on number of steps
        for step in range(steps):
            if step == 0:
                encoded_motif.append(symbol)
            else:
                encoded_motif.append("_")

    # Cast encoded_motif to string
    encoded_motif = " ".join(map(str, encoded_motif))

    return encoded_motif, total_duration
