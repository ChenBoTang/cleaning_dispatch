from django.urls import path

from . import views

urlpatterns = [
    path("status/", views.esp32_status, name="esp32_status"),
    path("command/", views.esp32_command, name="esp32_command"),
    path("set-command/", views.set_esp32_command, name="set_esp32_command"),
    path("control/", views.esp32_control, name="esp32_control"),
    path("api/control/", views.esp32_api_control, name="esp32_api_control"),
    path("rfid/", views.rfid_check, name="rfid_check"),
]
