from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_profile",
        verbose_name="會員帳號"
    )


    name = models.CharField("客戶名稱", max_length=100)
    contact = models.CharField("聯絡人", max_length=100, blank=True)
    phone = models.CharField("電話", max_length=30, blank=True)
    address = models.CharField("地址", max_length=255, blank=True)
    note = models.TextField("備註", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "客戶"
        verbose_name_plural = "客戶"

    def __str__(self):
        return self.name


class Vehicle(models.Model):

    STATUS_CHOICES = [
        ("可用", "可用"),
        ("維修中", "維修中"),
        ("停用", "停用"),
    ]

    plate_no = models.CharField(
        "車號",
        max_length=30,
        unique=True
    )

    name = models.CharField(
        "車輛名稱",
        max_length=100
    )

    vehicle_type = models.CharField(
        "車型",
        max_length=50,
        blank=True
    )

    status = models.CharField(
        "狀態",
        max_length=20,
        choices=STATUS_CHOICES,
        default="可用"
    )

    note = models.TextField(
        "備註",
        blank=True
    )

    def __str__(self):
        return f"{self.plate_no} - {self.name}"


class Employee(models.Model):

    name = models.CharField(
        "姓名",
        max_length=100
    )

    phone = models.CharField(
        "電話",
        max_length=30,
        blank=True
    )

    position = models.CharField(
        "職位",
        max_length=50,
        default="清潔人員"
    )

    available = models.BooleanField(
        "可派遣",
        default=True
    )

    note = models.TextField(
        "備註",
        blank=True
    )

    def __str__(self):
        return self.name


class Job(models.Model):

    STATUS_CHOICES = [
        ("待處理", "待處理"),
        ("已派車", "已派車"),
        ("進行中", "進行中"),
        ("已完成", "已完成"),
        ("取消", "取消"),
    ]

    job_no = models.CharField(
        "案件編號",
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        verbose_name="客戶"
    )

    clean_date = models.DateField(
        "清潔日期"
    )

    clean_time = models.TimeField(
        "清潔時間"
    )

    address = models.CharField(
        "清潔地址",
        max_length=255
    )

    clean_type = models.CharField(
        "清潔類型",
        max_length=100,
        default="一般清潔"
    )

    status = models.CharField(
        "狀態",
        max_length=20,
        choices=STATUS_CHOICES,
        default="待處理"
    )

    note = models.TextField(
        "備註",
        blank=True
    )

    def __str__(self):
        return self.job_no


class Dispatch(models.Model):

    STATUS_CHOICES = [
        ("已排程", "已排程"),
        ("出發", "出發"),
        ("完成", "完成"),
        ("取消", "取消"),
    ]

    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        verbose_name="案件"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="車輛"
    )

    driver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_dispatches",
        verbose_name="司機"
    )

    cleaner = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cleaner_dispatches",
        verbose_name="清潔人員"
    )

    departure_time = models.DateTimeField(
        "出發時間",
        null=True,
        blank=True
    )

    return_time = models.DateTimeField(
        "返回時間",
        null=True,
        blank=True
    )

    status = models.CharField(
        "派車狀態",
        max_length=20,
        choices=STATUS_CHOICES,
        default="已排程"
    )

    note = models.TextField(
        "備註",
        blank=True
    )

    def __str__(self):
        return f"{self.job.job_no} 派車"
