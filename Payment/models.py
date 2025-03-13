from django.db import models
from django.contrib.auth.models import User
from Base.models import BaseModel

class UserValue(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_value')
    value = models.IntegerField(default=10)  # Default value is 10

    def __str__(self):
        return f"{self.user.username} - {self.value}"
