from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
def get_default_user():
    user = get_user_model().objects.first()  # Returns the first user in the database
    return user.id if user else None  # Return user ID instead of user object


class HackathonsList(models.Model):
    STATUS_CHOICES = [
        (True, "Active"),
        (False, "Inactive"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    prize = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.BooleanField(choices=STATUS_CHOICES, default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Uses custom user model if swapped
        on_delete=models.CASCADE,  # Deletes hackathons when user is deleted
        default=get_default_user  # ✅ Use function reference, no parentheses
    )

    def __str__(self):
        return self.title

class HackathonApplication(models.Model):
    hackathon = models.ForeignKey(HackathonsList, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Store user reference
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} applied for {self.hackathon.title}"

