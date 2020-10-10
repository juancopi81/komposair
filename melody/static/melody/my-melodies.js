// Define range of melodies the retriev
let counter = 0;
let quantity = 2; 

// Variable of the melody template 
let melodyTemplate;

// When DOM loads, render melodies
document.addEventListener('DOMContentLoaded', () => {

	// Template of melodies
	melodyTemplate = Handlebars.compile(document.querySelector('#melody-template').innerHTML);

	load();
});

// If scroll to the bottom load next melodies
window.onscroll = () => {
	if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
		load();
	};
};

// Load next set of melodies
function load() {

	// Set start and end melodies number and update counter
	const start = counter;
	const end = counter + quantity;
	counter = end + 1;

	// Get new melodies and add them
	fetch(`/get_melodies?start=${start}&end=${end}`)
	.then(response => response.json())
	.then(data => {
		for (let melody of data.melodies) {
			add_melody(melody);
		};
	});
};

// Add a new melody with given information to DOM
function add_melody(melody) {

	// CHECK HOW YO FACTOR OUT SINCE IT IS ALSO USED IN HOME
	let notes = melody.notes;
	let bpm = melody.bpm;
	let model = melody.aimodel;

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
	let	melodyContent = melodyTemplate({'id': melody.id, 'src': mURL, 'model': model});

	document.querySelector('#melodies').innerHTML += melodyContent;

	// Add scoreboard
	document.getElementById('scoreboard' + melody.id).classList.remove('display-none');
	let visualizer = document.querySelector('.padding-1');
	visualizer.classList.remove('padding-1');
	visualizer.classList.add('padding-0');

}