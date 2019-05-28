import bcrypt
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users, Jobs, Categories
from datetime import datetime

def index(request):
    if 'user_id' in request.session:
        return redirect("/loggedin")
    return render(request, "helper/index.html")

def register(request):
    if request.method == "POST":
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            Users.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
            request.session['first_name'] = request.POST["first_name"]
            request.session['last_name'] = request.POST["last_name"]
            request.session["user_id"] = Users.objects.filter(email=request.POST["email"]).values()[0]['id']
            messages.success(request, "User successfully registered")
            return redirect("/loggedin")

def login(request):
    if request.method == "POST":
        errors = Users.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            l = Users.objects.filter(email=request.POST["email"])
            if len(l) == 0:
                messages.error(request, "uncaught error in validator that has overrided email existence check")
                return redirect('/')
            elif len(l) > 1:
                messages.error(request, "invalid data which has caused a duplicate email account to appear")
                return redirect('/')
            else:
                m = l.values()[0]
                request.session['first_name'] = m['first_name']
                request.session['last_name'] = m['last_name']
                request.session['user_id'] = m['id']                
                messages.success(request, "User successfully logged on")
                return redirect("/loggedin")
        

def loggedin(request):
    if not 'user_id' in request.session:
        return redirect('/')
    jobs = Jobs.objects.exclude(assigned_to=request.session['user_id'])
    your_jobs = Jobs.objects.filter(assigned_to=request.session['user_id'])
     
    context = {
        'first_name': request.session['first_name'],
        'last_name' : request.session['last_name'],
        'user_id': request.session['user_id'],
        'your_jobs': your_jobs,
        'jobs' : jobs
    }

    return render(request, "helper/loggedin.html", context)

def logout(request):
    if not 'user_id' in request.session:
        return redirect("/")
    request.session.clear()
    return redirect("/")

def create_new(request):
    if not 'user_id' in request.session:
        return redirect("/")
    return render(request, "helper/create.html")



def create(request):
    if not 'user_id' in request.session:
        return redirect("/")
    if request.method == 'POST':
        errors = Users.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/create_new')
        else:
            user = Users.objects.get(id=request.session['user_id'])
            Jobs.objects.create(job=request.POST['title'],
            desc=request.POST['description'],
            location=request.POST['location'],
            user_in_job=user)

            new_job = Jobs.objects.get(user_in_job=user, 
            location=request.POST['location'],
            job=request.POST['title'],
            desc=request.POST['description']
            )



            category = ""
            if int(request.POST.get('recreational', "-1")) == 0:
                category += "recreational, "
            if int(request.POST.get('imaginary', "-1")) == 2:
                category += "imaginary, "              
            if int(request.POST.get("education", "-1")) == 1:
                category += "education, " 
            if request.POST.get("other", "") != "":
                category += str(request.POST.get('other', "")) + ", "

            if category != "":
                category = category[:-2]
            else:
                category = "None"

            
            Categories.objects.create(name=category, categories_in_job=new_job)

            return redirect('/loggedin')
        

def desc(request, job_id):
    if not 'user_id' in request.session:
        return redirect("/")

    job = Jobs.objects.get(id= job_id)

    print("____________________")
    print(Categories.objects.get(categories_in_job=job_id))
    print(Categories.objects.get(categories_in_job=job_id).name)
    print("_______________________")
    context = {
        "first_name" : request.session["first_name"],
        "last_name" : request.session["last_name"],
        "user_id" : request.session["user_id"],
        "job" : job,
        "created_by" : job.user_in_job.first_name,
        "categories" : Categories.objects.get(categories_in_job=job_id)
    }
    return render(request, "helper/description.html", context)

def edit(request, job_id):
    if not 'user_id' in request.session:
        return redirect("/")
    job = Jobs.objects.get(id=job_id)
    context = {
        "first_name" : request.session["first_name"],
        "last_name" : request.session["last_name"],
        "user_id" : request.session["user_id"],
        "job" : job,
    }    
    return render(request, "helper/edit.html", context)

def submitedit(request, job_id):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Users.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit/' + str(job_id))
        else:
            job = Jobs.objects.get(id=job_id)
            job.desc = request.POST['description']
            job.location = request.POST['location']
            job.job = request.POST['title']
            job.updated_at = datetime.now()
            job.save()
            return redirect("/loggedin")


def remove(request, job_id):
    if not 'user_id' in request.session:
        return  redirect('/')
    user = Users.objects.get(id=request.session["user_id"])
    job= Jobs.objects.get(id=job_id)
    job.delete()
    return redirect("/loggedin")

    

def giveup(request, job_id):
    if not 'user_id' in request.session:
        return redirect('/')
    job = Jobs.objects.get(id=job_id)
    job.assigned_to = -1
    job.save()
    return redirect("/loggedin")

def add(request, job_id):
    if not 'user_id' in request.session:
        return redirect('/')
    job = Jobs.objects.get(id = job_id)
    job.assigned_to = request.session['user_id']
    job.save()        
    return redirect("/loggedin")



#for testing
def delete(request):
    Jobs.objects.all().delete()
    Users.objects.all().delete()
    request.session.clear()  
    return redirect('/')  


