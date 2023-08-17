from django.contrib import admin
from django.urls import path
from Home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout")
]
