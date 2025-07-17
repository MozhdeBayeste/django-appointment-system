from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from .models import UserProfile 
from consultant.models import ConsultantProfile
from django.contrib.auth.hashers import check_password , make_password
from django.forms.models import model_to_dict
import re


def is_logged(request):
    sess = request.session.get("user")
    if sess and "username" in sess:
        if UserProfile.objects.filter(username=sess["username"]).exists():
            return 1
    return 0

# user , 12345678
class RegistrationView(View):

    def get(self, request):
        return render(request, 'users/reg.html')
    
    def post(self, request):
        act = request.POST.get("act")
        if act and act.strip() == "ثبت نام":

            username = request.POST.get('username')
            password = request.POST.get('password')
            phonenumber = request.POST.get('phoneNumber')

            if not (username and password and phonenumber):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
            
            elif UserProfile.objects.filter(username=username).exists() or UserProfile.objects.filter(phoneNumber=phonenumber).exists():
                msg = 'نام کاربری / شماره تلفن قبلا استفاده شده است'
            
            elif len(password) < 8 or re.search(r"[؟،!\-+=@#$]", password):
                msg = "رمز عبور نباید از هشت کارکتر کمتر و شامل کاراکترهای خاص مانند ؟ ، ! - + = @ # $ باشد."
            
            else:
                UserProfile.objects.create(
                    username=username,
                    password=make_password(password),  
                    phoneNumber=phonenumber
                )
                msg = 'حساب کاربری با موفقیت ایجاد شد'
            
            return render(request, 'users/reg.html', {'msg': msg})

        elif act and act.strip() == "ورود":

            username = request.POST.get('chusername')
            password = request.POST.get('chpassword')

            if not (username and password):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
                return render(request, 'users/reg.html', {'msg': msg})

            user = UserProfile.objects.filter(username=username).first()

            if user and check_password(password, user.password):
                user_data = model_to_dict(user, fields=["username", "email", "fullname", "phoneNumber"])
                request.session["user"] = user_data
                request.session.modified = True
                #return redirect() main page
                return render(request, 'users/reg.html', {'msg': 'با موفقیت وارد شدید'}) 

            return render(request, 'users/reg.html', {'msg': 'نام کاربری / رمز عبور نادرست است'})

        else:
        #return redirect() error page
            return HttpResponse('Invalid form submission')


class UserUpdateView(View):

    def get(self,request):
        if not is_logged(request) :
            return redirect("login")
        user_data = request.session.get("user")
        user=UserProfile.objects.filter(username=user_data.get("username")).first()
        if not user:
            return render(request, 'users/update.html',{'msg':'کاربری پیدا نشد'})
            
        return render(request, 'users/update.html',{'user':user})
    
    def post(self,request):
        if not is_logged(request) :
            return redirect("login")
        user_data = request.session.get("user")
        user=UserProfile.objects.filter(username=user_data.get("username")).first()
        if not user:
            msg='کاربری پیدا نشد'

        username= request.POST.get("username")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phoneNumber")
        fullname = request.POST.get("fullname")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not (email and  fullname):
            msg = "لطفا فیلد های ضروری را پر کنید"
        elif username !=  user.username and UserProfile.objects.filter(username=username).exists():
            msg= "این نام کاربری قبلاً استفاده شده است."
        
        elif password:
            if len(password) < 8 or re.search(r"[؟،!\-+=@#$]", password):
                msg = "رمز عبور نباید از هشت کارکتر کمتر و شامل کاراکترهای خاص مانند ؟ ، ! - + = @ # $ باشد."
            elif password != confirm_password:
                msg = "رمز عبور با تکرار آن مطابقت ندارد."

        elif email !=  user.email and UserProfile.objects.filter(email=email).exists():
            msg="این ایمیل قبلاً استفاده شده است."

        elif phonenumber !=  user.phoneNumber and UserProfile.objects.filter(phoneNumber=phonenumber).exists():
            msg="این شماره تماس قبلاً استفاده شده است."

        else:
            user.username=username
            user.email = email
            user.phoneNumber = phonenumber
            user.fullname = fullname 
            if password:
                user.password = make_password(password)

            user.save()
            request.session["user"].update({
                "username": username,
                "email": email,
                "phoneNumber": phonenumber,
                "fullname": fullname
            })
            msg = "اطلاعات با موفقیت بروزرسانی شد"

        return render(request, 'users/update.html',{'user':user , 'msg':msg})