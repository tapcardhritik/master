from Base.models import BaseModel
from django.db import models
from django.contrib.auth.models import User  # The same User model used in Register.models
from django.utils.timezone import now

class VisitingCard(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visiting_card')
    visiting_card = models.ImageField(upload_to='visiting_cards/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Visiting Card"

class UserLocation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    device = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=now)


    def __str__(self):
        return f"{self.user.username} - {self.latitude}, {self.longitude} - {self.device}"
