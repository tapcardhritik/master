from django.shortcuts import render, redirect

def Home_page(request):
    context={"is_login":"LOGIN",
                  "url_rend":"account/login",
                  "title":"Home"
                  }
    if request.user.is_authenticated:
        context={"is_login":"LOGOUT",
                  "url_rend":"account/logout",
                  "title":"Home",
                  "if_dash":"true",
                  "url_dash":"/Dashbord"}
        return render(request, 'Home/index.html',context)
    return render(request, 'Home/index.html',context)