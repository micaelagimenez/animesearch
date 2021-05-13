from django.shortcuts import  render, redirect
from .models import Anime, Profile
from .forms import NewUserForm, UserForm, ProfileForm 
from django.views import View

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.urls import reverse

import requests
import json
from django.http import HttpResponse


from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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
       return render(request, 'profile.html')
    
    
   return render(request,'search.html')
       

@login_required
def profile(request):
    
    if request.method=='POST' and 'favorite_id' in request.POST :
            favorite_id = request.POST.get("favorite_id")
            request.user.profile.favorites.remove(favorite_id)
            messages.success(request,('Anime deleted from wishlist.'))
            return redirect("/profile")
    elif request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,('Your profile was successfully updated!'))
        else:
            messages.error(request,('Unable to complete request'))
            return redirect ("/profile")  
    
    user_form = UserForm()
    
    return render(request, 'profile.html',context = {"user":request.user, "user_form": user_form })


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


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_text.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'braavosi@outlook.es' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("core:homepage")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})