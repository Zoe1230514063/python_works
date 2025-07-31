from django.urls import path
from .views import login, students_list

urlpatterns = [
    path('login/', login),
    path('students/', students_list),
]