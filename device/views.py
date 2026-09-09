from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


esp32_command_state = {
    "device": "ESP32-001",
    "command": "OFF"
}


def esp32_status(request):
    return JsonResponse({
        "status": "online",
        "device": "ESP32-001",
        "message": "ESP32 connected to Django"
    })


def esp32_command(request):
    return JsonResponse(esp32_command_state)


@csrf_exempt
def set_esp32_command(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "POST required"
        }, status=405)

    try:
        data = json.loads(request.body)
        command = data.get("command")

        if command not in ["ON", "OFF"]:
            return JsonResponse({
                "error": "command must be ON or OFF"
            }, status=400)

        esp32_command_state["command"] = command

        return JsonResponse({
            "device": "ESP32-001",
            "command": command,
            "message": "Command updated"
        })

    except Exception:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)


def esp32_control(request):
    return render(
        request,
        "device/esp32_control.html",
        {
            "device": esp32_command_state["device"],
            "command": esp32_command_state["command"],
        }
    )