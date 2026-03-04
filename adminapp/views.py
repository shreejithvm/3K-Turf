from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from app1.models import Turf,Booking
from .forms import AdminLoginForm, TurfForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from app1.forms import BookingForm  # Or create a separate admin form




# Restrict non-staff
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("admin_login")

# ---------------- LOGIN ---------------------
class AdminLoginView(View):
    template_name = "adminapp/login.html"

    def get(self, request):
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return render(request, self.template_name, {"form": AdminLoginForm()})

    def post(self, request):
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            if user and user.is_staff:
                login(request, user)
                return redirect("admin_dashboard")
            messages.error(request, "Invalid admin email or password.")
        return render(request, self.template_name, {"form": form})


# ---------------- DASHBOARD ---------------------
class AdminDashboardView(StaffRequiredMixin, View):
    template_name = "adminapp/dashboard.html"

    def get(self, request):
        return render(request, self.template_name, {
            "turf_count": Turf.objects.count(),
            "booking_count": Booking.objects.count()
        })

# ---------------- TURF CRUD ---------------------
class TurfListView(StaffRequiredMixin, View):
    template_name = "adminapp/turf_list.html"

    def get(self, request):
        turfs = Turf.objects.all()
        return render(request, self.template_name, {"turfs": turfs})

class TurfCreateView(StaffRequiredMixin, View):
    template_name = "adminapp/turf_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": TurfForm()})

    def post(self, request):
        form = TurfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Turf added successfully")
            return redirect("admin_turf_list")
        return render(request, self.template_name, {"form": form})

class TurfEditView(StaffRequiredMixin, View):
    template_name = "adminapp/turf_form.html"

    def get(self, request, pk):
        turf = get_object_or_404(Turf, pk=pk)
        return render(request, self.template_name, {"form": TurfForm(instance=turf)})

    def post(self, request, pk):
        turf = get_object_or_404(Turf, pk=pk)
        form = TurfForm(request.POST, request.FILES, instance=turf)
        if form.is_valid():
            form.save()
            messages.success(request, "Turf updated.")
            return redirect("admin_turf_list")
        return render(request, self.template_name, {"form": form})

class TurfDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        turf = get_object_or_404(Turf, pk=pk)
        turf.delete()
        messages.info(request, "Turf deleted.")
        return redirect("admin_turf_list")



def is_admin(user):
    return user.is_staff or user.is_superuser

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminBookingList(View):
    def get(self, request):
        bookings = Booking.objects.select_related('user', 'turf').order_by('-date')
        return render(request, 'adminapp/booking_list.html', {'bookings': bookings})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminBookingUpdate(View):
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        form = BookingForm(instance=booking)
        return render(request, 'adminapp/booking_form.html', {'form': form, 'booking': booking})

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()

            # Send update email
            send_mail(
                subject='Your Turf Booking Was Updated',
                message=(
                    f"Hi {booking.user.username},\n\n"
                    f"Your booking for {booking.turf.name} has been updated.\n"
                    f"New Date: {booking.date}\n"
                    f"New Time: {booking.start_time} to {booking.end_time}\n\n"
                    f"Regards,\nAdmin Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.user.email],
                fail_silently=False,
            )

            messages.success(request, 'Booking updated and user notified.')
            return redirect('booking_list')
        return render(request, 'adminapp/booking_form.html', {'form': form, 'booking': booking})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminBookingDelete(View):
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        return render(request, 'adminapp/booking_confirm_delete.html', {'booking': booking})

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        # Send delete email before deletion
        send_mail(
            subject='Your Turf Booking Was Cancelled',
            message=(
                f"Hi {booking.user.username},\n\n"
                f"Your booking for {booking.turf.name} on {booking.date} "
                f"from {booking.start_time} to {booking.end_time} has been cancelled by the admin.\n\n"
                f"Regards,\nAdmin Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            fail_silently=False,
        )

        booking.delete()
        messages.success(request, 'Booking deleted and user notified.')
        return redirect('booking_list')
