from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpadteForm
from django.contrib.auth.decorators import login_required

def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get("username")
			messages.success(request, f"Your account has been created! You are now able to log in.")
			return redirect("login")
	else:
		form = UserRegisterForm()
	return render(request, "users/register.html", {"form": form, "title": "Register"})

@login_required
def profile(request):

	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpadteForm(request.POST, 
								   request.FILES,
								   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f"Your account has been updated")
			return redirect("profile")

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpadteForm(instance=request.user.profile)

	context = {
		"u_form": u_form,
		"p_form": p_form
	}
	return render(request, "users/profile.html", context)
