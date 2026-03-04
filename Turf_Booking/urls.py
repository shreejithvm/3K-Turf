"""
URL configuration for Turf_Booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from app1 import views as user_views
from adminapp import views as admin_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),

    #  User side
    path("", user_views.HomeView.as_view(), name="home"),
    path("register/", user_views.RegisterView.as_view(), name="register"),
    path("login/", user_views.LoginView.as_view(), name="login"),

        path("password_reset/", 
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
         name="password_reset"),
    path("password_reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
         name="password_reset_complete"),


    
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
    path("turf/<int:pk>/", user_views.TurfDetailView.as_view(), name="turf_detail"),
    # path("add-to-cart/<int:slot_id>/", user_views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", user_views.getMyorder.as_view(), name="cart"),
    path('book/<int:pk>/',user_views.BookingTurf.as_view(), name='book_turf'),
    path('delete/book/<int:pk>/',user_views.DeleteBook.as_view(), name='book_delete'),
    # Admin side 
    path("admin-panel/", include("adminapp.urls")),

   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
