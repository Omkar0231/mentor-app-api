from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class AvailableSlot(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    time = models.TimeField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name}: {self.date} {self.time} ({'Available' if self.available else 'Unavailable'})"
