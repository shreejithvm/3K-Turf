from django.urls import path
from . import views
from .views import AdminBookingList, AdminBookingUpdate, AdminBookingDelete


urlpatterns = [
    path("", views.AdminLoginView.as_view(), name="admin_login"),
    path("dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),

    # turfs
    path("turfs/", views.TurfListView.as_view(), name="admin_turf_list"),
    path("turfs/add/", views.TurfCreateView.as_view(), name="admin_turf_add"),
    path("turfs/edit/<int:pk>/", views.TurfEditView.as_view(), name="admin_turf_edit"),
    path("turfs/delete/<int:pk>/", views.TurfDeleteView.as_view(), name="admin_turf_delete"),
    path('bookings/', AdminBookingList.as_view(), name='booking_list'),
    path('bookings/update/<int:pk>/', AdminBookingUpdate.as_view(), name='admin_booking_update'),
    path('bookings/delete/<int:pk>/', AdminBookingDelete.as_view(), name='admin_booking_delete'),
]
