from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    # ---- std---
    path('Home/', views.student_home, name='student_home'),
    path('Schedule/<Schedule_Name>/', views.Schedule, name='Schedule'),
    path('Schedule/<Schedule_Name>/Material/video/', views.Schedule_Material_video,
         name='Schedule_Material_video'),
    path('Schedule/<Schedule_Name>/Task/', views.Schedule_task, name='Schedule_task'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
