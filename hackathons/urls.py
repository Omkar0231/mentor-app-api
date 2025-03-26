from django.urls import path
from . import views


# localhost:8000/chai/
urlpatterns = [
    path('create-hackathon/', views.HackathonsListView.as_view(), name='hackathons_api'),

    path('create-hackathon/<int:pk>/', views.HackathonView.as_view(), name='hackathon-detail'),

    path('create-hackathon/<int:pk>/apply/', views.ApplyHackathonView.as_view(), name='hackathon-apply'),
    path('create-hackathon/applications/', views.HackathonApplicationsListView.as_view(), name='hackathon-applications'),
]