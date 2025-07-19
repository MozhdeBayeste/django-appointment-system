from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from .models import ConsultantProfile ,AvailableTime
from users.models import UserProfile
from django.contrib.auth.hashers import check_password , make_password
from django.utils import timezone
import re


def is_logged(request):
    consultant_id = request.session.get("consultant_id")
    return ConsultantProfile.objects.filter(id=consultant_id).exists() if consultant_id else False

# 09123456789    secret-12345
class RegistrationView(View):

    def get(self, request):
        return render(request, 'consultant/reg.html')
    
    def post(self, request):
        act = request.POST.get("act")
        if act and act.strip() == "ثبت نام":

            fullname = request.POST.get('fullname')
            password = request.POST.get('password')
            phonenumber = request.POST.get('phoneNumber')

            if not (fullname and password and phonenumber):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
            
            elif ConsultantProfile.objects.filter(phoneNumber=phonenumber).exists():
                msg = ' شماره تلفن قبلا استفاده شده است'
            
            elif (len(password) < 8 or
                  not re.search(r"[a-zA-Z]", password) or      
                  not re.search(r"\d", password) or            
                  not re.search(r"[؟،!\\\-+=@#$]", password)): 
                msg = ("رمز عبور باید حداقل ۸ کاراکتر باشد و شامل حداقل یک حرف، "
                       "یک عدد و یک کاراکتر خاص مانند ؟ ، ! - + = @ # $ باشد.")
            
            else:
                consultant=ConsultantProfile.objects.create(
                    full_name=fullname,
                    password=make_password(password),  
                    phoneNumber=phonenumber
                )
                request.session["consultant_id"] = consultant.id
                msg = 'حساب کاربری با موفقیت ایجاد شد'
            
            return render(request, 'consultant/reg.html', {'msg': msg})

        elif act and act.strip() == "ورود":

            phonenumber = request.POST.get('chphonenumber')
            password = request.POST.get('chpassword')

            if not (phonenumber and password):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
                return render(request, 'consultant/reg.html', {'msg': msg})

            consultant = ConsultantProfile.objects.filter(phoneNumber=phonenumber).first()

            if consultant and check_password(password, consultant.password):
                request.session["consultant_id"] = consultant.id  
                request.session.modified = True
                #return redirect() main page
                return render(request, 'consultant/reg.html', {'msg': 'با موفقیت وارد شدید'}) 

            return render(request, 'consultant/reg.html', {'msg': 'نام / رمز عبور نادرست است'})

        else:
        #return redirect() error page
            return HttpResponse('Invalid form submission')


class ConsultantUpdateView(View):

    def get(self,request):
        if not is_logged(request) :
            return redirect("login_consultant")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        if not consultant:
            return render(request, 'consultant/update.html',{'msg':'کاربری پیدا نشد'})
            
        return render(request, 'consultant/update.html',{'Consultant':consultant})
    
    def post(self,request):
        if not is_logged(request) :
            return redirect("login_consultant")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        if not consultant:
            msg='کاربری پیدا نشد'

        fullname= request.POST.get("fullname")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phoneNumber")
        specialty = request.POST.get("specialty")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not (email and  fullname):
            msg = "لطفا فیلد های ضروری را پر کنید"

        if password:
            if (len(password) < 8 or
                not re.search(r"[a-zA-Z]", password) or
                not re.search(r"\d", password) or
                not re.search(r"[؟،!\\\-+=@#$]", password)):
                    msg = ("رمز عبور باید حداقل ۸ کاراکتر باشد و شامل حداقل یک حرف، "
                            "یک عدد و یک کاراکتر خاص مانند ؟ ، ! - + = @ # $ باشد.")

        if password != confirm_password:
            msg = "رمز عبور با تکرار آن مطابقت ندارد."
        
        elif password:
            if len(password) < 8 or re.search(r"[؟،!\-+=@#$]", password):
                msg = "رمز عبور نباید از هشت کارکتر کمتر و شامل کاراکترهای خاص مانند ؟ ، ! - + = @ # $ باشد."
            elif password != confirm_password:
                msg = "رمز عبور با تکرار آن مطابقت ندارد."

        elif email !=  consultant.email and ConsultantProfile.objects.filter(email=email).exists():
            msg="این ایمیل قبلاً استفاده شده است."

        elif phonenumber !=  consultant.phoneNumber and ConsultantProfile.objects.filter(phoneNumber=phonenumber).exists():
            msg="این شماره تماس قبلاً استفاده شده است."

        else:
            consultant.full_name=fullname
            consultant.email = email
            consultant.phoneNumber = phonenumber
            consultant.specialty = specialty
            
            if password:
                consultant.password = make_password(password)

            consultant.save()
            msg = "اطلاعات با موفقیت بروزرسانی شد"

        return render(request, 'consultant/update.html',{'consultant':consultant , 'msg':msg})
    


    

class AddAvailableTimeView(View):
    def get(self, request):
        if not is_logged(request) :
            return redirect("login_consultant")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        return render(request, 'consultant/addconsultantavailabletime.html', {'consultant': consultant})

    def post(self, request):
        if not is_logged(request) :
            return redirect("login_consultant")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        note = request.POST.get('note')

        msg = ""
        if start_time and end_time:
            if start_time >= end_time:
                msg = "زمان پایان باید بعد از زمان شروع باشد."
            else:
                AvailableTime.objects.create(
                    consultant=consultant,
                    start_time=start_time,
                    end_time=end_time,
                    note=note,
                    is_active=True
                )
                msg = "زمان با موفقیت ثبت شد."
        else:
            msg = "لطفاً تمام فیلدهای ضروری را پر کنید."

        return render(request, 'consultant/addconsultantavailabletime.html', {
            'consultant': consultant,
            'msg': msg
        })