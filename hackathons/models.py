from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.

# class Standard(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

class HackathonsList(models.Model):
    STATUS_CHOICES = [
        (True, "Active"),
        (False, "Inactive"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    # image = models.ImageField(upload_to='hackathons_list/')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.BooleanField(choices=STATUS_CHOICES, default=True)
    # link = models.URLField()

    def __str__(self):
        return self.title

class HackathonApplication(models.Model):
    hackathon = models.ForeignKey(HackathonsList, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Store user reference
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} applied for {self.hackathon.title}"

