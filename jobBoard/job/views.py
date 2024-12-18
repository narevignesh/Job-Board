from django.shortcuts import render
from .models import *
from random import randint
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
import requests
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages




# Create your views here.



def HomePage(request):
    return render(request, "app/home.html")

def IndexPage(request):
    return render(request, "app/index.html")

def CompanyPage(request):
    return render(request, "app/company/index.html")


def SignupPage(request):
    return render(request,"app/signup.html")

def RegisterUser(request):
    if request.POST['role'] == "Candidate":
        role = request.POST['role']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = UserMaster.objects.filter(email=email)
        
        if user:
            message = "user already exist"
            return render(request, "app/signup.html", {'msg': message})

        
        else:
            if password == confirm_password:
                otp = randint(10000,999999)
                newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                newcand = Candidate.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                return render(request,"app/login.html")
            
    elif request.POST['role'] == "Company":
        role = request.POST['role']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = UserMaster.objects.filter(email=email)
        
        if user:
            message = "user already exist"
            return render(request, "app/signup.html", {'msg': message})

        
        else:
            if password == confirm_password:
                otp = randint(10000,999999)
                newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                newcamp = Company.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                return render(request,"app/login.html",{"email" : email})
    
    else:
        print("done") 
        
def OtpPage(request):  
    return render(request,"app/otpverify.html")                 

def Otpverify(request):
    email = request.POST['email']
    otp = int(request.POST['otp'])

    try:
        user = UserMaster.objects.get(email=email)
        if user:
            if user.otp == otp:
                message = "Otp verified successfully"
                return render(request, "app/login.html", {'msg': message})
            else:
                message = "Otp is incorrect"
                return render(request, "app/otpverify.html", {'msg': message})
    except UserMaster.DoesNotExist:
        message = "User does not exist"
        return render(request, "app/signup.html", {'msg': message})
    
def LoginPage(request):
    return render(request,"app/login.html")    


def loginUser(request):
    if request.method == "POST":
        role = request.POST.get("role")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserMaster.objects.get(email=email)


            if role.lower() == "candidate" and user.role.lower() == "candidate":
                if user.password == password:
                    can = Candidate.objects.get(user_id=user)

                    request.session["id"] = user.id
                    request.session["role"] = user.role
                    request.session["firstname"] = can.firstname
                    request.session["lastname"] = can.lastname
                    request.session["email"] = user.email
                    request.session["password"] = user.password
                    return redirect("index")
                else:
                    msg = "Password does not match"
                    return render(request, "app/login.html", {"msg": msg})


            elif role.lower() == "company" and user.role.lower() == "company":
                if user.password == password:
                    comp = Company.objects.get(user_id=user)

                    request.session["id"] = user.id
                    request.session["role"] = user.role
                    request.session["firstname"] = comp.firstname
                    request.session["lastname"] = comp.lastname
                    request.session["email"] = user.email
                    request.session["password"] = user.password
                    return redirect("company")
                else:
                    msg = "Password does not match"
                    return render(request, "app/login.html", {"msg": msg})

            else:
                msg = "Invalid role selected"
                return render(request, "app/login.html", {"msg": msg})

        except UserMaster.DoesNotExist:
            msg = "User does not exist"
            return render(request, "app/login.html", {"msg": msg})
    

    return render(request, "app/login.html", {"msg": "Invalid request method"})

def Canpro(request,pk):
        user = UserMaster.objects.get(pk=pk)
        can = Candidate.objects.get(user_id=user)
        return render(request,"app/canpro.html",{'user':user,'can':can }) 
    
def UpdateCan(request, pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Candidate":
        can = Candidate.objects.get(user_id=user)
        can.state = request.POST.get('state')
        can.city = request.POST.get('city')
        can.education = request.POST.get('education')
        can.website = request.POST.get('website')
        can.contact = request.POST.get('contact')
        can.gender = request.POST.get('gender')
        can.address = request.POST.get('address')
        can.firstname = request.POST.get('firstname')
        can.lastname = request.POST.get('lastname')
        can.dob = request.POST.get('dob')
        can.save()
        url = f'/canpro/{pk}'
        return redirect(url)

    
           
def Comnpro(request,pk):
    user = UserMaster.objects.get(pk=pk)
    com = Company.objects.get(user_id=user)
    return render(request,"app/company/comnpro.html",{'user':user,'com':com })

def UpdateCom(request, pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Company":
        com = Company.objects.get(user_id=user)
        com.firstname = request.POST.get('firstname')
        com.lastname = request.POST.get('lastname')
        com.companyname = request.POST.get('company')
        com.website = request.POST.get('website')
        com.address = request.POST.get('address')
        com.contact = request.POST.get('contact')
        com.email = request.POST.get('email')
        com.state = request.POST.get('state')
        com.city = request.POST.get('city')
        com.save()
        url = f'/comnpro/{pk}'
        return redirect(url)

def post_job(request,pk):
    return render(request, "app/company/jobpost.html")

 
def post_job_submit(request,pk):
    user = UserMaster.objects.get(id=pk)
    if user.role == "Company":
        comp = Company.objects.get(user_id=user)
        name = request.POST['name']
        title = request.POST['title']
        description = request.POST['description']
        salary = request.POST['salary']
        experience = request.POST['experience']  
        website = request.POST['website']
        logo = request.FILES['logo']
        
        newjob = JobPost.objects.create(company_id=comp,title=title,description=description,salary=salary,experience=experience,website=website,logo=logo,name=name)
        
        msg = "Job posted successfully"
        return render(request, "app/company/jobpost.html", {'msg': msg})
    
def show_job_date(request, pk):
    user = UserMaster.objects.get(id=pk)
    com = Company.objects.get(user_id_id=user)
    company = com.id
    job_posts = JobPost.objects.all()
    return render(request, 'app/company/job_posted.html', {'job_posts': job_posts ,"company_id":company})

def job_update(request, id):
    job = JobPost.objects.get(id=id)
    return render(request, "app/company/edit_job.html", {"job": job})


def job_updated(request, id):
    if request.method == "POST":
        job = get_object_or_404(JobPost, id=id)
        job.name = request.POST.get('name', job.name)
        job.title = request.POST.get('title', job.title)
        job.description = request.POST.get('description', job.description)
        job.salary = request.POST.get('salary', job.salary)
        job.experience = request.POST.get('experience', job.experience)
        job.website = request.POST.get('website', job.website)
        if request.FILES.get('logo'):
            job.logo = request.FILES['logo']
        job.save()
        messages.success(request, "Job details updated successfully!")
        return redirect(reverse('jobupdate', args=[id]))
    return redirect(reverse('jobupdate', args=[id]))

def Delete_job(request, id, pk):
    job = get_object_or_404(JobPost, id=id)
    job.delete()
    messages.success(request, f"Job deleted successfully!")  
    return redirect('jobdata', pk=pk)

def job_list_candidate(request):
    jobs = JobPost.objects.all()
    return render(request, "app/job-list.html", {"jobs": jobs})

def job_Details(request,id):
    job = JobPost.objects.get(id=id)
    return render(request, "app/job-details.html", {"job": job})

def job_Application(request, id, num):
    return render(request, "app/job-application.html", {"id": id, "num": num})



def job_Apply(request, id, num):
    job_post = get_object_or_404(JobPost, id=id)
    company = Company.objects.get(id=num)

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')
        job_position = request.POST.get('job_position')

        # Get the logged-in user (optional)
        user = request.user if request.user.is_authenticated else None

        JobApplication.objects.create(
            company=company,
            job_post=job_post,
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            address=address,
            cover_letter=cover_letter,
            resume=resume,
            job_position=job_position,
            user=user  # Add the user field
        )
        msg = "Your job application has been submitted successfully!"
        return redirect(f'/job_details/{id}/?msg={msg}')

    
    return render(request, "app/job-application.html", {'job_post': job_post, 'id': id, 'num': num })

        


def logOut(request):
    del request.session["email"]
    del request.session["password"]
    return redirect("home")

 
