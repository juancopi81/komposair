from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib import messages
from .utils import parse_motif, MelodyGenerator, SEQUENCE_LENGTH
import json
from .models import Melody

def home(request):
	return render(request, "melody/home.html")

# Generate the melody based on the seed
@require_http_methods(["POST"])
def generate(request):
	
	# See if method was post
	if request.method == "POST":

		# Retrive values
		seed = json.loads(request.POST.get("motif"))
		bpm = int(request.POST.get("bpm"))
		temperature = float(request.POST.get("temperature"))

		# Sanity check
		if not seed:
			return JsonResponse({"succes": False}, status=400)

		encoded_seed, duration = parse_motif(seed)
		
		sixteenth_duration = duration / 0.25

		# Create a melody generator
		mg = MelodyGenerator()

		melody = mg.generate_melody(encoded_seed, 64 - int(sixteenth_duration), SEQUENCE_LENGTH, temperature)

		midi = mg.save_melody(melody, bpm=bpm)

		try:
			with open(midi, 'rb') as f:
				file_data = f.read()

			response = HttpResponse(file_data, content_type="audio/midi", status=200)

		except IOError:
			response = JsonResponse({"succes": False}, status=400)

		return response

# Save melody selected by user
@require_http_methods(["POST"])
def save_melody(request):

	# Check method was post
	if request.method == "POST":

		# Check if user is authenticated
		if not request.user.is_authenticated:
			response = JsonResponse({"succes": False, "message": "You need to be logged in order to save melodies"}, status=200)

		else:			
			# Retrive values
			notes = json.loads(request.POST.get("notes"))
			bpm = int(request.POST.get("bpm"))
			model = request.POST.get("model")

			melody = Melody(notes=notes, bpm=bpm, aimodel=model)

			melody.save()

			melody.person.add(request.user)

			messages.success(request, "The melody was saved in your profile")

			response = JsonResponse({"succes": True, "message": "The melody was saved in your profile"})


		return response