from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse
from .models import ConsultantProfile ,AvailableTime
from users.models import UserProfile
from django.contrib.auth.hashers import check_password , make_password
from django.contrib import messages
import re
from django.db.models import Q
from datetime import datetime, timedelta
from appointments.models import Appointment
from django.utils.timezone import now


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

            fullname = request.POST.get('full_name')
            password = request.POST.get('password')
            phonenumber = request.POST.get('phone_number')
            confirm_password = request.POST.get("confirm_password")


            if not (fullname and password and phonenumber):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
            
            elif ConsultantProfile.objects.filter(phoneNumber=phonenumber).exists():
                msg = ' شماره تلفن قبلا استفاده شده است'
            
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
                consultant=ConsultantProfile.objects.create(
                    fullName=fullname,
                    password=make_password(password),  
                    phoneNumber=phonenumber
                )
                request.session["consultant_id"] = consultant.id
                msg = 'حساب کاربری با موفقیت ایجاد شد'
            
            return render(request, 'consultant/reg.html', {'msg': msg})

        elif act and act.strip() == "ورود":

            phonenumber = request.POST.get('check_phone_number')
            password = request.POST.get('check_password')
            if not (phonenumber and password):
                msg = 'لطفا تمامی فیلد ها را پر کنید'
                return render(request, 'consultant/reg.html', {'msg': msg})

            consultant = ConsultantProfile.objects.filter(phoneNumber=phonenumber).first()

            if consultant and check_password(password, consultant.password):
                request.session["consultant_id"] = consultant.id  
                request.session.modified = True
                messages.success(request, "عملیات با موفقیت انجام شد.")
                return redirect('consultant_dashboard')

            return render(request, 'consultant/reg.html', {'msg': 'شماره تلفن / رمز عبور نادرست است'})

        else:
        #return redirect() error page
            return HttpResponse('Invalid form submission')


class ConsultantUpdateView(View):
    def get(self,request):
        if not is_logged(request) :
            return redirect("consultant_login")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        if not consultant:
            return render(request, 'consultant/update.html',{'msg':'کاربری پیدا نشد'})     
        return render(request, 'consultant/update.html',{'Consultant':consultant})
    
    def post(self,request):
        if not is_logged(request) :
            return redirect("consultant_login")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        if not consultant:
            msg='کاربری پیدا نشد'

        fullname= request.POST.get("full_name")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phone_number")
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

        elif email !=  consultant.email and ConsultantProfile.objects.filter(email=email).exists():
            msg="این ایمیل قبلاً استفاده شده است."

        elif phonenumber !=  consultant.phoneNumber and ConsultantProfile.objects.filter(phoneNumber=phonenumber).exists():
            msg="این شماره تماس قبلاً استفاده شده است."

        else:
            consultant.fullName=fullname
            consultant.email = email
            consultant.phoneNumber = phonenumber
            consultant.specialty = specialty
            
            if password:
                consultant.password = make_password(password)

            consultant.save()
            messages.success(request, "عملیات با موفقیت انجام شد.")
            return redirect('consultant_dashboard')

        return render(request, 'consultant/update.html',{'consultant':consultant , 'msg':msg})
    

class AddAvailableTimeView(View):
    def get(self, request):
        if not is_logged(request) :
            return redirect("consultant_login")
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()
        return render(request, 'consultant/addAvailableTime.html', {'consultant': consultant})

    def post(self, request):
        if not is_logged(request) :
            return redirect("consultant_login")
        
        consultant = ConsultantProfile.objects.filter(id=request.session.get("consultant_id")).first()

        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        slot_duration = int(request.POST.get("slot_duration"))
        note = request.POST.get("note")

        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        slots = []
        current = start_dt
        while current + timedelta(minutes=slot_duration) <= end_dt:
            slots.append((current, current + timedelta(minutes=slot_duration)))
            current += timedelta(minutes=slot_duration)

        for start, end in slots:
            AvailableTime.objects.create(
                consultant=consultant,
                startTime=start,
                endTime=end,
                note=note
            )

        msg = f"{len(slots)} نوبت با موفقیت ایجاد شد."
        return render(request, "consultant/addAvailableTime.html", {"msg": msg})
    

    
class ConsultantProfileView(View):
    def get(self, request, pk):
        consultant = ConsultantProfile.objects.filter(id=pk , isActive=True).first()
        if not consultant:
            return render(request, 'consultant/consultantProfile.html', {'msg': 'مشاوری یافت نشد'})
        return render(request, 'consultant/consultantProfile.html', {'consultant': consultant})
    
class ConsultantDashboardView(View):
    def get(self, request):
        if not is_logged(request):
            return redirect("consultant_login")

        consultant_id = request.session.get('consultant_id')
        consultant =ConsultantProfile.objects.filter(id=consultant_id).first()
        if not consultant:
            return render(request, 'consultant/dashboard.html', {'msg':'مشاوری یافت نشد'})

        return render(request, 'consultant/dashboard.html', {'fullname':consultant.fullName})
    
class ConsultantListView(View):
    def get(self,request):
        if not is_logged(request):
            return redirect("consultant_login")
        query = request.GET.get('q')
        consultants = ConsultantProfile.objects.all()

        if query:
            consultants = consultants.filter(Q(fullName__icontains=query) | Q(specialty__icontains=query))

        consultants = consultants[:24]
        return render(request,'consultant/consultantList.html',{'consultants':consultants})
    
def filter_appointments_by_time(qs, filter_type):
    today = now().date()
    if filter_type == 'today':
        return qs.filter(startTime__date=today)
    elif filter_type == 'week':
        week_later = today + timedelta(days=7)
        return qs.filter(startTime__date__range=(today, week_later))
    elif filter_type == 'month':
        month_later = today + timedelta(days=30)
        return qs.filter(startTime__date__range=(today, month_later))
    return qs

    
class AvailableTimeListView(View):
    def get(self, request):
        if not is_logged(request):
            return redirect("consultant_login")
        
        consultant_id = request.session.get('consultant_id')
        filter_type = request.GET.get("filter")
        times = AvailableTime.objects.filter(consultant_id=consultant_id, isActive=True)

        if filter_type:
            times = filter_appointments_by_time(times, filter_type)

        return render(request, 'consultant/availableTimes.html', {'available_times': times,'filter': filter_type})
    
    def post(self,request):
        if not is_logged(request):
            return redirect("consultant_login")
        
        act=request.POST.get("act")
        if act == 'حذف':
            time_id=request.POST.get("time_id")
            time=AvailableTime.objects.filter(id=time_id).first()
            if time:
                time.delete()
        return redirect("consultant_available_times")
            
class AppointmentListView(View):
    def get(self, request):
        if not is_logged(request):
            return redirect("consultant_login")

        consultant_id = request.session.get('consultant_id')
        filter_type = request.GET.get("filter")
        appointments = Appointment.objects.filter(consultant_id=consultant_id)

        if filter_type:
            appointments = filter_appointments_by_time(appointments, filter_type)

        return render(request, 'consultant/appointments.html', {'appointments': appointments,'filter': filter_type})
