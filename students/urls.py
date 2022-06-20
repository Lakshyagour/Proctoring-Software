from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('give-test', give_test),
    path('', dashboard)
]
