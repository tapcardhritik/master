from django.urls import path
from .views import upload_visiting_card,get_download_card,get_uuid,get_Visiting_card_by_uuid,save_user_data,download_visiting_card,view_and_download_card

urlpatterns = [
    path('upload-card/', upload_visiting_card, name='upload_visiting_card'),
    path('get_download/', get_download_card, name='get_download_card'),
    path('my_user/<uuid:uuid_value>/', get_Visiting_card_by_uuid, name="get_profile_by_uuid"),
    path('save-user-data/', save_user_data, name='save_user_data'),
    path('download-card/', download_visiting_card, name='download_card'),
    path('get_uuid/',get_uuid, name='get_uuid'),
]



