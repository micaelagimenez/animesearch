from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Anime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
import json

from django.http import HttpResponse
from django.views import View
from .forms import NewUserForm, UserForm, ProfileForm 


def homepage(request):
    return render(request, template_name="home.html")


def search(request):
   animes = []

   if request.method=='POST' and 'search' in request.POST :
       animes_url = 'https://api.jikan.moe/v3/search/anime?q={}&limit=6&page=1'
       
       search_params = {
           'animes' : 'title',
           'q' : request.POST['search']
           
           }

       r = requests.get(animes_url, params=search_params)
       results = r.json()
       
       results = results['results']
       
       
       if len(results):
           for result in results:
               animes_data = {
                   'Id' : result["mal_id"],
                   'Title' : result["title"],
                   'Episodes' : result["episodes"],
                   'Image' : result["image_url"]
               }
               animes.append(animes_data)
       else:
           message = print("No results found")
       
       for item in animes:
           id = item.get("Id")  
           title = item.get("Title")
           episodes = item.get("Episodes")
           image = item.get("Image")
           
           anime_in_database = Anime.objects.filter(title=title).exists()
           if not anime_in_database:
              anime = Anime.objects.create(mal_id=id, title=title, episodes=episodes, image=image) 
              anime.save()

       context = {
        'animes' : animes
        }
            
       return render(request,'search.html', context)

   elif request.method=='POST' and 'anime_id' in request.POST :

       anime_id = request.POST.get("anime_id")
       anime = Anime.objects.get(mal_id = anime_id)
       request.user.profile.favorites.add(anime)
       messages.success(request,(f'{anime} added to wishlist.'))
       
    
   return render(request,'search.html')
       

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="registration/signup.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/search")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("core:homepage")


@login_required
def profile(request):
    
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request,('Your wishlist was successfully updated!'))
        else:
            messages.error(request,('Unable to complete request'))
        return redirect ("profile")
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request = request, template_name ="profile.html", context = {"user":request.user, 
		"user_form": user_form, "profile_form": profile_form,})

