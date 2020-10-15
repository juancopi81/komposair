from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import parse_motif, MelodyGenerator, SEQUENCE_LENGTH
import json
from .models import Melody, Vote

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
			return JsonResponse({"success": False}, status=400)

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
			response = JsonResponse({"success": False}, status=400)

		return response

# Save melody selected by user
@require_http_methods(["POST"])
def save_melody(request):

	# Check method was post
	if request.method == "POST":

		# Check if user is authenticated
		if not request.user.is_authenticated:
			response = JsonResponse({"success": False, "message": "You need to be logged in order to save melodies"}, status=200)

		else:			
			# Retrive values
			notes = json.loads(request.POST.get("notes"))
			bpm = int(request.POST.get("bpm"))
			model = request.POST.get("model")
			melody_id = int(request.POST.get("melody_id"))
			user = request.user

			# Check if melody already in database and in users melodies
			if (melody_id != -1):

				if user.melodies.filter(pk=melody_id).exists():
					return JsonResponse({"success": False, "message": "This melody is already in your saved melodies"})

			melody = Melody(notes=notes, bpm=bpm, aimodel=model)

			melody.save()

			melody.person.add(request.user)

			response = JsonResponse({"success": True, "message": "The melody was saved in your melodies"})


		return response

# Show saved melodies of the user
@login_required
def my_melodies(request):

	# Render template 
	return render(request, "melody/my_melodies.html")

def get_melodies(request):

	# Get start and end point
	start = int(request.GET.get("start") or 0)
	end = int(request.GET.get("end") or (start + 9))
	personal = json.loads(request.GET.get("personal") or False)

	print(personal)

	# Get the current user
	person = request.user

	# Get melodies of current user
	melodies = Melody.objects.all().filter(person=person).order_by('-score')[start:end+1].values()

	# Get votes of the user
	votes = Vote.objects.all().filter(person=person)

	for i, m_melody in enumerate(melodies):
		for m_vote in votes:
			if (m_vote.melody.id == m_melody['id']):
				melodies[i]['user_score'] = m_vote.user_score
				
	return  JsonResponse({"melodies": list(melodies)})

# Delete user from melody so it is not shown in their profiel
@login_required
def delete_melody(request):

	# Get the melody id and the user
	user = request.user
	melody_id = int(request.GET.get("melody_id"))

	melody = Melody.objects.get(pk=melody_id)

	try:
		melody.person.remove(user)
		response = JsonResponse({"success": True, "message": "The melody was deleted from your profile"}, status=200)
	except Exception as e:
		response = JsonResponse({"success": False, "message": "The melody was not deleted from your profile"}, status=200)
		print(e)

	return response

# Register vote of the user
def add_vote(request):

	# Check that user is logged in
	if not request.user.is_authenticated:
		response = JsonResponse({"success": False, "message": "You need to be logged in order to vote"}, status=200)

	# Get melody id and user
	user = request.user
	melody_id = int(request.GET.get("melody_id"))

	melody = Melody.objects.get(pk=melody_id)

	# Get vote of the user
	vote = int(request.GET.get("vote"))

	# Check that number is between -1 and 1
	if -1 <= vote <= 1:
		# See if user has already voted for this melody
		query_vote = Vote.objects.filter(melody = melody, person = user).first()

		# If not, insert the vote and update the score
		if not query_vote:
			
			# Add new vote
			new_vote = Vote(user_score=vote, melody=melody, person=user)
			try:
				new_vote.save()
			except Exception as e:
				raise e
				response = JsonResponse({"success": False, "message": "Something went wrong and your vote was not registered"}, status=200)
			
			# Update score
			melody.score += vote
			try:
				melody.save()
			except Exception as e:
				raise e
				response = JsonResponse({"success": False, "message": "Something went wrong and your vote was not registered"}, status=200)

			score = melody.score
			user_score = vote
			response = JsonResponse({"success": True, "message": "Your vote was registered", "score": score, "user_score": user_score}, status=200)

		else:

			# Check if vote is the same as already registered
			if query_vote.user_score == vote:
				response = JsonResponse({"success": False, "message": "You have already voted for this melody"}, status=200)
			else:
				query_vote.user_score += vote
				query_vote.save()

				melody.score += vote
				melody.save()

				score = melody.score
				user_score = query_vote.user_score

				response = JsonResponse({"success": True, "message": "Your vote was registered", "score": score, "user_score": user_score}, status=200)

	else:
		response = JsonResponse({"success": False, "message": "Something went wrong and your vote was not registered"})

	return response

# Show all melodies
def melodies(request):
	return render(request, "melody/melodies.html")