from django.shortcuts import render, redirect

def Home_page(request):
    context={"is_login":"LOGIN",
                "element_2_title":"Register",
                "element_2_data":'data-toggle=modal data-target=#modal-form-signup',
                  "element_rend":'data-toggle=modal data-target=#modal-form',
                  }
    if request.user.is_authenticated:
        context={"is_login":"LOGOUT",
                  "url":'/account/logout',
                  "title":"Home",
                  "element_2_title":"Dashbord",
                  "element_2_url":"/Dashbord",
                 
                 }
        return render(request, 'Base/index.html',context)
    return render(request, 'Base/index.html',context)