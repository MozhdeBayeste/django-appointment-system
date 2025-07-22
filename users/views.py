from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.urls import reverse
from .models import UserProfile 
from consultant.models import ConsultantProfile ,AvailableTime
from appointments.models import Appointment
from django.contrib.auth.hashers import check_password , make_password
from django.contrib import messages
from django.utils.timezone import now
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
            phonenumber = request.POST.get('phone_number')
            confirm_password = request.POST.get("confirm_password")


            if not (username and password and phonenumber):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
            
            elif UserProfile.objects.filter(username=username).exists() or UserProfile.objects.filter(phoneNumber=phonenumber).exists():
                msg = 'نام کاربری / شماره تلفن قبلا استفاده شده است'
            
            if password:
                if (len(password) < 8 or
                    not re.search(r"[a-zA-Z]", password) or
                    not re.search(r"\d", password) or
                    not re.search(r"[؟،!\\\-+=@#$]", password)):
                    msg = ("رمز عبور باید حداقل ۸ کاراکتر باشد و شامل حداقل یک حرف، "
                            "یک عدد و یک کاراکتر خاص مانند ؟ ، ! - + = @ # $ باشد.")

            if password != confirm_password:
                msg = "رمز عبور با تکرار آن مطابقت ندارد."
            
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

            username = request.POST.get('check_username')
            password = request.POST.get('check_password')

            if not (username and password):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
                return render(request, 'users/reg.html', {'msg': msg})

            user = UserProfile.objects.filter(username=username).first()

            if user and check_password(password, user.password):
                request.session["user_id"] = user.id  
                request.session.modified = True
                messages.success(request, "عملیات با موفقیت انجام شد.")
                return redirect("user_dashboard")
            return render(request, 'users/reg.html', {'msg': 'نام کاربری / رمز عبور نادرست است'})

        else:
        #return redirect() error page
            return HttpResponse('Invalid form submission')


class UserUpdateView(View):

    def get(self,request):
        if not is_logged(request) :
            return redirect("user_login")
        
        user = UserProfile.objects.filter(id=request.session.get("user_id")).first()
        if not user:
            return render(request, 'users/update.html',{'msg':'کاربری پیدا نشد'})
            
        return render(request, 'users/update.html',{'user':user})
    
    def post(self,request):
        if not is_logged(request) :
            return redirect("user_login")
        
        user = UserProfile.objects.filter(id=request.session.get("user_id")).first()
        if not user:
            msg='کاربری پیدا نشد'

        username= request.POST.get("username")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phone_number")
        fullname = request.POST.get("full_name")
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
            user.fullName = fullname 
            if password:
                user.password = make_password(password)

            user.save()
            messages.success(request, "عملیات با موفقیت انجام شد.")
            return redirect("user_dashboard")

        return render(request, 'users/update.html',{'user':user , 'msg':msg})

class UserDashboardView(View):
    def get(self, request):
        if not is_logged(request):
            return redirect("user_login")
        user =UserProfile.objects.filter(id=request.session.get('user_id')).first()
        if not user:
            return render(request, 'users/dashboard.html', {'msg':'کاربری یافت نشد'})

        return render(request, 'users/dashboard.html', {'username':user.username})
    
class UserAppointmentsView(View):
    def get(self, request):
        if not is_logged(request):
            return redirect("user_login")
        user = UserProfile.objects.get(id=request.session['user_id'])
        appointments = Appointment.objects.filter(user=user).select_related("availableTime", "consultant").order_by('-bookedAt')
        return render(request, 'users/userAppointments.html', {'appointments': appointments})


class ConsultantAvailableTimesView(View):
    def get(self, request, consultant_id):
        if not is_logged(request) :
            return redirect("user_login")
        consultant = ConsultantProfile.objects.filter(id=consultant_id).first()
        available_times = AvailableTime.objects.filter(consultant=consultant, isActive=True, startTime__gte=now()).order_by('startTime')
        return render(request, 'users/reservationList.html', {'consultant': consultant,'available_times': available_times})

    def post(self, request, consultant_id):
        if not is_logged(request) :
            return redirect("user_login")
        
        user = UserProfile.objects.filter(id=request.session.get('user_id')).first()
        consultant = ConsultantProfile.objects.filter(id=consultant_id).first()
        time_id = request.POST.get('time_id')
        available_time = AvailableTime.objects.filter(id=time_id, isActive=True).first()

        if not available_time:
            messages.error(request, 'این نوبت دیگر در دسترس نیست.')
            return redirect('reservation_list', consultant_id=consultant_id)

        future_appointments = Appointment.objects.filter(user=user,availableTime__startTime__gt=now()).count()

        if future_appointments >= 2:
            messages.warning(request, 'شما حداکثر دو نوبت فعال در آینده می‌توانید داشته باشید.')
            return redirect('reservation_list', consultant_id=consultant_id)
        
        Appointment.objects.create(
            user=user,
            consultant=consultant,
            availableTime=available_time,
        )
        available_time.isActive = False
        available_time.save()

        messages.success(request, 'نوبت شما با موفقیت رزرو شد.')
        return redirect('reservation_list', consultant_id=consultant_id)
