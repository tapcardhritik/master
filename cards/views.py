from django.shortcuts import render, redirect
from .models import VisitingCard,UserLocation
from Register.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from Payment.models import UserValue
import os
import json
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


def upload_visiting_card(request):
    if not request.user.is_authenticated:
        return redirect("/account/login/")
    profile, created = VisitingCard.objects.get_or_create(user=request.user)  # Ensure VisitingCard exists
    if request.method == "POST":
        visiting_card = request.FILES.get("visiting_card")  # Ensure correct field name
        if visiting_card:
            profile.visiting_card = visiting_card  # Update image
            profile.save()
            return redirect("/Dashbord")  # Redirect after successful upload

    return render(request, "Cards/card_upload.html", {"profile": profile})


def get_uuid(request):
    if not request.user.is_authenticated:
        return redirect("account/login/")
    user = User.objects.get(username=request.user)  # Replace with the actual username
    profile = Profile.objects.get(user=user)
    print(profile.uid)
    return redirect(f'/card/my_user/{profile.uid}')

def get_download_card(request):
    print("AM CALLEed")
    user = User.objects.get(username="hritik@ok.com")  # Replace with the actual username
    profile = Profile.objects.get(user=user)
    print(profile.uid)
    return render(request,"Cards/card.html")

def get_Visiting_card_by_uuid(request, uuid_value):
    obj=Profile.objects.get(uid=uuid_value)
    user = User.objects.get(username=obj) 
    val = UserValue.objects.filter(user=user).first()
    val.value=val.value-1
    val.save()
    print(val.value) 
    print(user)
    if val.value<1:
        return render(request,"Cards/limit.html")
    profile = VisitingCard.objects.get(user=user)
    download_url = "/card/download-card/"
    return render(request, 'Cards/card.html', {'image_url': profile.visiting_card.url, 'download_url': download_url})



    
def view_and_download_card(request):
    """ Display visiting card and trigger automatic download """
    profile = VisitingCard.objects.get(user=request.user)
    
    print("UUUUUUUUUUUUUUUUUUU",profile.visiting_card.url)
    download_url = "/card/download-card/"
    return render(request, 'Cards/card.html', {'image_url': profile.visiting_card.url, 'download_url': download_url})

def download_visiting_card(request):
    try:
        print("OPOPOPOOPOPO")
        profile = VisitingCard.objects.get(user=request.user)

        # Construct the full path using MEDIA_ROOT
        file_path = os.path.join(settings.MEDIA_ROOT, str(profile.visiting_card))

        print("OOOOOOOOOOOOOOOOOOOO", file_path)  # Debugging

        # Check if the file exists
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename="Visiting_Card.jpg")
        else:
            return JsonResponse({"error": "File not found"}, status=404)
    
    except VisitingCard.DoesNotExist:
        return JsonResponse({"error": "User does not have a visiting card"}, status=404)

@csrf_exempt  
def save_user_data(request):
    """ Save user data (location, date, time, user agent) in the database """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            date=data.get('date'),
            time=data.get('time'),
            user_agent=data.get('user_agent')
            print(latitude[0])
            print(longitude[0])
            print(date[0])
            print(time[0])
            print(user_agent[0])
            user = User.objects.get(username=request.user)
            location = UserLocation.objects.create(user=user, latitude=latitude[0], longitude=longitude[0], device=user_agent[0], timestamp=now())
            location.save()
            print("sucesss")
            return JsonResponse({"message": "Data saved successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)
