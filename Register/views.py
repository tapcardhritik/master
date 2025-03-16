from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from .models import Profile
from Payment.models import UserValue
# Login View
def login_page(request):
    if request.user.is_authenticated:  # Check if user is already logged in
        return redirect('/Dashbord')
    
    
    if request.method == 'POST':
        email = request.POST.get("username")
        password = request.POST.get("password")
        print(email)
        print(password)

        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, "User does not exist")
            return redirect('/Dashbord')

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/Dashbord')  # Make sure 'home' is a valid URL name in your Django URLs
        
    return render(request, 'Register/login.html')

# Register View
def register_page(request):
    if request.user.is_authenticated:  # Check if user is already logged in
        return redirect('/Dashbord')
    
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm_password")
        profile_image = request.FILES.get("profile_picture")
        print(username, email, password1, password2, profile_image)

        if password1 != password2:
            messages.warning(request, "Passwords do not match")
            return HttpResponseRedirect(request.path_info)

        if User.objects.filter(username=email).exists():
            messages.warning(request, "User already exists")
            return HttpResponseRedirect(request.path_info)

        # Create the user
        user_obj = User.objects.create(first_name=username, email=email, username=email)
        user_obj.set_password(password1)
        user_obj.save()

        # Create the user profile
        Profile.objects.create(user=user_obj, Profile_image=profile_image)

        # Fetch the correct user object
        value = UserValue.objects.create(user=user_obj)  # ✅ Corrected
        value.save()

        messages.success(request, "Account created successfully")
        return redirect('/account/login')

    return render(request, 'Register/Register.html')
# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/')  # Redirect to login page after logout

def edit(request):
    user_obj = User.objects.filter(username=request.user)
    return render(request,"Register/update_detail.html")