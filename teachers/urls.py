from django.urls import path
from .views import *
urlpatterns = [
    path('',index),
    path('dashboard',dashboard),
    path('create-test-obj',create_test_objective),
    path('create-test-subj',create_test_subjective),
    path('view-questions',view_question),
]