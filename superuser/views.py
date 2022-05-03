from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sites.shortcuts import get_current_site

from users.models import(
	AdminAccount, Company, SuperUserAccount, CompanyRequest,
    InstructorAccount, StudentAccount, ParentAccount
)


from userapi import utilities

from smtplib import SMTPException
import random, string

def super_user_login(request):
    if request.method == 'POST':
        get_username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        if SuperUserAccount.objects.filter(email=get_username_or_email).exists():

            user_email = SuperUserAccount.objects.get(email=get_username_or_email)
            user = authenticate(username=user_email.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('super-user-home')
            else:
                print('email not found')
                
        elif SuperUserAccount.objects.filter(username=get_username_or_email).exists():

            user_username = SuperUserAccount.objects.get(username=get_username_or_email)
            user = authenticate(username=user_username.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('super-user-home')
                
            else:
                print('username not found')
        
        else:
            print('username or email not found')
            
    return render(request, 'superuser/super_user_login.html', context={})
    
    
    
def super_user_home(request):
    return render(request, 'superuser/super_user_home.html', context={})


def super_user_company_requests(request):
    context = {}
    
    comapny_requests = CompanyRequest.objects.all()
    context['comapny_requests'] = comapny_requests
    
    if request.method == 'POST':
        
        company_name 		 = request.POST.get('company_name')
        number_of_admin 	 = request.POST.get('number_of_admin')
        number_of_instructor = request.POST.get('number_of_instructor')
        number_of_student 	 = request.POST.get('number_of_student')
        start 				 = request.POST.get('start')
        end 				 = request.POST.get('end')
        email 				 = request.POST.get('email')
        sign 				 = request.POST.get('sign')
        status 				 = request.POST.get('status')
        description			 = request.POST.get('description')
        company_id			 = request.POST.get('id')
        
        if status == 'approved':
            if utilities.email_exists(email=email):
                context['email_error'] = 'This email registred before!'
                
            elif utilities.company_name_exists(company_name=company_name):
                context['company_name_error'] = 'This email registred before!'
                
                
            elif utilities.company_contact_email_exists(contact_email=email):
                context['email_error'] = 'This email registred before!'
                
            else:
                
                try:
                    code = string.ascii_letters
                    for i in range(11):
                        code += str(i)
                    rd = random.choices(code, k=15)

                    link = reverse('login-view', kwargs={'company_name': company_name, 'type_user': 'admin'})
                    send_mail(
                            f'Hi you have now admin account for your company! {company_name}',
                            f'''
                            This account allows you to manage your company,
                            
                            
                            You can login with: 
                            username: {company_name+''.join(rd)}
                            password: {''.join(rd)}
                            
                            With link:
                            {'http://'+get_current_site(request).domain+link}
                            ''',
                            'bla@colon.com',
                            [email]
                        )
                    if sign == 'true':
                        sign = True
                    else:
                        sign = False
                    
                    user = AdminAccount.objects.create_user(
						username 	 = company_name+''.join(rd),
						email 	 	 = email,
						first_name 	 = 'f_name',
						last_name  	 = 'l_name',
						company_name = company_name,
						admin_type 	 = 'main',
					)
                    
                    Company.objects.create(
						company_name 		= user.company_name,
						admins_number 		= number_of_admin,
						instrauctors_number = number_of_instructor,
						students_number     = number_of_student,
						start				= start,
						end					= end,
						is_sign_up			= sign,
						contact_email		= email,
						description			= description,
					)
                    user.set_password(''.join(rd))
                    user.is_active = True
                    user.save()
                    
                    CompanyRequest.objects.get(id=company_id).delete()
					
                except SMTPException:
                    context['error_send_mail'] = 'Failed to create please try again.'
                    
        elif status == 'rejected':
            try:
                send_mail(
                            f'Hi {email}',
                            f'''
                            Sorry your requirements do not match,
                            try to make another request.
                            ''',
                            'bla@colon.com',
                            [email]
                        )
                CompanyRequest.objects.get(id=company_id).delete()

            except SMTPException:
                context['error_send_mail'] = 'Failed to create please try again.'
       
    return render(request, 'superuser/company_requests.html', context=context)

@csrf_exempt
def get_request_data(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        company_request = CompanyRequest.objects.get(id=id)
        return JsonResponse({
			'company_name' : company_request.company_name,
			'admin_num'    : company_request.admins_number,
			'ins_num' 	   : company_request.instrauctors_number,
			'stu_num' 	   : company_request.students_number,
			'start' 	   : company_request.start,
			'end' 		   : company_request.end,
			'sign_up' 	   : company_request.is_sign_up,
			'cont_email'   : company_request.contact_email,
			'status' 	   : company_request.status,
			'description'  : company_request.description,
			'id'		   : company_request.id
		})


def get_all_companies(request):
    all_companies = Company.objects.all()
    return render(request, 'superuser/companies.html', context={'all_companies': all_companies})

def del_company(request, id):
    del_id = Company.objects.get(id=id)
    del_id.delete()
    return redirect('all-companies')

def get_all_admins(request):
    all_companies = Company.objects.all()

    if not request.method == 'POST':
        all_admins = AdminAccount.objects.all()
        return render(request, 'superuser/admins.html', context={'all_admins': all_admins, 'all_companies': all_companies})
    else:
        co_name = request.POST.get('co_name')
        all_admins = AdminAccount.objects.filter(company_name=co_name)
        return render(request, 'superuser/admins.html', context={'all_admins': all_admins, 'all_companies': all_companies})


def del_admin(request, id):
    del_id = AdminAccount.objects.get(id=id)
    del_id.delete()
    return redirect('super-all-admins')


def get_all_instructor(request):
    all_companies = Company.objects.all()

    if not request.method == 'POST':
        instructors = InstructorAccount.objects.all()
        return render(request, 'superuser/instructors.html', context={'instructors': instructors, 'all_companies': all_companies})
    else:
        co_name = request.POST.get('co_name')
        instructors = InstructorAccount.objects.filter(company_name=co_name)
        return render(request, 'superuser/instructors.html', context={'instructors': instructors, 'all_companies': all_companies})

def del_instructor(request, id):
    InstructorAccount.objects.get(id=id).delete()
    return redirect('super-all-instructors')


def get_all_student(request):
    all_companies = Company.objects.all()

    if not request.method == 'POST':
        student = StudentAccount.objects.all()
        return render(request, 'superuser/student.html', context={'student': student, 'all_companies': all_companies})
    else:
        co_name = request.POST.get('co_name')
        student = StudentAccount.objects.filter(company_name=co_name)
        return render(request, 'superuser/student.html', context={'student': student, 'all_companies': all_companies})


def del_student(request, id):
    StudentAccount.objects.get(id=id).delete()
    return redirect('super-all-instructors')

def get_all_parent(request):
    parent = ParentAccount.objects.all()
    return render(request, 'superuser/parent.html', context={'parent': parent})


def del_parent(request, id):
    ParentAccount.objects.get(id=id).delete()
    return redirect('super-all-instructors')




