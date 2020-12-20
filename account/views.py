from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from account.models import MyUser, MyUserManager
# Create your views here.
def indexView(request):
    return render(request,'index.html')

def dashboardView(request):
    return render(request,'dashboard.html')

def registerView(request):
    
    if request.method == "POST":
        email=request.POST['email']
        first_name=request.POST['first_name']
        name=request.POST['name']
        company_name=request.POST['company_name']
        phone=request.POST['phone']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if MyUser.objects.filter(email=email):
                messages.info(request,'email déja utilisé')
                return render(request,'registration/register.html')
            elif MyUser.objects.filter(company_name=company_name):
                messages.info(request,'nom de compagnie déja existante')
                return render(request,'registration/register.html')
            else:
                user=MyUser.objects.create_user(email=email,first_name=first_name,name=name,company_name=company_name,phone=phone,password=password1)
                user.save()
                return render(request,'dashboard.html')
                
        else:
            messages.info(request,'les mots de passe ne correspondent pas')
            return render(request,'registration/register.html')
    else:
        return render(request,'registration/register.html')    


def loginView(request):

    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            return render(request,'dashboard.html')
        else:
            messages.info(request,'Compte inexistant')
            return render(request,'registration/login.html')
    else:
        return render(request,'registration/login.html')
    
def logout(request):
    auth.logout(request)
    redirect('login')
