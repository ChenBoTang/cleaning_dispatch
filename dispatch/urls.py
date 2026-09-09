from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path("register/", views.register, name="register"),
    path("login/",auth_views.LoginView.as_view(template_name="registration/login.html"),
    name="login"
    ),

    path(
    "logout/",
    auth_views.LogoutView.as_view(),
    name="logout"
    ),



    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "customers/",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "customers/add/",
        views.customer_create,
        name="customer_create"
    ),

    path(
        "vehicles/",
        views.vehicle_list,
        name="vehicle_list"
    ),

    path(
        "vehicles/add/",
        views.vehicle_create,
        name="vehicle_create"
    ),

    path(
        "employees/",
        views.employee_list,
        name="employee_list"
    ),

    path(
        "employees/add/",
        views.employee_create,
        name="employee_create"
    ),

    path(
        "jobs/",
        views.job_list,
        name="job_list"
    ),

    path(
        "jobs/add/",
        views.job_create,
        name="job_create"
    ),

    path(
        "dispatch/",
        views.dispatch_list,
        name="dispatch_list"
    ),

    path(
        "dispatch/add/",
        views.dispatch_create,
        name="dispatch_create"
    ),

    path(
        "dispatch/<int:pk>/print/",
        views.dispatch_print,
        name="dispatch_print"
    ),
]
