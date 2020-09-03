// Variable to keep track of input notes
let renderNotes;

// Check current duration of the motiv
let totalCurrentDuration = 0;

// Vexflow variables
const VF = Vex.Flow;

document.addEventListener('DOMContentLoaded', () => {

	// Start a new staff
	eraseStaff();

	// Button to erase notes
	document.getElementById('input-eraser').addEventListener('click', eraseStaff);

	// Disable durations based on selected by user
	document.getElementById('input-duration').addEventListener('change', function(obj) {
		let inputPitch = document.getElementById('input-pitch');
		let inputAccidental = document.getElementById('input-accidental');
		let inputOctave = document.getElementById('input-octave');
		let inputDot = document.getElementById('input-dot');

		inputPitch.disabled = (this.value.includes('r'));
		inputAccidental.disabled = (this.value.includes('r'));
		inputOctave.disabled = (this.value.includes('r'));
		inputDot.disabled = (this.value.includes('16') || this.value.includes('1'));
	})

	// Add the notes entered by the user
	let notes = [];

	document.querySelector('#input-form').onsubmit = (e) => {

		// Prevent the form to be sent
		e.preventDefault();

		// Erase any alert comments
		document.getElementById('input-info').innerHTML = '';

		// Retrieve information sent by the user
		let inputDuration = document.getElementById('input-duration').value;
		let inputPitch = document.getElementById('input-pitch').value;
		let inputAccidental = document.getElementById('input-accidental').value;
		let inputOctave = document.getElementById('input-octave').value;

		let inputNote = inputPitch + inputAccidental + inputOctave;

		let isDotted = false;

		if (document.getElementById('input-dot').checked == true) {
			isDotted = true;
			inputDuration = inputDuration + '.';
		}

		// Clear the form
		let elements = document.querySelector('#input-form');

		for (element of elements) {
			element.value = '';
			if (element.disabled) {
				element.disabled = false;
			}
		};

		document.getElementById('input-dot').checked = false;

		// Check if new note would exceed allowed duration
		let currentNoteDuration = inputDuration.replace('r', '');
		let currentNoteDurationInSixteenth = (16 / parseInt(currentNoteDuration));

		if (isDotted) {
			currentNoteDurationInSixteenth += currentNoteDurationInSixteenth / 2;
		}

		if (totalCurrentDuration + currentNoteDurationInSixteenth > 16) {
			document.getElementById('input-info').innerHTML = "Your motif can't be longer than a 4/4 bar";
			return false;
		}

		// Add note to the array
		notes = [...notes, {'duration': inputDuration, 'note': inputNote, 'dot': isDotted}]

		// Calculate how many rests should be added to complete the bar
		restsString = restsToComplete(notes);

		// Create string for the notes voice
		let notesString = '';

		// Reset total current duration
		totalCurrentDuration = 0;

		// Create each value of the array as a string
		for (note of notes) {

			// Initialize empty string for each note
			let noteString = '';
			
			// Check if is silence
			if (note.duration.includes('r')) {
				
				// Remove r if is a rest
				let noteDuration = note.duration.replace('r', '');

				// Check if silence is dotted
				if (note.dot) {
					
					// Remove dot and write it in right position
					noteString = noteDuration.replace('.', '');
					noteString = 'B4/' + noteString +'/r.,'

				} else {

					// Create string of the silence
					noteString = 'B4/' + noteDuration + '/r,';
				}
			} else {

				// If not silence
				noteString = note.note + '/' + note.duration + ',';
				noteDuration = note.duration;
			}

			// Update the notes voice
			notesString += noteString;

			// Calculate the duration of the notes in 16th
			let noteDurationInSixteenth = (16 / parseInt(noteDuration));

			// If dotted increase value respectively
			if (note.dot) {
				noteDurationInSixteenth += noteDurationInSixteenth / 2;
			}

			// Update total duration of motive
			totalCurrentDuration += noteDurationInSixteenth;
		}

		renderNotes = notesString + restsString;

		// Remove staff to paint it again
		const staff = document.getElementById('staff-input');

		while (staff.hasChildNodes()) {
		    staff.removeChild(staff.lastChild);
		}

		// Paint new notes
		var vf = new VF.Factory({renderer: {elementId: 'staff-input'}});
		var score = vf.EasyScore();
		var system = vf.System();

		system.addStave({
		  voices: [score.voice(score.notes(renderNotes))]
		}).addClef('treble').addTimeSignature('4/4');

		vf.draw();

		// If motiv equals the allowed duration, disable more input
		if (totalCurrentDuration === 16) {
			document.getElementById('input-submit').disabled = true;
			document.getElementById('input-info').innerHTML = "You can't add more notes to your motif";
		}

	};

});

function restsToComplete(notes) {

	// Intialize rests to the total 16 notes
	let restsDuration = 16;

	// Initialize the duration of notes to zero
	let notesDuration = 0;

	for (note of notes) {

		// Remove r if is a rest
		noteDuration = note.duration.replace('r', '');

		// Calculate the duration of the notes in 16th
		let noteDurationInSixteenth = (16 / parseInt(noteDuration));

		// If dotted increase value respectively
		if (note.dot) {
			noteDurationInSixteenth += noteDurationInSixteenth / 2;
		}

		// Update total duration of the notes
		notesDuration += noteDurationInSixteenth;
	}

	// Calculate what is left to use in rests
	restsDuration -= notesDuration;

	let quarterRests = Math.floor(restsDuration / 4);
	let sixteenthRests = restsDuration % 4;

	// Stringify the values of the rests
	let quarterRestsString = 'B4/4/r,'.repeat(quarterRests);
	let sixteenthRestsString = 'B4/16/r,'.repeat(sixteenthRests);

	return sixteenthRestsString + quarterRestsString; 
}

function eraseStaff() {

	// Remove staff to paint it again
	const staff = document.getElementById('staff-input');

	while (staff.hasChildNodes()) {
	    staff.removeChild(staff.lastChild);
	}

	// Create an SVG renderer and attach it to the DIV element named 'staff-input'.
	var vf = new VF.Factory({renderer: {elementId: 'staff-input'}});
	var score = vf.EasyScore();
	var system = vf.System();

	renderNotes = 'B4/4/r,B4/4/r,B4/4/r,B4/4/r,';

	system.addStave({
	  voices: [score.voice(score.notes(renderNotes))]
	}).addClef('treble').addTimeSignature('4/4');

	vf.draw();

	// Enable again the input of notes and clean the info message
	if (document.getElementById('input-submit').disabled) {
		document.getElementById('input-submit').disabled = false;
	}

	document.getElementById('input-info').innerHTML = '';
	
}