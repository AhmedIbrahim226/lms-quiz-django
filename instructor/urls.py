from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    # ---- ins---
    path('Home/', views.instructor_home, name='instructor_home'),
    path('Schedule/', views.Schedule_home, name='Schedule_home'),
    path('Settings/', views.Settings, name='Settings'),
    path('Schedule/<Schedule_Name>/Material', views.instructor_Material, name='instructor_Material'),
    path('Schedule/<Schedule_Name>/Task', views.instructor_Task, name='instructor_Task'),

    path('Schedule/<Schedule_Name>/Material/Delete/<id>/<type>', views.delete_material,
         name='delete_material'),
    path('Schedule/<Schedule_Name>/Material/Task/<id>/<type>', views.delete_task, name='delete_task'),
    path('Schedule/<Schedule_Name>/<username>/ViewTasks', views.ViweTasks, name='ViweTasks'),
    path('Schedule/<Schedule_Name>/<username>/ViewTasks/<id>/Delete', views.detet_task_ans,
         name='detet_task_ans'),
    path('Schedule/<Schedule_Name>/view_student', views.std_open_Schedule, name='std_open_Schedule'),
    path('Schedule/<Schedule_Name>', views.Schedule_view, name='Schedule_Instructor'),
    path('Schedule/Material/view', views.view_Material, name='view_Material'),
    path('Schedule/<Schedule_Name>/<username>/report', views.report, name='report'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
