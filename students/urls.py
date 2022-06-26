from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('test-login', test_login),
    path('give_test_objective', give_test_objective,name = "give_test_objective"),
    path('video_stream', video_stream,name = "video_stream"),
    path('test_result', test_result,name = "test_result"),
    path('save-proctor-log-to-media', save_proctor_log),
]
