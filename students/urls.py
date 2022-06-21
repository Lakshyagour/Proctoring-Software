from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('test-login', test_login),
    path('give-test', give_test_objective),
    path('video_stream', video_stream,name = "video_stream"),
]
