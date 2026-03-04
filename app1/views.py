from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Turf,Booking
from .forms import UserRegisterForm, UserLoginForm,AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import Turf, Booking  
from .forms import BookingForm 


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = UserRegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        form = UserLoginForm()  
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)  
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Hai, {user.username}")   
            return redirect("home")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out.")
        return redirect("home")

class HomeView(View):
    template_name="home.html"
    def get(self, request):
        sport=request.GET.get("sport")
        district=request.GET.get("district")

        turfs = Turf.objects.all()
        if sport:
            turfs = turfs.filter(sport=sport)
        if district:
            turfs = turfs.filter(district=district)

        # pass distinct choices for selects (so template can render)
        sport_choices = [c[0] for c in Turf._meta.get_field('sport').choices]
        district_choices = [c[0] for c in Turf._meta.get_field('district').choices]

        context = {
            "turfs": turfs,
            "sport_choices": sport_choices,
            "district_choices": district_choices,
            "selected_sport": sport or "",
            "selected_district": district or "",
        }
        return render(request, self.template_name, context)

class TurfDetailView(View):
    template_name = "turf_detail.html"
    def get(self, request, pk):
        turf = get_object_or_404(Turf, pk=pk)
        return render(request, self.template_name, {"turf": turf})


@method_decorator(login_required, name='dispatch')
class BookingTurf(View):
    def get(self, request, pk, *args, **kwargs):
        turf = get_object_or_404(Turf, pk=pk)
        form = BookingForm(initial={
            'user': request.user,
            'turf': turf,
            'date': datetime.today().date(),
            'start_time': '06:00',  # default start time
            'end_time': '07:00',    # default end time (1 hour later)
        })
        return render(request, 'booking_form.html', {'form': form, 'turf': turf})

    def post(self, request, pk, *args, **kwargs):
        turf = get_object_or_404(Turf, pk=pk)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.turf = turf
            booking.save()

            # Send email confirmation
            subject = 'Turf Booking Confirmation'
            message = (
                f"Hi {request.user.username},\n\n"
                f"Your booking for {turf.name} is confirmed.\n"
                f"Date: {booking.date}\n"
                f"Time: {booking.start_time} to {booking.end_time}\n\n"
                f"Thank you for using our service!"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

            messages.success(request, 'Booking successful! Confirmation sent to your email.')
            return redirect('home')  
        else:
            return render(request, 'booking_form.html', {'form': form, 'turf': turf})

class getMyorder(View):
    def get(self,request,*args,**kwargs):
        # user=request.user
        orders=Booking.objects.filter(user=request.user)
        return render(request,"myorders.html",{'orders':orders})

class DeleteBook(View):
    def get(self,request,*args,**kwargs):
        order_id=Booking.objects.get(id=kwargs.get("pk"))
        order_id.delete()
        subject = 'Turf Booking Confirmation'
        message = (
            f"Hi {request.user.username},\n\n"
            f" Your Booking deleted!"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )           
        messages.success(request, 'Your Booked slot is cancelled')
        return redirect('cart')  