from django.contrib import admin

from .models import (
    Customer,
    Vehicle,
    Employee,
    Job,
    Dispatch,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "contact",
        "phone",
        "address",
    )

    search_fields = (
        "name",
        "contact",
        "phone",
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "plate_no",
        "name",
        "vehicle_type",
        "status",
    )

    list_filter = (
        "status",
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "position",
        "available",
    )

    list_filter = (
        "available",
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "job_no",
        "customer",
        "clean_date",
        "clean_time",
        "clean_type",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "job_no",
        "customer__name",
        "address",
    )


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):

    list_display = (
        "job",
        "vehicle",
        "driver",
        "cleaner",
        "status",
    )

    list_filter = (
        "status",
    )
