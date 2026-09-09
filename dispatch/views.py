from datetime import date

from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CustomerForm,
    VehicleForm,
    EmployeeForm,
    JobForm,
    DispatchForm,
)
from .models import (
    Customer,
    Vehicle,
    Employee,
    Job,
    Dispatch,
)


def dashboard(request):
    today = date.today()

    context = {
        "customer_count": Customer.objects.count(),
        "today_jobs": Job.objects.filter(
            clean_date=today
        ).count(),
        "available_vehicles": Vehicle.objects.filter(
            status="可用"
        ).count(),
        "available_employees": Employee.objects.filter(
            available=True
        ).count(),
        "jobs": Job.objects.filter(
            clean_date=today
        ).select_related("customer"),
    }

    return render(
        request,
        "dispatch/dashboard.html",
        context
    )


def customer_list(request):
    return render(
        request,
        "dispatch/customer_list.html",
        {
            "customers": Customer.objects.all()
        }
    )


def customer_create(request):
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("customer_list")

    return render(
        request,
        "dispatch/form.html",
        {
            "title": "新增客戶",
            "form": form
        }
    )


def vehicle_list(request):
    return render(
        request,
        "dispatch/vehicle_list.html",
        {
            "vehicles": Vehicle.objects.all()
        }
    )


def vehicle_create(request):
    form = VehicleForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("vehicle_list")

    return render(
        request,
        "dispatch/form.html",
        {
            "title": "新增車輛",
            "form": form
        }
    )


def employee_list(request):
    return render(
        request,
        "dispatch/employee_list.html",
        {
            "employees": Employee.objects.all()
        }
    )


def employee_create(request):
    form = EmployeeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("employee_list")

    return render(
        request,
        "dispatch/form.html",
        {
            "title": "新增人員",
            "form": form
        }
    )


def job_list(request):
    return render(
        request,
        "dispatch/job_list.html",
        {
            "jobs": Job.objects.select_related("customer")
        }
    )


def job_create(request):
    form = JobForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("job_list")

    return render(
        request,
        "dispatch/form.html",
        {
            "title": "新增清潔案件",
            "form": form
        }
    )


def dispatch_list(request):
    dispatches = Dispatch.objects.select_related(
        "job",
        "job__customer",
        "vehicle",
        "driver",
        "cleaner",
    )

    return render(
        request,
        "dispatch/dispatch_list.html",
        {
            "dispatches": dispatches
        }
    )


def dispatch_create(request):
    form = DispatchForm(request.POST or None)

    if form.is_valid():
        obj = form.save()

        obj.job.status = "已派車"
        obj.job.save(update_fields=["status"])

        return redirect("dispatch_list")

    return render(
        request,
        "dispatch/form.html",
        {
            "title": "新增派車",
            "form": form
        }
    )


def dispatch_print(request, pk):
    obj = get_object_or_404(
        Dispatch.objects.select_related(
            "job",
            "job__customer",
            "vehicle",
            "driver",
            "cleaner",
        ),
        pk=pk
    )

    return render(
        request,
        "dispatch/dispatch_print.html",
        {
            "dispatch": obj
        }
    )


# =========================
# 會員註冊
# =========================

from django.contrib.auth.models import User
from .forms import CustomerRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            Customer.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                contact=form.cleaned_data["contact"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"]
            )

            return redirect("login")

    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )
