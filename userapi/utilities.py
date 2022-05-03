from users.models import(
    SuperUserAccount, AdminAccount,
    InstructorAccount, StudentAccount,
    ParentAccount, Company, CompanyRequest
)


## search if username exists
def username_exists(username):
    
    if (
        SuperUserAccount.objects.filter(username=username).exists() or 
        AdminAccount.objects.filter(username=username).exists() or 
        InstructorAccount.objects.filter(username=username).exists() or
        StudentAccount.objects.filter(username=username).exists() or
        ParentAccount.objects.filter(username=username).exists()
    ):
        
        return True
    else:
        return False

## search if email exists
def email_exists(email):
    
    if (
        Company.objects.filter(contact_email=email).exists() or
        SuperUserAccount.objects.filter(email=email).exists() or
        AdminAccount.objects.filter(email=email).exists() or 
        InstructorAccount.objects.filter(email=email).exists() or
        StudentAccount.objects.filter(email=email).exists() or
        ParentAccount.objects.filter(email=email).exists()
    ):
        
        return True
    else:
        return False

## search if company_name exists
def company_name_exists(company_name):
    
    if Company.objects.filter(company_name=company_name).exists():
        
        return True
    else:
        return False

## search if company_email exists
def company_contact_email_exists(contact_email):
    
    if (
        Company.objects.filter(contact_email=contact_email).exists() or
        SuperUserAccount.objects.filter(email=contact_email).exists() or 
        AdminAccount.objects.filter(email=contact_email).exists() or 
        InstructorAccount.objects.filter(email=contact_email).exists() or
        StudentAccount.objects.filter(email=contact_email).exists() or
        ParentAccount.objects.filter(email=contact_email).exists()
    ):  
        return True
    else:
        return False