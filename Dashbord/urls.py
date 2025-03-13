from django.urls import path
from .views import DashBord_page

urlpatterns = [
    path('', DashBord_page, name='Dashbord'),
]