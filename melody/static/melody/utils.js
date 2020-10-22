// Salamander Piano
const salamanderSampler = new Tone.Sampler({
	urls: {
		A0: "A0.mp3",
		C1: "C1.mp3",
		"D#1": "Ds1.mp3",
		"F#1": "Fs1.mp3",
		A1: "A1.mp3",
		C2: "C2.mp3",
		"D#2": "Ds2.mp3",
		"F#2": "Fs2.mp3",
		A2: "A2.mp3",
		C3: "C3.mp3",
		"D#3": "Ds3.mp3",
		"F#3": "Fs3.mp3",
		A3: "A3.mp3",
		C4: "C4.mp3",
		"D#4": "Ds4.mp3",
		"F#4": "Fs4.mp3",
		A4: "A4.mp3",
		C5: "C5.mp3",
		"D#5": "Ds5.mp3",
		"F#5": "Fs5.mp3",
		A5: "A5.mp3",
		C6: "C6.mp3",
		"D#6": "Ds6.mp3",
		"F#6": "Fs6.mp3",
		A6: "A6.mp3",
		C7: "C7.mp3",
		"D#7": "Ds7.mp3",
		"F#7": "Fs7.mp3",
		A7: "A7.mp3",
		C8: "C8.mp3"
	},
	release: 1,
	baseUrl: "https://tonejs.github.io/audio/salamander/"
}).toDestination();


// Use Tone Transport to schedule the notes
class TonePlayer {

	// Use the salamander sampler
	constructor() {
		this.sampler = salamanderSampler;
	}

	/**
     * Use Tone.js Transport to play a series of notes encoded as strings
     * @param notes
     */
     play(notes, bpm) {
     	const sampler = this.sampler;

     	// Reset from the Transport and set bpm
     	Tone.Transport.bpm.value = bpm;
     	Tone.Transport.stop();
     	Tone.Transport.position = 0;
     	Tone.Transport.cancel();

     	// Schedule the notes, time represents absolute time in seconds
     	Tone.Transport.schedule((time) => {

     		// Relative time of note with respect to start of measure, in seconds
     		let relativeTime = 0;

     		// Loop over the notes
     		for (const note of notes) {

     			// Remove dot and rest
     			let noteDuration = note.duration.replace('.', '');
     			noteDuration = noteDuration.replace('r', '');

     			// Time of the note, remove 'r' if rest
     			let duration = noteDuration + 'n';

     			if (note.dot) {
     				duration = duration + '.';
     			}

     			// Only schedule if it is not a rest
     			if (!note.duration.includes('r')) {

     				// Schedule the note to be played in Transport timeline
     				// after previous notes have been played (-> relative time)
     				sampler.triggerAttackRelease(note.note, duration, time + relativeTime)
     			}

     			// Update relative time
     			relativeTime += Tone.Time(duration).toSeconds();
     		}
     	});

     	Tone.Transport.start();
     }
}

// Colors
let colorVote = '#ff0000';
let colorNoVote = '#000000';

async function saveMelody(melodyUrl, bpm, model, melodyId = -1) {
	
	// Get the notes out of the url
	let noteSequence = await core.urlToNoteSequence(melodyUrl);
	let notes = noteSequence.notes;

	// Add the data to send with the request
	const data = new FormData();

	// Add bpm model and notes 
	data.append('bpm', bpm);
	data.append('model', model);
	data.append('notes', JSON.stringify(notes));
	data.append('melody_id', melodyId);

	// Get the token
	const csrftoken = getCookie('csrftoken');

	// Send request to save melody
	fetch('/save_melody', {
		method: 'POST',
		body: data,
		headers: { "X-CSRFToken": csrftoken },
	})
	.then(response => response.json())
	.then(data => {
		alertDialog(data.message)
	})
	.catch(error => console.log('Error: ', error));	
}

// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function alertDialog(message) {
	$('#modal-alert').modal('show');
	document.getElementById('modal-text').innerHTML = message;
}

function delete_melody(melodyID) {
	fetch(`/delete_melody?melody_id=${melodyID}`)
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			melodyDiv = document.getElementById('melody-render' + melodyID);
			melodyDiv.style.animationPlayState = 'running';
			melodyDiv.addEventListener('animationend', () => {
				melodyDiv.remove();
			});
		} else {
			alertDialog(data.message);
		};
	});
};

function vote_melody(melodyID, vote) {
	fetch(`/add_vote?melody_id=${melodyID}&vote=${vote}`)
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			document.getElementById('score-number' + melodyID).innerHTML = data.score;
			update_votes_view(melodyID, data.user_score)
		}
		
		alertDialog(data.message);
	});
};

function update_votes_view(melodyID, userScore) {

	if (userScore === 1) {
		document.getElementById('upvote' + melodyID).style.color = colorVote;
		document.getElementById('downvote' + melodyID).style.color = colorNoVote;
	}
	if (userScore === 0) {
		document.getElementById('upvote' + melodyID).style.color = colorNoVote;
		document.getElementById('downvote' + melodyID).style.color = colorNoVote;
	}
	if (userScore === -1) {
		document.getElementById('upvote' + melodyID).style.color = colorNoVote;
		document.getElementById('downvote' + melodyID).style.color = colorVote;
	}

}

// Add a new melody with given information to DOM
function add_melody(melody, isPersonal) {

	// CHECK HOW YO FACTOR OUT SINCE IT IS ALSO USED IN HOME
	let notes = melody.notes;
	let bpm = melody.bpm;
	let model = melody.aimodel;
	let score = melody.score;
	let date = melody.date_created;
	let convertDate = new Date(date);

	// Options for formatter date
	let optionsDate = { year: 'numeric', month: 'long', day: 'numeric'};

	let parseDate = convertDate.toLocaleString('en-US', optionsDate);


	let magentaSequence = {notes,
		quantizationInfo: {stepsPerQuarter: 4},
		tempos: [{time: 0, qpm: bpm}],
		totalQuantizedSteps: 64
	};

	let quantizedSequence = core.sequences.quantizeNoteSequence(magentaSequence, 4);

	// Create midi file out of magenta note sequence
	const midi = core.sequenceProtoToMidi(quantizedSequence);

	// Convert byte array to file
	const mFile = new Blob([midi], { type: 'audio/midi' });

	// Get url of the file
	const mURL = URL.createObjectURL(mFile);

	// Add midi element to the dom
	let	melodyContent = melodyTemplate({'id': melody.id, 'src': mURL, 'model': model, 'bpm': bpm, 'score': score, 'date': parseDate});

	var div = document.getElementById('melodies');

	div.insertAdjacentHTML('beforeend', melodyContent);

	// Add scoreboard
	document.getElementById('scoreboard' + melody.id).classList.remove('display-none');
	let visualizer = document.querySelector('.padding-1');
	visualizer.classList.remove('padding-1');
	visualizer.classList.add('padding-0');

	// Update votes view
	if(melody.user_score) {
		update_votes_view(melody.id, melody.user_score);
	};

	// Remove save icon add delete if is in my_melodies
	if (isPersonal) {
		document.getElementById('save-melody' + melody.id).parentNode.classList.add('display-none');
		document.getElementById('delete-melody' + melody.id).parentNode.classList.remove('display-none');
	} else {
		document.getElementById('save-melody' + melody.id).addEventListener('click', () => {
			saveMelody(mURL, bpm, model, melody.id);
		});
	}
	
	// Add bpm and info
	document.getElementById('bpm-render' + melody.id).classList.remove('display-none');
	document.getElementById('info-melody' + melody.id).classList.remove('display-none');

	// Add event listener to remove melodies from this user
	document.getElementById('delete-melody' + melody.id).addEventListener('click', () => {
		delete_melody(melody.id);
	});

	// Add event listener to vote melodies
	document.getElementById('upvote' + melody.id).addEventListener('click', () => {
		vote_melody(melody.id, 1);
	});
	document.getElementById('downvote' + melody.id).addEventListener('click', () => {
		vote_melody(melody.id, -1);
	});
}