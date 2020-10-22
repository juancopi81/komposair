let melodyTemplate;

document.addEventListener('DOMContentLoaded', () => {
	
	// Get the melody ud
	let divMelodies = document.getElementById('melodies');
	let melodyId = divMelodies.dataset.melodyId;

	// Template of melodies
	melodyTemplate = Handlebars.compile(document.querySelector('#melody-template').innerHTML);

	loadOne(melodyId);
});

function loadOne(melodyId) {

	const start = melodyId;
	const end = melodyId;
	let personalMelodies = false;

	// Get new melodies and add them
	fetch(`/get_melodies?start=${start}&end=${end}&personal=${personalMelodies}`)
	.then(response => response.json())
	.then(data => {
		data.melodies.forEach(melody => add_melody(melody, personalMelodies));
		document.getElementById('info-melody' + melodyId).remove();
	});
};