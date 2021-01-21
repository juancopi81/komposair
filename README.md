[![Actions Status](https://github.com/juancopi81/komposair/workflows/Komposair%20CI-CD/badge.svg)](https://github.com/juancopi81/komposair/actions)

# Komposair

*Komposair was selected by TensorFlow for the [TensorFlow Community Spotlight program](https://blog.tensorflow.org/2020/11/tensorflow-community-spotlight-program-update.html) on December 2020*

Komposair is a web app that lets musician create melodies using AI. Visit Komposar at https://www.komposair.com/

  - Create melodies based on your motif
  - Explore other melodies created by the community
  - Save your melodies, download them as midi files, vote for your favorites and comment them

# In the browser

  - Komposair needs no installation you can use it right in your browser
  - We use Tone.js and Magenta so you can hear the melodies in the browser or export them as a midi file if you prefer


You can also:
  - Upload your model (to be done, for the moment feel free to send us and email with your model)
  - Find a random melody if you feel lucky

The models to create melodies will be improved, the melodies are generated using motifs of the users. The motif is one building block for melody compositions. Find more information about [motifs](https://en.wikipedia.org/wiki/Motif_(music))

Arnold Schönberg defines a motif as:

> a unit which contains one or more 
> features of interval and rhythm [whose] presence 
> is maintained in constant use throughout a piece

### Tech

Komposair uses several open source projects to work properly:

* [Django](https://www.djangoproject.com/) - A high-level Python Web framework that encourages rapid development and clean, pragmatic design
* [Start Bootstrap - Simple Sidebar](https://github.com/StartBootstrap/startbootstrap-simple-sidebar/) - Simple Sidebar is an off canvas sidebar navigation template for Bootstrap created by Start Bootstrap.
* [Vexflow](https://www.vexflow.com/) - online music notation rendering API. It is written completely in JavaScript and runs right in the browser. VexFlow supports HTML5 Canvas and SVG.
* [Twitter Bootstrap] - Great UI boilerplate for modern web apps
* [Magenta.js](https://github.com/magenta/magenta-js) - a collection of TypeScript libraries for doing inference with pre-trained Magenta models
* [Tensorflow](https://www.tensorflow.org/) - Open source library to help you develop and train ML models
* [Music21](http://web.mit.edu/music21/) - A toolkit for computer-aided musicology
* [Tone.js](https://tonejs.github.io/) - a Web Audio framework for creating interactive music in the browser
* [Django Markdownify](https://pypi.org/project/django-markdownify/) - A Django Markdown filter
* [Handlebars.js](https://handlebarsjs.com/) - Minimal templating on steroids

And of course Komposair itself is open source with a [public repository](https://github.com/juancopi81/komposair)
 on GitHub.

### CS50's Web Programming with Python and JavaScript

Komposair is my final project for the course [CS50's Web Programming with Python and Javascript](https://www.edx.org/es/course/cs50s-web-programming-with-python-and-javascript). I tried to use many of the concepts taught by Prof. Bryan Yu. These are the files insides Komposair:
  * Komposair: Root project: settings, urls, init...
  * Media: Media files of the project
  * Melody: This is the main app of Komposair, with the static files, templates views
  * Users: This is the app that handles user registration, login, logout

 The project is mobile responsive and uses Javascript and Django with more than one model. I think that it satisfies the requirements of the course.

### Support

Want to contribute? Great!

Please feel free to [contact me](https://twitter.com/juancopi81) if you want to send a model or contribute in any other way



### To-dos

 - Write more models train on different genres
 - Add more options, such as, other time signatures, 
 - Add more features in the melody detail view: Suggested lyrics and harmonizaties using AI

License
----

MIT


**Free Software, Hell Yeah!**
