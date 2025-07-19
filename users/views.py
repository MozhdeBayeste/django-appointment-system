from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from .models import UserProfile 
from consultant.models import ConsultantProfile
from django.contrib.auth.hashers import check_password , make_password
import re


def is_logged(request):
    user_id = request.session.get("user_id")
    return UserProfile.objects.filter(id=user_id).exists() if user_id else False


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
            
            elif (len(password) < 8 or
                  not re.search(r"[a-zA-Z]", password) or      
                  not re.search(r"\d", password)): 
                msg = ("رمز عبور باید حداقل ۸ کاراکتر باشد و شامل حداقل یک حرف، "
                       "یک عدد باشد.")
            
            else:
                user = UserProfile.objects.create(
                    username=username,
                    password=make_password(password),  
                    phoneNumber=phonenumber
                )
                request.session["user_id"] = user.id
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
                request.session["user_id"] = user.id  
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
        
        user = UserProfile.objects.filter(id=request.session.get("user_id")).first()
        if not user:
            return render(request, 'users/update.html',{'msg':'کاربری پیدا نشد'})
            
        return render(request, 'users/update.html',{'user':user})
    
    def post(self,request):
        if not is_logged(request) :
            return redirect("login")
        
        user = UserProfile.objects.filter(id=request.session.get("user_id")).first()
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
        
        if password:
            if (len(password) < 8 or
                not re.search(r"[a-zA-Z]", password) or
                not re.search(r"\d", password)):
                    msg = ("رمز عبور باید حداقل ۸ کاراکتر باشد و شامل حداقل یک حرف، "
                            "یک عدد باشد.")
        if password != confirm_password:
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
            msg = "اطلاعات با موفقیت بروزرسانی شد"

        return render(request, 'users/update.html',{'user':user , 'msg':msg})