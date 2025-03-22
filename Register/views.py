from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from .models import Profile
from Payment.models import UserValue
from django.http import JsonResponse
import json
# Login View
def login_page(request):
    # If the user is already authenticated, redirect them
    if request.user.is_authenticated:
        return redirect('/Dashbord')

    # Handle the POST request when the form is submitted
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            
            # Try to find the user by email
            user_obj = User.objects.filter(username=email).first()

            if not user_obj:
                return JsonResponse({'success': False, 'message': 'User does not exist'}, status=400)

            # Authenticate the user
            user_obj = authenticate(username=email, password=password)
            
            if user_obj is not None:
                # Log the user in and send a success response
                login(request, user_obj)
                return JsonResponse({'success': True})
            else:
                # Authentication failed
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)
    return redirect('/')

    # If not a POST request, render the login page
# Register View
def register_page(request):
    # If the user is already authenticated, redirect them to the dashboard
    if request.user.is_authenticated:
        return redirect('/Dashbord')

    # Handle POST request when the form is submitted
    if request.method == 'POST':
        # If the request is from a JSON API
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password1 = data.get("password")
            password2 = data.get("confirm_password")
            profile_image = data.get("profile_picture")  # The profile image URL or base64 string
            print(username)
            print(email)
            print(password1)
            print(profile_image)

            if User.objects.filter(username=email).exists():
                return JsonResponse({'success': False, 'message': 'User already exists'}, status=400)

            # Create the user object
            user_obj = User.objects.create(first_name=username, email=email, username=email)
            user_obj.set_password(password1)
            user_obj.save()

            # Create the user profile (optional field, you can modify this if profile image is provided via API)
            if profile_image:
                # Handle image upload or saving logic here
                Profile.objects.create(user=user_obj, Profile_image=profile_image)
            else:
                # If no profile image is provided, set a default image (if required)
                Profile.objects.create(user=user_obj, Profile_image='default-image.jpg')  # Use a default image

            # Create the user value (optional or related model)
            value = UserValue.objects.create(user=user_obj)
            value.save()

            return JsonResponse({'success': True, 'message': 'Account created successfully'})

    return redirect("/")

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/')  # Redirect to login page after logout

def edit(request):
    user_obj = User.objects.filter(username=request.user)
    return render(request,"Register/update_detail.html")