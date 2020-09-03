from django.shortcuts import render

def home(request):
	context = {
		"prueba": "prueba"
	}

	return render(request, "melody/home.html", context)
