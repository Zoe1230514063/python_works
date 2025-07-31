from django.urls import path
from .views import (
    my_assignments,
    delete_assignment,
    assignment_detail,
    student_list_for_assignment,
    assignment_list
)

urlpatterns = [
    path('my/', my_assignments),
    path('<str:assignment_id>/delete/', delete_assignment),
    path('detail/', assignment_detail),         # GET /api/assignments/detail/
    path('student-list/', student_list_for_assignment), # GET /api/assignments/student-list/
    path('', assignment_list),  # GET /api/assignments/
]
