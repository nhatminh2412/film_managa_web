from app.models import Employee, Partner

def authorize(f_email, f_password):
    print(f"Email: {f_email}, Password: {f_password}")
    acc = None
    try:    
        acc = Employee.objects.get(email=f_email, password=f_password)    
    except Employee.DoesNotExist:
        try:
            acc = Partner.objects.get(email=f_email, password=f_password)
        except Partner.DoesNotExist:
            acc = None
    return acc
    
