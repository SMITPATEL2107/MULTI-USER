from django.shortcuts import render
from .models import *
from random import randint
from .utils import * 

# Create your views here.
def page(request):
    return render(request,"app/registration.html")

def LoginPage(request):
    return render(request,"app/login.html")

def RegisterUser(request):
    try:
        if request.POST['role'] == 'doctor':
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirmpassword']
            gender = request.POST['gender']
            email = request.POST['email']
            speciality = request.POST['speciality']
            dateofbirth = request.POST['birthdate']
            city = request.POST['city']
            mobile = str(request.POST['phone'])

            user = User.objects.filter(email=email)
            if user:
                message = 'This email already exists'
                return render(request, 'app/registration.html', {'message': message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(
                        email=email, password=password, role=role, otp=otp)
                    newdoctor = Doctor.objects.create(user_id=newuser, firstname=firstname, lastname=lastname,
                                                      gender=gender, speciality=speciality, city=city, mobile=mobile, birthdate=dateofbirth)
                    email_subject="Account Verification Mail"
                    sendmail(email_subject,"mail_template",email,{'name':firstname,'otp':otp})               
                    return render(request, 'app/LOGIN.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request, 'app/registration.html', {'message': message})

        else:
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirm']
            gender = request.POST['gender']
            email = request.POST['email']
            dateofbirth = request.POST['birthdate']
            city = request.POST['city']
            mobile = str(request.POST['phone']) 
            user = User.objects.filter(email=email)
            if user:
                message = 'This email already exists'
                return render(request, 'app/registration.html', {'message': message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(
                        email=email, password=password, role=role, otp=otp)
                    newpatient = Patient.objects.create(
                        user_id=newuser, firstname=firstname, lastname=lastname, gender=gender, city=city, mobile=mobile, birthdate=dateofbirth)
                    return render(request, 'app/login.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request, 'app/registration.html', {'message': message})
    except User.DoesNotExist:
        message = 'This email already exists'
        return render(request, 'app/registration.html', {'message': message})


def LoginUser(request):
    if request.POST['role'] == 'doctor':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        print(user)
        if user[0]:
            if user[0].password == password and user[0].role == 'doctor':
                doctor = Doctor.objects.filter(user_id=user[0])
                request.session['email'] = user[0].email
                request.session['firstname'] = doctor[0].firstname
                request.session['role'] = user[0].role
                request.session['id'] = user[0].id

                return render(request,"app/home.html")
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request, "app/login.html", {'message': message})
        else:
            message = "user doesn't exist"
            return render(request, "app/login.html", {'message': message})

    if request.POST['role'] == 'patient':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        print(user)
        if user[0]:
            if user[0].password == password and user[0].role == 'patient':
                patient = Patient.objects.filter(user_id=user[0])
                request.session['email'] = user[0].email
                request.session['firstname'] = patient[0].firstname
                request.session['role'] = user[0].role
                request.session['id'] = user[0].id
                return render(request,"app/home.html")
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request, "app/login.html", {'message': message})
        else:
            message = "user doesn't exist"
            return render(request, "app/login.html", {'message': message})