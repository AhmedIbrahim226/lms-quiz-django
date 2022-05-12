import random
import re
import string
from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from .models import (
    AdminAccount, Company, InstructorAccount,
    StudentAccount, ParentAccount,
    SuperUserAccount, CompanyRequest
    )
from userapi import utilities
from django.http import JsonResponse


def make_request(request):
    context = {}
    if request.method == 'POST':
        company_name         = request.POST.get('company_name')
        number_of_admin      = request.POST.get('number_of_admin')
        number_of_instructor = request.POST.get('number_of_instructor')
        number_of_student    = request.POST.get('number_of_student')
        start                = request.POST.get('start')
        end                  = request.POST.get('end')
        description          = request.POST.get('description')
        email                = request.POST.get('email')
        is_signup            = request.POST.get('is_signup')
        
        if utilities.company_name_exists(company_name=company_name):
            context['error_company_name'] = 'This company allready registered!'
        elif utilities.company_contact_email_exists(contact_email=email):
            context['error_company_email'] = 'This email allready registered!'
        else:
            if is_signup is not None:
                # print(is_signup)
                is_signup = True
            else:
                is_signup = False
                # print('not_sign')
            print(is_signup)
            print(start)
            print(end)
            
            CompanyRequest.objects.create(
                company_name=company_name,
                admins_number=number_of_admin,
                instrauctors_number=number_of_instructor,
                students_number=number_of_student,
                start=start,
                end=end,
                is_sign_up=is_signup,
                contact_email=email,
                description=description,
            )
            context['success_request'] = 'The check o your request may take a few minutes or days, so be prepared for our notifications!'
            
        
        
        
    return render(request, 'users/make_request.html', context=context)
    

def home_view(request):
    return render(request, 'users/home_view.html', context={})


def become_partener_home(request):
    return render(request, 'users/become_partner_home.html', {})
    
def type_view(request, *args, **kwargs):
    company_name = kwargs['company_name']
    return render(request, 'users/type_view.html', context={'company_name': company_name})


def login_view(request, company_name, type_user):
    if_company_sign = Company.objects.get(company_name=company_name)

    parent_type = False
    if type_user == 'parent':
        parent_type = True

    context = {
        'if_company_sign': if_company_sign.is_sign_up,
        'company_name': company_name,
        'if_parent_type': parent_type,
        'type_user': type_user
    }

    if request.method == 'POST':

        get_username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        if type_user == 'admin':
            if AdminAccount.objects.filter(email=get_username_or_email).exists():

                user_check = AdminAccount.objects.get(email=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('admin with email logined')

                        login(request, user)
                        return redirect("home_admin")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'email or password not correct!'
                    print('email or password not correct!')

            elif AdminAccount.objects.filter(username=get_username_or_email).exists():

                user_check = AdminAccount.objects.get(username=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('admin logined')
                        login(request, user)
                        return redirect("home_admin")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'username or password not correct!'
                    print('username or password not correct!')

            else:
                context['error_login'] = 'Can\'t login, you are\'t admin!'
                print('Can\'t login, you are\'t admin!')

        elif type_user == 'doctor':
            if InstructorAccount.objects.filter(email=get_username_or_email, instructor_type=type_user).exists():

                user_check = InstructorAccount.objects.get(email=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('doctor with email logined')
                        login(request, user)
                        return redirect("instructor_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'email or password not correct!'
                    print('email or password not correct!')

            elif InstructorAccount.objects.filter(username=get_username_or_email, instructor_type=type_user).exists():

                user_check = InstructorAccount.objects.get(username=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('doctor logined')
                        login(request, user)
                        return redirect("instructor_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'username or password not correct!'
                    print('username or password not correct!')

            else:
                context['error_login'] = 'Can\'t login, you are\'t doctor!'
                print('Can\'t login, you are\'t doctor!')

        elif type_user == 'assistant':
            if InstructorAccount.objects.filter(email=get_username_or_email, instructor_type=type_user).exists():

                user_check = InstructorAccount.objects.get(email=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('assistant with email logined')
                        login(request, user)
                        return redirect("instructor_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'email or password not correct!'
                    print('email or password not correct!')

            elif InstructorAccount.objects.filter(username=get_username_or_email, instructor_type=type_user).exists():

                user_check = InstructorAccount.objects.get(username=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('assistant logined')
                        login(request, user)
                        return redirect("instructor_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'username or password not correct!'
                    print('username or password not correct!')


            else:
                context['error_login'] = 'Can\'t login, you are\'t assistant!'
                print('Can\'t login, you are\'t assistant!')

        elif type_user == 'trainer':
            if InstructorAccount.objects.filter(email=get_username_or_email, instructor_type=type_user).exists():

                user_check = InstructorAccount.objects.get(email=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('trainer with email logined')
                        login(request, user)
                        return redirect("instructor_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'email or password not correct!'
                    print('email or password not correct!')

            elif InstructorAccount.objects.filter(username=get_username_or_email, instructor_type=type_user).exists():

                user_check = InstructorAccount.objects.get(username=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('trainer logined')
                        login(request, user)
                        return redirect("instructor_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'username or password not correct!'
                    print('username or password not correct!')

            else:
                context['error_login'] = 'Can\'t login, you are\'t trainer!'
                print('Can\'t login, you are\'t trainer!')

        elif type_user == 'student':
            if StudentAccount.objects.filter(email=get_username_or_email).exists():

                user_check = StudentAccount.objects.get(email=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('student with email logined')
                        login(request, user)
                        return redirect("student_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'email or password not correct!'
                    print('email or password not correct!')

            elif StudentAccount.objects.filter(username=get_username_or_email).exists():

                user_check = StudentAccount.objects.get(username=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('student logined')
                        login(request, user)
                        return redirect("student_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'username or password not correct!'
                    print('username or password not correct!')

            else:
                context['error_login'] = 'Can\'t login, you are\'t student!'
                print('Can\'t login, you are\'t student!')

        elif type_user == 'parent':
            if ParentAccount.objects.filter(email=get_username_or_email).exists():

                user_check = ParentAccount.objects.get(email=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('parent with email logined')
                        login(request, user)
                        return redirect("parent_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'email or password not correct!'
                    print('email or password not correct!')
            elif ParentAccount.objects.filter(username=get_username_or_email).exists():

                user_check = ParentAccount.objects.get(username=get_username_or_email)
                user = authenticate(username=user_check.username, password=password)

                if user is not None:
                    if user.company_name == company_name:
                        print('parent logined')
                        login(request, user)
                        return redirect("parent_home")
                    else:
                        context['error_login'] = 'You can\'t login in this company'
                        print('You can\'t login in this company')
                else:
                    context['error_login'] = 'username or password not correct!'
                    print('username or password not correct!')

            else:
                context['error_login'] = 'Can\'t login, you are\'t parent!'
                print('Can\'t login, you are\'t parent!')

    return render(request, 'users/login.html',
                  context=context)


def sign_up_instructor_view(request, *args, **kwargs):
    company_name = kwargs['company_name']
    type_user = kwargs['type_user']

    context = {'company_name': company_name, 'type_user': type_user}

    if request.method == 'POST':
        if type_user == 'doctor' or type_user == 'assistant' or type_user == 'trainer':
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            department = request.POST.get("department")

            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if utilities.username_exists(username=username):
                context['error'] = 'This username exists!'

            elif utilities.email_exists(email=email):
                context['error'] = 'This email exists!'

            expert_password = re.findall("[a-zA-Z]", password)
            if len(password) < 8:
                context['error'] = 'Your password must contain at least 8 characters.'
            elif not expert_password:
                context['error'] = 'Your password can’t be entirely numeric.'
            elif confirm_password != password:
                context['error'] = 'Your passwords not same!.'

            else:
                user = InstructorAccount.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    department=department,
                    company_name=company_name,
                    instructor_type=type_user,
                )
                user.set_password(confirm_password)
                user.is_active = False
                user.save()

                context['success'] = 'Your account created, wait your admin to activate your account.'

    return render(request, 'users/sign_up_instructor.html', context=context)


def sign_up_student_view(request , *args, **kwargs):
    type_user = kwargs['type_user']
    company_name = kwargs['company_name']

    context = {}
    context['company_name'] = company_name
    context['type_user'] = type_user

    if request.method == 'POST':

        if type_user == 'student':
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            department = request.POST.get("department")
            gender = request.POST.get("gender")
            age = request.POST.get("age")
            national_id = request.POST.get("national_id")
            parent_national_id = request.POST.get("parent_national_id")
            parent_email = request.POST.get("parent_email")

            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if utilities.username_exists(username=username):
                context['username_error'] = 'This username exists!'

            elif utilities.email_exists(email=email):
                context['email_error'] = 'This email exists!'

            expert_password = re.findall("[a-zA-Z]", password)

            if len(password) < 8:
                context['error_pass'] = 'Your password must contain at least 8 characters.'
            elif not expert_password:
                context['error_pass'] = 'Your password can’t be entirely numeric.'
            elif confirm_password != password:
                context['error_pass'] = 'Your passwords not same!.'

            else:
                try:
                    user = StudentAccount.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        company_name=company_name,
                        department=department,
                        gender=gender,
                        age=age,
                        national_id=national_id,
                        parent_national_id=parent_national_id
                    )

                    if ParentAccount.objects.filter(national_id=parent_national_id).exists():
                        user.set_password(confirm_password)
                        user.is_active = False
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
                        user.set_password(confirm_password)
                        user.is_active = False
                        user.save()

                        user_parent.set_password(''.join(rd))
                        user_parent.is_active = False
                        user_parent.save()

                        context['success'] = 'Your account created, wait your admin to activate your account.'




                except SMTPException:
                    context['error_send_mail'] = 'Failed to create please try again.'
    return render(request, 'users/sign_up_student.html', context=context)


def companies_view(request):
    companies = Company.objects.all()
    return render(request, 'users/companies_view.html', context={'companies': companies})

        

def logout_view(request):
    logout(request)
    return redirect('home')