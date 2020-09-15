from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import parse_motif, MelodyGenerator, SEQUENCE_LENGTH
import json

def home(request):
	return render(request, "melody/home.html")

# Generate the melody based on the seed
@require_http_methods(["POST"])
def generate(request):
	
	# See if method was post
	if request.method == "POST":

		# Retrive seed
		seed = json.loads(request.POST.get("motif"))

		# Sanity check
		if not seed:
			return JsonResponse({"succes": False}, status=400)

		encoded_seed = parse_motif(seed)

		# Create a melody generator
		mg = MelodyGenerator()

		melody = mg.generate_melody(encoded_seed, 50, SEQUENCE_LENGTH, 0.3)

		print(melody)

		mg.save_melody(melody)

		# Return the seed
		return JsonResponse({"seed": seed}, status=200)


