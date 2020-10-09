// Define range of melodies the retriev
let counter = 1;
let quantity = 3; 

// When DOM loads, render melodies
document.addEventListener('DOMContentLoaded', load);

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
	const end = counter + quantity - 1;
	counter = end + 1;

	// Get new melodies and add them
	fetch('/get_melodies?start=${start}&end=${end}')
	.then(response => response.json())
	.then(data => {
		data.melodies.foEach(add_melody);
		console.log(data);
		console.log(data.melodies)
	})

}