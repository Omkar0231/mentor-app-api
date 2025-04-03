from django.urls import path
from .views import UpdateUserDetails, CreateAvailableSlots, UpdateAvailableSlot

urlpatterns = [
    path('update-user-details/', UpdateUserDetails.as_view(), name='create-or-list-user-details'),
    path('update-user-details/<int:user_id>/', UpdateUserDetails.as_view(), name='update-user-details'),
    path('update-available-slots/<int:user_id>/', CreateAvailableSlots.as_view(), name='create-slots'),
    path('update-available-slot/<int:slot_id>/', UpdateAvailableSlot.as_view(), name='update-slot'),
]
