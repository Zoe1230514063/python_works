from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.classes.views import class_list
from apps.assignments.views import publish_assignment, assignment_detail, student_list_for_assignment
from apps.submissions.views import to_mark_list, update_score
from apps.users.views import student_add, student_delete
from apps.assignments.views import my_assignments, delete_assignment

urlpatterns = [
    path('admin/', admin.site.urls),

    # 所有以 /api/ 开头的路由
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.assignments.urls')),
    path('api/submissions/', include('apps.submissions.urls')),
    path('api/assignments/', include('apps.assignments.urls')),

    # 单独挂载的路由
    path('api/classes/', class_list),
    path('api/assignments/publish/', publish_assignment),
    path('api/submissions/to-mark/', to_mark_list),
    path('api/submissions/<str:sid>/score/', update_score),

    path('api/students/add/', student_add),  # 新增学生
    path('api/students/<str:sno>/delete/', student_delete),  # 删除学生

    path('api/assignments/my/', my_assignments),
    path('api/assignments/<str:assignment_id>/delete/', delete_assignment),

    path('api/assignments/detail/', assignment_detail),
    path('api/assignments/student-list/', student_list_for_assignment),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)