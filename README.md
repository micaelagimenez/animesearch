# Anime Website
Django website that uses https://jikan.moe/ API to retrieve animes from the website MyAnimeList.
User can register and login. The search engine allows the user to search for animes and add their favorites to their profile. On their profile, the user can edit their username and email as well as delete favorite animes.


## Endpoints 
1. Homepage.
2. Register.
3. Login.
4. Password reset.
5. Search.
6. Profile

## 1. Homepage
The homepage shows the user a message and asks them to either register or login to proceed.

## 2. Register
User can register using a username, an email and a password.

## 3. Login
User can login using their username and password or be redirected to the password reset view in case they forgot their password. 

## 4. Password reset
User can reset their password using their email.

## 5. Search
Users can search for animes given their title. If the user is registered, they can click on a star button to add the anime to their profile. 

## 6. Profile
User can check their profile to see their account's data and their favorite animes. They can modify their data by clicking on the "edit profile" button and delete animes by clicking on the "x" button.
