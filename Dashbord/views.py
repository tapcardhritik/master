from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Register.models import Profile  
from Payment.models import UserValue
from django.contrib.auth.models import User
from cards.models import UserLocation,VisitingCard


def DashBord_page(request):
    if not request.user.is_authenticated:
        return redirect("/account/login")
    user = User.objects.get(username=request.user)
    try:
        visiting_card = VisitingCard.objects.get(user=user)
    except VisitingCard.DoesNotExist:
        visiting_card = None
    if not visiting_card:
        return redirect("/card/upload-card/")

    user = request.user  # Get the logged-in user
    profile = Profile.objects.get(user=user)  
    val = UserValue.objects.filter(user=user).first()  

    # Ensure val.value is always available
    count = val.value if val else 0  

    # Get user locations and convert to a list of dictionaries
    user_locations = UserLocation.objects.filter(user=user)
    locations = [
        {
            "latitude": float(loc.latitude),
            "longitude": float(loc.longitude),
            "device": loc.device
        }
        for loc in user_locations
    ]

    # Debugging prints (remove after testing)
    print(user.first_name)
    print(count)
    for loc in locations:
        print(loc["latitude"], loc["longitude"])

    context = {
        "profile": profile,
        "count": count,
        "name": user.first_name,
        "email": user.username,
        "locations": locations,  # Pass formatted location data
        "visiting_card": visiting_card
    }

    return render(request, 'Dashbord/dashbord.html', context)
