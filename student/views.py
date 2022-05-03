from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from schedule.models import StudentSchedule, MaterialVideo, InstructorSchedule, TaskInstructor, TaskStudent
from users.models import InstructorAccount, ExtraPermissions


def student_home(request):
    context = {
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
    }
    return render(request, "student/home.html", context)


def Schedule(request, Schedule_Name):
    ins_s = InstructorSchedule.objects.get(instructor_schedule_name=Schedule_Name).instructor_name

    inst_ext = ExtraPermissions.objects.get(user_have_perm=ins_s)
    li = (TaskStudent.objects.filter(std_schedule=Schedule_Name, std_company=request.user.company_name,
                                  std_username=request.user.username, ))
    lis = []

    for li in li:
        l = {"taskname": li.std_task_name, "degree_p": li.std_task_d * 10, "degree": li.std_task_d}
        lis.append(l)
    print(lis)

    context = {
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
        "ExtraPermissions": inst_ext,
        "ScheduleStudent": Schedule_Name,
        "ans_task": lis,
        # list(ans_task.objects.filter(std_schedule=Schedule_Name,std_company=request.user.company_name,std_username=request.user.username,))
    }
    return render(request, "student/schedule.html", context)


def Schedule_Material_video(request, Schedule_Name):
    context = {
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
        "Material_video": MaterialVideo.objects.filter(Schedule_name=Schedule_Name)
    }
    return render(request, "student/videomat.html", context)


def Schedule_task(request, Schedule_Name):
    if request.method == "POST":
        taskname = request.POST.get('itn')
        upload = request.FILES['uf']
        fs = FileSystemStorage()
        filename = fs.save(upload.name, upload)
        upload_url = fs.url(filename)
        print(upload.name.split('.')[-1])
        TaskStudent.objects.create(
            std_username=request.user.username,
            std_company=request.user.company_name,
            std_task_name=taskname,
            std_schedule=Schedule_Name,
            std_task_file=upload_url,
            std_task_d=0,
            is_download=True,
        ).save()
    context = {
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
        "ScheduleStudent": Schedule_Name,
        "task": TaskInstructor.objects.filter(Schedule_name=Schedule_Name, company_name=request.user.company_name),
        "ans_task": TaskStudent.objects.filter(std_schedule=Schedule_Name, std_company=request.user.company_name,
                                            std_username=request.user.username, )
    }
    return render(request, "student/task.html", context)