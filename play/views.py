from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .urls import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth import login,logout
from django.utils.encoding import force_bytes,force_str
from django.views.decorators.csrf import csrf_exempt
from .token import gen
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from django.utils import timezone
from web import settings
def home(request):
     return render(request,'main/Welcome.html') 
def dash(request):
          if request.user.is_authenticated:
               return render(request,'main/dash.html')
          else:
               return redirect('signin')
          
          
def signin(request):
       if request.method == 'POST':

          username=request.POST['username']
          password=request.POST['password']
          user=authenticate(username=username,password=password)
          if user is not None:
               login(request,user)
               f=user.first_name
               #return  render((request),'main/dash.html',{'fn':f})
               return redirect("dash")
          else:
               messages.error(request,"Enter correct Credentials")
               return redirect("signin")
            
    
       return render(request,'main/Sign_in.html') 
      
def signup(request):
     if request.method=="POST":
          username=request.POST['username']
          firstname=request.POST['firstname']
          lastname=request.POST['lastname']
          email=request.POST['email']
          password=request.POST['password']
          confirmpassword=request.POST['confirmpassword']
          if User.objects.filter(username=username).exists():
               messages.error(request,"Username already exist!")
               return redirect('signup')
          if User.objects.filter(email=email).exists():
               messages.error(request,"Email already exist!")
               return redirect('signup')
          if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
          if password !=confirmpassword:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
          if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
          user=User.objects.create_user(username,email,password)
          user.first_name=firstname
          user.last_name=lastname
          user.is_active=False
          user.save()

          messages.success(request,"Your Account details has been taken, To activate Account verify your email id")
          sub="Welcome to Our Website"
          message='Hello '+user.first_name+" ! \n\n"+'Welcome Thank You for visiting our website \n We have sent you a another conformation mail to verify your email id.\n          Thanking you\n Team OP'
          from_email=settings.EMAIL_HOST_USER
          to_email=[user.email]
          send_mail(sub,message,from_email,to_email,fail_silently=True)
          curr_site=get_current_site(request)
          email_sub="Confirm your Email "
          mess=render_to_string('main/email_confirmation.html',
                                {'name':user.first_name,
                                 'domain':curr_site.domain,
                                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                 'token':gen.make_token(user)}
                                 )
          email=EmailMessage(
               email_sub,
               mess,
               settings.EMAIL_HOST_USER,
               [user.email],

          )
          
          email.send(fail_silently=True)

          return redirect("signin")
     return render(request,"main/Sign_up.html")
def signout(request):
     logout(request)
     return redirect('home')
     
def activate(request,uidb64,token):
     try:
          uid=force_str(urlsafe_base64_decode(uidb64))
          user=User.objects.get(pk=uid)
     except (TypeError,ValueError,OverflowError,User.DoesNotExist):
          user=None
     if user is not None and gen.check_token(user,token):
          user.is_active=True
          user.save()
          login(request,user)
          messages.success(request,"Your Account Successfully created")
          return redirect('signin')
     else:
          messages.success(request,"Activation Failed")
          return redirect('signup')
def todo(request):
     if request.user.is_authenticated:
               todo_items=To_do.objects.filter(user=request.user).order_by("-add_date")
               return render(request,'main/todolist.html',{"todo_items":todo_items}) 
     else:
               return redirect('signin')
@csrf_exempt
def add_todo(request):
     if request.user.is_authenticated:
               current_date=timezone.now()
               data=request.POST['data']
               user=request.user
               created_obj=To_do.objects.create(add_date=current_date,text=data,user=user)
               return redirect("todo")
               
     else:
               return redirect('signin')
     
@csrf_exempt
def add_notes(request):
     current_date=timezone.now()
     text=request.POST['notes']
     user=request.user
     new_ob=Note.objects.create(add_date=current_date,text=text,user=user)
     return redirect('notes')
def notes(request):
     notes_list=Note.objects.filter(user=request.user).order_by("-add_date")
     return render(request,'main/Note.html',{'notes_list':notes_list})
def edit_notes(request,notes_text,notes_id):
     var=notes_text
     Note.objects.get(id=notes_id).delete()
     return render(request,'main/Note.html',{'var':var})
def edit_notes_after(request,notes_text):
      current_date=timezone.now()
      text=request.POST['notes']
      user=request.user
      new_ob=Note.objects.create(add_date=current_date,text=text,user=user)
      return redirect('notes')

def delete_notes(request,notes_id):
     Note.objects.get(id=notes_id).delete()
     return redirect('notes')
def delete_todo(request,todo_id):
     To_do.objects.get(id=todo_id).delete()
     return redirect("todo")
def deleteall(request):
     user=request.user
     user_todo_items = To_do.objects.filter(user=user)
     user_todo_items.delete()
     return redirect("todo")
def track(request):
     if request.user.is_authenticated:
       from phonenumbers import timezone
       if request.method=='POST':
          number=request.POST['phone-input']
          ch_number=phonenumbers.parse(number,'CH')
          c_name=geocoder.description_for_number(ch_number,'en')
          t_zone=phonenumbers.parse(number)
          time_zone=timezone.time_zones_for_number(t_zone)
          service_number=phonenumbers.parse(number,'R0')
          s_name = carrier.name_for_number(service_number,'en')
          return render(request,'main/tracknumber.html',{'cn':c_name,'tz':time_zone,'sn':s_name})
                
     else:
               return redirect('signin')
     return render(request,'main/tracknumber.html')
     
def square_run(request):
     if request.user.is_authenticated:
               return render(request,'main/squarerun.html')
               
     else:
               return redirect('signin')
def contact(request):
      return HttpResponse('Any Queries! Call : +917569127271 \n.Please Go Back to Home Page')
@csrf_exempt
def forget(request):
     
     if (request.method=="POST"):
           username=request.POST['username']
           password=request.POST['new_password']
           new= SetPasswordForm(user=request.user, data=request.POST)
           messages.success(request,"Your Account Password Has changed,Please SignIn")
           return redirect('signin')
     return render(request,'main/forget.html')