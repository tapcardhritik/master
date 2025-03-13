from django.db import models
from Base.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    is_email_varified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    Profile_image=models.ImageField(upload_to='profile')
    
    def __str__(self):
        return self.user.username