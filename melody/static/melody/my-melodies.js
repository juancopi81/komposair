// Define range of melodies the retriev
let counter = 0;
let quantity = 4; 

// Variable of the melody template 
let melodyTemplate;

// Colors
let colorVote = '#ff0000';
let colorNoVote = '#000000';

let personalMelodies = true;

// When DOM loads, render melodies
document.addEventListener('DOMContentLoaded', () => {

	if(document.URL.includes('my_melodies')) {
		personalMelodies = true;
	} else {
		personalMelodies = false;
		document.getElementById('saved-melodies').setAttribute('style', 'background-color:#dae0e5!important');
	}

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
	const filter = document.getElementById('id_m_filter').value;
	const order = document.getElementById('id_m_order').value;

	// Get new melodies and add them
	fetch(`/get_melodies?start=${start}&end=${end}&personal=${personalMelodies}&filter=${filter}&order=${order}`)
	.then(response => response.json())
	.then(data => {
		data.melodies.forEach(melody => add_melody(melody, personalMelodies));
	});
};