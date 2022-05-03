from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from schedule.models import Material, MaterialVideo, InstructorSchedule, TaskInstructor, TaskStudent, StudentSchedule, Schedule
from users.models import ExtraPermissions, StudentAccount
from django.urls import reverse


def Schedule_view(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    count_std = {
        "std": StudentSchedule.objects.filter(student_schedule_name=Schedule_Name).count(),
        "Material": MaterialVideo.objects.filter(Schedule_name=Schedule_Name).count(),
        "Material_slide": Material.objects.filter(Schedule_name=Schedule_Name).count(),
        "task": TaskInstructor.objects.filter(Schedule_name=Schedule_Name).count(),

    }
    print(count_std)
    context = {
        "Schedule_Name": Schedule_Name,
        "count_std": count_std,
        "Schedule_Name": Schedule_Name,
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),
    }
    return render(request, 'Instructor/ScheduleinStruector.html', context)


def instructor_home(request):
    if request.user.id is None:
        return redirect("home")

    context = {
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),

    }
    return render(request, 'Instructor/home.html', context)


def Schedule_home(request):
    context = {
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),

    }
    return render(request, 'Instructor/schedule_t.html', context)


def instructor_Material(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    if request.method == "POST":
        material_name = request.POST['name']
        upload = request.FILES['upload']
        if "choice" in request.POST and request.POST["choice"] == "addvideo":
            fs = FileSystemStorage()
            filename = fs.save("material/video/" + material_name + ".mp4", upload)
            upload_url = fs.url(filename)
            print(upload.name.split('.')[1])
            print(Schedule_Name)
            MaterialVideo.objects.create(
                material_name=material_name,
                lecture_video=upload_url,
                company_name=request.user.company_name,
                Schedule_name=Schedule_Name,
                material_is_link=False,
                lecture_video_link=None,
            ).save()
        elif "choice" in request.POST and request.POST["choice"] == "addSlide":

            fs = FileSystemStorage()
            filename = fs.save("material/slide/" + material_name + "." + upload.name.split('.')[-1], upload)
            upload_url = fs.url(filename)
            print(upload.name.split('.')[-1])
            print(Schedule_Name)
            Material.objects.create(

                material_name=material_name,
                slide=upload,
                company_name=request.user.company_name,
                Schedule_name=Schedule_Name,
            ).save()
    context = {
        "viwetask": TaskInstructor.objects.all(),
        "material": MaterialVideo.objects.filter(Schedule_name=Schedule_Name),
        "material_slide": Material.objects.filter(Schedule_name=Schedule_Name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),

        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),

    }
    return render(request, "Instructor/material.html", context)


def delete_material(request, Schedule_Name, id, type):
    if type == "Video":

        delete = MaterialVideo.objects.get(
            id=id,
            Schedule_name=Schedule_Name,

        )
        delete.delete()

    elif type == "slide":

        delete = Material.objects.get(
            id=id,
            Schedule_name=Schedule_Name,
        )
        delete.delete()
    return redirect(reverse("instructor_Material", kwargs={"Schedule_Name": Schedule_Name}))


def delete_task(request, Schedule_Name, id, type):
    if type == "task":
        delete = TaskInstructor.objects.get(
            id=id,
            Schedule_name=Schedule_Name,
        )
        delete.delete()

    return redirect(reverse("instructor_Task", kwargs={"Schedule_Name": Schedule_Name}))


def instructor_Task(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    if request.method == "POST":
        if "addtask" in request.POST and request.POST["addtask"] == "addtask":
            taskname = request.POST['name_task']
            upload = request.FILES['filetask']
            fs = FileSystemStorage()
            filename = fs.save("tasks/" + upload.name, upload)
            upload_url = fs.url(filename)
            print("tasks/" + upload.name.split('.')[1])
            TaskInstructor.objects.create(

                task_name=taskname,
                task_file=upload_url,
                company_name=request.user.company_name,
                Schedule_name=Schedule_Name,
            ).save()

    context = {
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),

        "instructor_Schedule": InstructorSchedule.objects.filter(instructor_name=request.user.username),
        "viwetask": TaskInstructor.objects.filter(Schedule_name=Schedule_Name),
    }
    return render(request, "Instructor/task.html", context)


def instructor_Schedule(request):
    if 'get' in request.GET:
        InstructorSchedule.objects.create(
            instructor_schedule_name=request.GET["instructor_schedule_name"],
            company_name=request.user.company_name,
            instructor_name=request.user.username,
        ).save()
        Schedule.objects.create(
            schedule_name=request.GET["Schedule_Name"],
            instructor_schedule_name=request.GET["instructor_schedule_name"],
            student_schedule_name=request.GET["student_schedule_name"],
            company_name=request.user.company_name,
            quiz_name=request.GET["quiz_name"],
            task_name=request.GET["task_name"],
            material_name=request.GET["material_name"],
            course_name=request.GET["course_name"],
            post_title=request.GET["post_title"],
        ).save()
        return JsonResponse({"state": True})
    context = {

    }
    return render(request, "Instructor/Schedule.html", context)


def view_Material(request):
    context = {
        "material": MaterialVideo.objects.all(),
        "material_slied": Material.objects.all(),
    }
    return render(request, 'Instructor/viewmateral.html', context)


def std_open_Schedule(request, Schedule_Name):
    StudentSchedulev = StudentSchedule.objects.filter(student_schedule_name=Schedule_Name)

    l = []
    for StudentSchedulev in StudentSchedulev:
        l.append(StudentAccount.objects.get(username=StudentSchedulev.student_name))
    print(l)
    context = {
        'StudentSchedule': StudentSchedule.objects.filter(student_schedule_name=Schedule_Name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),

        "instructor_Schedule": InstructorSchedule.objects.filter(instructor_name=request.user.username),
    }
    return render(request, 'Instructor/student_schedule.html', context)


def ViweTasks(request, Schedule_Name, username):
    print(Schedule_Name, username)
    _std_task = TaskStudent.objects.filter(std_username=username,
                                        std_schedule=Schedule_Name, std_task_d="0")
    if request.method == "POST":
        deg = TaskStudent.objects.get(std_username=username,
                                   std_schedule=Schedule_Name, std_task_name=request.POST.get('itn'))

        deg.std_task_d = int(request.POST.get('degree'))
        deg.save()
    context = {
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),
        "std_task": _std_task
    }
    return render(request, "Instructor/v_tasks.html", context)


def detet_task_ans(request, Schedule_Name, username, id):
    delete = TaskStudent.objects.get(
        id=id,
        std_schedule=Schedule_Name,
        std_username=username,
    )
    delete.delete()
    return redirect(reverse("ViweTasks", kwargs={"Schedule_Name": Schedule_Name, "username": username}))


def report(request, Schedule_Name, username):
    degreeAll = 0
    TaskdegreeAll = TaskStudent.objects.filter(std_schedule=Schedule_Name, std_username=username)
    print(TaskdegreeAll)
    for i in TaskdegreeAll:
        degreeAll += i.std_task_d
    print(degreeAll)
    context = {
        "reportTask": TaskStudent.objects.filter(std_schedule=Schedule_Name, std_username=username),
        "degreeAll": degreeAll,
        "instructor_Schedule": InstructorSchedule.objects.filter(instructor_name=request.user.username),
    }
    return render(request, "Instructor/report.html", context)


def Settings(r):
    context = {
        "instructor_Schedule": InstructorSchedule.objects.filter(instructor_name=r.user.username),
    }
    return render(r, "Instructor/Settings.html", context)