from django.shortcuts import render, redirect
from django.core.mail import send_mail
from users.models import(
    StudentAccount, ParentAccount, ExtraPermissions,
    CompanyRequest, InstructorAccount,
    SuperUserAccount, AdminAccount, Company
)
from userapi import utilities
import re, random, string
from smtplib import SMTPException

from schedule.models import (
    Course, Schedule, InstructorSchedule,
    StudentSchedule, Material, MaterialVideo, TaskInstructor
)
from schedule.models import TaskStudent
from django.http import JsonResponse
from django.urls import reverse


def home_admin(request):
    if request.user.id is None:
        return redirect("home")

    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),

    }
    return render(request, 'admin/home.html', context)


def Schedule_admin(request):
    if request.user.id is None:
        return redirect("home")
    if request.method == "POST":
        Schedule.objects.create(
            schedule_name=request.POST["Schedule_Name"],
            company_name=request.user.company_name,
            course_name=request.POST["course_name"],
        ).save()
    context = {
        "course": Course.objects.filter(company_name=request.user.company_name).order_by("-created_on"),
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),

    }
    return render(request, 'admin/Schedule.html', context)


def Course_admin(request):
    if request.user.id is None:
        return redirect("home")
    if request.method == "POST":
        Course.objects.create(
            course_name=request.POST['Course_Name'],
            company_name=request.user.company_name,
        ).save()
    context = {
        "courses": Course.objects.filter(company_name=request.user.company_name).order_by("-created_on"),
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/course.html', context)


def Schedule_instructor_admin(request):
    if request.user.id is None:
        return redirect("home")
    if request.method == "POST":
        print(request.POST['instructor'])
        if False == InstructorSchedule.objects.filter(instructor_schedule_name=request.POST['Schedule'],
                                                      instructor_name=request.POST['instructor']).exists():
            InstructorSchedule.objects.create(
                instructor_schedule_name=request.POST['Schedule'],
                company_name=request.user.company_name,
                instructor_name=request.POST['instructor']
            ).save()

    context = {
        "instructor": InstructorAccount.objects.filter(company_name=request.user.company_name, is_active=True),
        "ScheduleInstructor": InstructorSchedule.objects.filter(company_name=request.user.company_name),
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/Schedule_instructor.html', context)


def Schedule_student(request):
    if request.user.id is None:
        return redirect("home")

    if request.method == "POST":
        x = request.POST.get("len")
        print(x)
        y = int(x)
        print(type(y))
        print(request.POST['Schedule'])
        for i in range(0, y):

            if False == StudentSchedule.objects.filter(student_schedule_name=request.POST['Schedule'],
                                                       student_name=request.POST.get(f"data[{i}]")).exists():
                StudentSchedule.objects.create(
                    student_schedule_name=request.POST['Schedule'],
                    company_name=request.user.company_name,
                    student_name=request.POST.get(f"data[{i}]")
                ).save()

        return JsonResponse({"suss": True})
    if "getdata" in request.GET:

        student = StudentAccount.objects.filter(company_name=request.user.company_name,
                                                id_college__icontains=request.GET['id_college'])
        xx = []
        for x in student:
            xx.append(f'{x.username} {x.first_name} {x.last_name}')
        return JsonResponse({"getdatasea": xx})
    context = {
        "student": StudentAccount.objects.filter(company_name=request.user.company_name,
                                                 id_college__icontains="2018030"),
        "Schedule": Schedule.objects.filter(company_name=request.user.company_name),
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/Schedule_student.html', context)


def manage_Schedule(request, ScheduleName):
    instuctors_schedule = InstructorSchedule.objects.filter(instructor_schedule_name=ScheduleName,
                                                            company_name=request.user.company_name)
    instructor_data = InstructorAccount.objects.filter(username__in=[x.instructor_name for x in instuctors_schedule])
    Course.objects.filter()
    # instructor_name

    Studentcount = StudentSchedule.objects.filter(company_name=request.user.company_name,
                                                  student_schedule_name=ScheduleName).count
    materialcount1 = Material.objects.filter(company_name=request.user.company_name, Schedule_name=ScheduleName).count
    materialcount2 = MaterialVideo.objects.filter(company_name=request.user.company_name,
                                                   Schedule_name=ScheduleName).count
    taskcount = TaskInstructor.objects.filter(company_name=request.user.company_name, Schedule_name=ScheduleName).count
    # materialcount=(int(materialcount1) +int(materialcount2))
    student_schedule = StudentSchedule.objects.filter(student_schedule_name=ScheduleName,
                                                      company_name=request.user.company_name)
    student_data = StudentAccount.objects.filter(username__in=[x.student_name for x in student_schedule])

    print(instuctors_schedule)
    context = {
        "instuctors_schedule": instructor_data,
        "ScheduleName": ScheduleName,
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
        "course_name": Schedule.objects.get(company_name=request.user.company_name, schedule_name=ScheduleName),
        "Studentcount": Studentcount,
        "materialcount1": materialcount1,
        "materialcount2": materialcount2,
        "taskcount": taskcount,
        "student_data": student_data,

    }
    return render(request, 'admin/manage_Schedule.html', context)


def delete_user_Schedule(request, ScheduleName, username, type):
    if type == "instructor":
        deletesc = InstructorSchedule.objects.filter(instructor_schedule_name=ScheduleName, instructor_name=username)
        for d in deletesc:
            InstructorSchedule.objects.get(id=d.id).delete()

    if type == "student":
        deletestd = StudentSchedule.objects.filter(student_schedule_name=ScheduleName, student_name=username)
        for d in deletestd:
            StudentSchedule.objects.get(id=d.id).delete()
        student_task_delete = TaskStudent.objects.filter(std_username=username, std_schedule=ScheduleName)
        for i in student_task_delete:
            TaskStudent.objects.get(id=i.id).delete()

    context = {

    }
    return redirect(reverse("manage_Schedule", kwargs={"ScheduleName": ScheduleName}))


def delete_Schedule(request, ScheduleName):
    Schedule.objects.get(schedule_name=ScheduleName).delete()

    ins_sc = InstructorSchedule.objects.filter(instructor_schedule_name=ScheduleName)
    for i in ins_sc:
        InstructorSchedule.objects.get(id=i.id).delete()

    std_sc = StudentSchedule.objects.filter(student_schedule_name=ScheduleName)
    for i in std_sc:
        StudentSchedule.objects.get(id=i.id).delete()

    mat = Material.objects.filter(Schedule_name=ScheduleName)
    for i in mat:
        Material.objects.get(id=i.id).delete()

    task_std = TaskStudent.objects.filter(std_schedule=ScheduleName)
    for i in task_std:
        TaskStudent.objects.get(id=i.id).delete()

    Taskins = TaskInstructor.objects.filter(Schedule_name=ScheduleName)
    for i in Taskins:
        TaskInstructor.objects.get(id=i.id).delete()

    return redirect("home_admin")


def manage_admin(request):
    if request.method == "POST":
        # print(request.POST)
        if "AddAdminS" in request.POST:
            createadmin = AdminAccount.objects.create(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                first_name=request.POST.get('firstname'),
                last_name=request.POST.get('lastname'),
                company_name=request.user.company_name,
                admin_type=request.POST.get('Type'),

            )
            createadmin.set_password(request.POST.get('Password'))
            createadmin.save()

            createExtraPermissions = ExtraPermissions.objects.create(
                user_have_perm=createadmin.username,
                company_name=createadmin.company_name,
                update_assistant=False,
                update_doctor=False,
                update_student=False,
                update_trainer=False,
            )
            createExtraPermissions.save()
            add_ExtraPermissions = ExtraPermissions.objects.get(
                user_have_perm=createadmin.username,
                company_name12222=createadmin.company_name,

            )
            print(createadmin.username)
            if (request.POST.get(f"Doctor[0]") == "on"):
                add_ExtraPermissions.add_doctor = True
            if (request.POST.get(f"Doctor[1]") == "on"):
                add_ExtraPermissions.delete_doctor = True
            if (request.POST.get(f"Doctor[2]") == "on"):
                add_ExtraPermissions.update_doctor = True

            if (request.POST.get(f"Assistant[0]") == "on"):
                add_ExtraPermissions.add_assistant = True
            if (request.POST.get(f"Assistant[1]") == "on"):
                add_ExtraPermissions.delete_assistant = True
            if (request.POST.get(f"Assistant[2]") == "on"):
                add_ExtraPermissions.update_assistant = True

            if (request.POST.get(f"Trainer[0]") == "on"):
                add_ExtraPermissions.add_trainer = True
            if (request.POST.get(f"Trainer[1]") == "on"):
                add_ExtraPermissions.delete_trainer = True
            if (request.POST.get(f"Trainer[2]") == "on"):
                add_ExtraPermissions.update_trainer = True

            if (request.POST.get(f"Admin[0]") == "on"):
                add_ExtraPermissions.add_admin = True
            if (request.POST.get(f"Admin[1]") == "on"):
                add_ExtraPermissions.delete_admin = True
            if (request.POST.get(f"Admin[2]") == "on"):
                add_ExtraPermissions.update_admin = True

            if (request.POST.get(f"Student[0]") == "on"):
                add_ExtraPermissions.add_student = True
            if (request.POST.get(f"Student[1]") == "on"):
                add_ExtraPermissions.delete_student = True
            if (request.POST.get(f"Student[2]") == "on"):
                add_ExtraPermissions.update_student = True

            if (request.POST.get(f"Course[0]") == "on"):
                add_ExtraPermissions.open_course = True
            if (request.POST.get(f"Course[1]") == "on"):
                add_ExtraPermissions.delete_course = True
            add_ExtraPermissions.save()
        if "EditAdminS" in request.POST:
            editadmin = AdminAccount.objects.get(
                username=request.POST.get('E_username'),
                company_name=request.user.company_name
            )
            editadmin.username = request.POST.get('E_username')
            editadmin.email = request.POST.get('E_email')
            editadmin.first_name = request.POST.get('E_firstname')
            editadmin.last_name = request.POST.get('E_lastname')
            editadmin.company_name = request.user.company_name
            # editadmin.admin_type =request.POST.get('E_Type') 
            if ("Active" in request.POST):
                editadmin.is_active = True
            else:
                editadmin.is_active = False
            editadmin.save()

            add_ExtraPermissions = ExtraPermissions.objects.get(
                user_have_perm=editadmin.username,
                company_name=editadmin.company_name,

            )

            if (request.POST.get(f"e_Doctor[0]") == "on"):
                add_ExtraPermissions.add_doctor = True
            else:
                add_ExtraPermissions.add_doctor = False

            if (request.POST.get(f"e_Doctor[1]") == "on"):
                add_ExtraPermissions.update_doctor = True
            else:
                add_ExtraPermissions.update_doctor = False
            if (request.POST.get(f"e_Doctor[2]") == "on"):
                add_ExtraPermissions.delete_doctor = True
            else:
                add_ExtraPermissions.delete_doctor = False
            if (request.POST.get(f"e_Assistant[0]") == "on"):
                add_ExtraPermissions.add_assistant = True
            else:
                add_ExtraPermissions.add_assistant = False
            if (request.POST.get(f"e_Assistant[2]") == "on"):
                add_ExtraPermissions.delete_assistant = True
            else:
                add_ExtraPermissions.delete_assistant = False

            if (request.POST.get(f"e_Assistant[1]") == "on"):
                add_ExtraPermissions.update_assistant = True
            else:
                add_ExtraPermissions.update_assistant = False

            if (request.POST.get(f"e_Trainer[0]") == "on"):
                add_ExtraPermissions.add_trainer = True
            else:
                add_ExtraPermissions.add_trainer = False
            if (request.POST.get(f"e_Trainer[2]") == "on"):
                add_ExtraPermissions.delete_trainer = True
            else:
                add_ExtraPermissions.delete_trainer = False
            if (request.POST.get(f"e_Trainer[1]") == "on"):
                add_ExtraPermissions.update_trainer = True
            else:
                add_ExtraPermissions.update_trainer = False
            if (request.POST.get(f"e_Admin[0]") == "on"):
                add_ExtraPermissions.add_admin = True
            else:
                add_ExtraPermissions.add_admin = False
            if (request.POST.get(f"e_Admin[2]") == "on"):
                add_ExtraPermissions.delete_admin = True
            else:
                add_ExtraPermissions.delete_admin = False
            if (request.POST.get(f"e_Admin[1]") == "on"):
                add_ExtraPermissions.update_admin = True
            else:
                add_ExtraPermissions.update_admin = False
            if (request.POST.get(f"e_Student[0]") == "on"):
                add_ExtraPermissions.add_student = True
            else:
                add_ExtraPermissions.add_student = False
            if (request.POST.get(f"e_Student[2]") == "on"):
                add_ExtraPermissions.delete_student = True
            else:
                add_ExtraPermissions.delete_student = False
            if (request.POST.get(f"e_Student[1]") == "on"):
                add_ExtraPermissions.update_student = True
            else:
                add_ExtraPermissions.update_student = False

            if (request.POST.get(f"e_Course[0]") == "on"):
                add_ExtraPermissions.open_course = True
            else:
                add_ExtraPermissions.open_course = False
            if (request.POST.get(f"e_Course[1]") == "on"):
                add_ExtraPermissions.delete_course = True
            else:
                add_ExtraPermissions.delete_course = False
            add_ExtraPermissions.save()

    if "dataget" in request.GET:
        print(request.GET['username'])
        extraPermissions = ExtraPermissions.objects.get(
            user_have_perm=request.GET['username'],
            company_name=request.user.company_name,
        )
        Permissions = {
            "add_doctor": extraPermissions.add_doctor,
            "delete_doctor": extraPermissions.delete_doctor,
            "update_doctor": extraPermissions.update_doctor,
            "add_assistant": extraPermissions.add_assistant,
            "delete_assistant": extraPermissions.delete_assistant,
            "update_assistant": extraPermissions.update_assistant,
            "add_trainer": extraPermissions.add_trainer,
            "delete_trainer": extraPermissions.delete_trainer,
            "update_trainer": extraPermissions.update_trainer,
            "add_admin": extraPermissions.add_admin,
            "delete_admin": extraPermissions.delete_admin,
            "update_admin": extraPermissions.update_admin,
            "add_student": extraPermissions.add_student,
            "delete_student": extraPermissions.delete_student,
            "update_student": extraPermissions.update_student,
            "open_course": extraPermissions.open_course,
            "delete_course": extraPermissions.delete_course,
        }
        return JsonResponse(Permissions)
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
        "AdminAccount": AdminAccount.objects.filter(company_name=request.user.company_name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username), }
    return render(request, 'admin/Manage_Admin.html', context)


def deleteadmin(request, id, username):
    AdminAccount.objects.get(id=id).delete()
    ExtraPermissions.objects.get(user_have_perm=username).delete()
    return redirect(reverse("manage_admin", kwargs={}))


def manage_instructor(request):
    if request.method == "POST":
        if "ADDInstructor" in request.POST:
            createinst = InstructorAccount.objects.create(
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                first_name=request.POST.get("firstname"),
                last_name=request.POST.get("lastname"),
                department=request.POST.get("department"),
                company_name=request.user.company_name,
                instructor_type=request.POST.get("type"),
            )
            createinst.set_password("password")
            createinst.save()
            createpre = ExtraPermissions.objects.create(
                user_have_perm=createinst.username,
                company_name=createinst.company_name,
            )
            createpre.save()
            print(request.POST)
            editpre = ExtraPermissions.objects.get(
                user_have_perm=createpre.user_have_perm,
                company_name=request.user.company_name,
            )
            print(editpre)

            if (request.POST.get("opencourse") == "on"):
                editpre.open_course = True
            if (request.POST.get("deletecourse") == "on"):
                editpre.delete_course = True
            if (request.POST.get("material") == "on"):
                editpre.upload_materials = True
            if (request.POST.get("opencourse") == "on"):
                editpre.add_quiz = True
            if (request.POST.get("quiz") == "on"):
                editpre.add_task = True
            if (request.POST.get("post") == "on"):
                editpre.add_post = True
            editpre.save()
        if "EditInstructor" in request.POST:
            edit = InstructorAccount.objects.get(
                username=request.POST.get("eusername"),
            );
            edit.username = request.POST.get("eusername")
            edit.email = request.POST.get("eemail")
            edit.first_name = request.POST.get("efirstname")
            edit.last_name = request.POST.get("efirstname")
            edit.department = request.POST.get("edepartment")
            edit.instructor_type = request.POST.get("etype")

            editpre = ExtraPermissions.objects.get(
                user_have_perm=request.POST.get("eusername")
            )
            if "eactive" in request.POST:
                edit.is_active = True
            else:
                edit.is_active = False
            edit.save()

            if "eopencourse" in request.POST:
                editpre.open_course = True
            else:
                editpre.open_course = False
            if "edeletecourse" in request.POST:
                editpre.delete_course = True
            else:
                editpre.delete_course = False
            if "ematerial" in request.POST:
                editpre.upload_materials = True
            else:
                editpre.upload_materials = False
            if "equiz" in request.POST:
                editpre.add_quiz = True
            else:
                editpre.add_quiz = False
            if "etask" in request.POST:
                editpre.add_task = True
            else:
                editpre.add_task = False
            if "epost" in request.POST:
                editpre.add_post = True
            else:
                editpre.add_post = False
            editpre.save()
    if "getdata" in request.GET:
        getPermissions = ExtraPermissions.objects.get(user_have_perm=request.GET["username"])
        data = {
            "open_course": getPermissions.open_course,
            "delete_course": getPermissions.delete_course,
            "upload_materials": getPermissions.upload_materials,
            "add_quiz": getPermissions.add_quiz,
            "add_task": getPermissions.add_task,
            "add_post": getPermissions.add_post,
        }
        return JsonResponse(data)
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
        "InstructorAccount": InstructorAccount.objects.filter(company_name=request.user.company_name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),

    }

    return render(request, 'admin/Manage_Instructor.html', context)


def deleteinstuctor(request, id, username):
    InstructorAccount.objects.get(id=id).delete()
    ExtraPermissions.objects.get(user_have_perm=username).delete()
    return redirect(manage_instructor)


def manage_Student(request):
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
        "StudentAccount": StudentAccount.objects.filter(company_name=request.user.company_name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
    }
    if request.method == "POST":
        if "ADDStudent" in request.POST:
            # print(request.POST)
            # if False == StudentAccount.objects.filter(
            #         username=request.POST.get("username")).exists() and False == StudentAccount.objects.filter(
            #         email=request.POST.get("email")).exists():
            #
            #     create = StudentAccount.objects.create(
            #         username=request.POST.get("username"),
            #         email=request.POST.get("email"),
            #         first_name=request.POST.get("firstname"),
            #         last_name=request.POST.get("lastname"),
            #         department=request.POST.get("department"),
            #         company_name=request.user.company_name,
            #         id_college=request.POST.get("id_college"),
            #         gender=request.POST.get("gender"),
            #         age=request.POST.get("age"),
            #         national_id=request.POST.get("national_id"),
            #         parent_national_id=request.POST.get("parent_national_id"),
            #     )
            #     create.set_password(request.POST.get("password"))
            #     create.save()
            #     if False == ParentAccount.objects.filter(
            #             email=request.POST.get("emailparnet")).exists() and False == ParentAccount.objects.filter(
            #             national_id=request.POST.get("parent_national_id")).exists():
            #         user = ParentAccount.objects.create(
            #             username=create.last_name + "." + str(create.id),
            #             email=request.POST.get("emailparnet"),
            #             first_name=create.last_name,
            #             last_name="",
            #             national_id=create.parent_national_id,
            #         )
            #         user.set_password("000000")
            #         user.save()
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            department = request.POST.get("department")
            company_name = request.user.company_name
            id_college = request.POST.get("id_college")
            gender = request.POST.get("gender")
            age = request.POST.get("age")
            national_id = request.POST.get("national_id")
            parent_national_id = request.POST.get("parent_national_id")
            password = request.POST.get('password')
            parent_email = request.POST.get("emailparnet")

            if utilities.username_exists(username=username):
                context['username_error'] = 'This username exists!'

            elif utilities.email_exists(email=email):
                context['email_error'] = 'This email exists!'

            expert_password = re.findall("[a-zA-Z]", password)

            if len(password) < 8:
                context['error_pass'] = 'Your password must contain at least 8 characters.'
            elif not expert_password:
                context['error_pass'] = 'Your password can’t be entirely numeric.'

            else:
                try:
                    user = StudentAccount.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        company_name=company_name,
                        department=department,
                        id_college=id_college,
                        gender=gender,
                        age=age,
                        national_id=national_id,
                        parent_national_id=parent_national_id
                    )

                    if ParentAccount.objects.filter(national_id=parent_national_id).exists():
                        user.set_password(password)
                        user.is_active = True
                        user.save()
                        context['success'] = 'Your account created, wait your admin to activate your account.'
                    else:
                        code = string.ascii_letters
                        for i in range(11):
                            code += str(i)
                        rd = random.choices(code, k=15)

                        user_parent = ParentAccount.objects.create_user(
                            username=user.username + ''.join(rd),
                            email=parent_email,
                            first_name='f_name',
                            last_name='l_name',
                            national_id=parent_national_id
                        )

                        send_mail(
                            'Hi you have now parent account!',
                            f'''
                                This account allows you to lookout your children, follow them,
                                and follow up on their studies continuously,
                                as you can know their grades all the time.

                                You can login with: 
                                username: {user_parent.username}
                                password: {''.join(rd)}
                                ''',
                            'bla@colon.com',
                            [parent_email]
                        )
                        user.set_password(password)
                        user.is_active = True
                        user.save()

                        user_parent.set_password(''.join(rd))
                        user_parent.is_active = True
                        user_parent.save()

                        context['success'] = 'Your account created, wait your admin to activate your account.'




                except SMTPException:
                    context['error_send_mail'] = 'Failed to create please try again.'
        if "EditStudent" in request.POST:
            # print(request.POST)                                   
            edit = StudentAccount.objects.get(username=request.POST.get("eusername"))
            edit.email = request.POST.get("eemail")
            edit.first_name = request.POST.get("efirstname")
            edit.last_name = request.POST.get("elastname")
            edit.department = request.POST.get("edepartment")
            edit.company_name = request.user.company_name
            edit.id_college = request.POST.get("eid_college")
            edit.national_id = request.POST.get("enational_id")
            edit.age = request.POST.get("eage")
            if "eactive" in request.POST:
                edit.is_active = True
            else:
                edit.is_active = False
            edit.save()

    return render(request, 'admin/Manage_Student.html', context)


def deletestudent(request, id):
    getstud = StudentAccount.objects.get(id=id)
    getcountparnet = StudentAccount.objects.filter(parent_national_id=getstud.parent_national_id).count()
    if getcountparnet == 1:
        ParentAccount.objects.get(national_id=getstud.parent_national_id).delete()
    getstud.delete()
    return redirect("manage_Student")


def manage_parent(request):
    student_nat = StudentAccount.objects.filter(company_name=request.user.company_name)
    parent_nat = ParentAccount.objects.filter(national_id__in=[x.parent_national_id for x in student_nat])
    print(parent_nat)
    context = {
        "parent": parent_nat,
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/Manage_Parent.html', context)


def Statistics(request):
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/Statistics.html', context)


def settings(request):
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/settings.html', context)


def Request_instructor(request):
    if request.method == "POST":
        if "requestinst" in request.POST:
            requesr_inst = InstructorAccount.objects.get(username=request.POST['username'])
            requesr_inst.is_active = True
            requesr_inst.save()

    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
        "InstructorAccount": InstructorAccount.objects.filter(is_active=False)
    }
    return render(request, 'admin/Request_instructor.html', context)


def Request_Student(request):
    if request.method == "POST":
        if "requeststd" in request.POST:
            requesr_std = StudentAccount.objects.get(username=request.POST['username'])
            requesr_std.is_active = True
            requesr_std.id_college = request.POST['id_college']
            requesr_std.save()
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
        "StudentAccount": StudentAccount.objects.filter(is_active=False, id_college="")
    }
    return render(request, 'admin/Request_Student.html', context)


def profile_admin(request):
    context = {
        "Schedule_company": Schedule.objects.filter(company_name=request.user.company_name),
    }
    return render(request, 'admin/profile_admin.html', context)