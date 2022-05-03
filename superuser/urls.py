from django.urls import path
from . import views
from . import blog


urlpatterns = [
    path('', views.super_user_login, name='super-user-login'),
    path("dashboard/", views.super_user_home, name='super-user-home'),
    path("dashboard/company-requests/", views.super_user_company_requests, name='super-user-company-requests'),
    
    path("dashboard/company-requests/data/", views.get_request_data, name=''),

    path("dashboard/companies/", views.get_all_companies, name='all-companies'),
    path("dashboard/companies/delete/<id>/", views.del_company, name='super-del-company'),

    path("dashboard/admins/", views.get_all_admins, name='super-all-admins'),
    path("dashboard/admins/delete/<id>/", views.del_admin, name='super-del-admin'),
    
    path("dashboard/instructors/", views.get_all_instructor, name='super-all-instructors'),
    path("dashboard/instructors/delete/<id>/", views.del_instructor, name='super-del-instructor'),

    path("dashboard/students/", views.get_all_student, name='super-all-students'),
    path("dashboard/students/delete/<id>/", views.del_student, name='super-del-student'),

    path("dashboard/parents/", views.get_all_parent, name='super-all-parents'),
    path("dashboard/parents/delete/<id>/", views.del_parent, name='super-del-parent'),


    path("dashboard/messages/", blog.get_message_unread, name='super-msg'),
    path("dashboard/response-description/", blog.response_message_description),

]
