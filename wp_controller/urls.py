from django.urls import path
from .views import ReceiveMessage

urlpatterns = [
    path('receive/', ReceiveMessage.as_view(), name='receive-message'),
]
