from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from dispatch.models import Dispatch
from device.models import RFIDCard
import json


esp32_command_state = {
    "device": "ESP32-001",
    "command": "OFF",
}


def esp32_status(request):
    return JsonResponse({
        "status": "online",
        "device": esp32_command_state["device"],
        "message": "ESP32 connected to Django",
    })


def esp32_command(request):
    return JsonResponse({
        "device": esp32_command_state["device"],
        "command": esp32_command_state["command"],
    })


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
            "device": esp32_command_state["device"],
            "command": esp32_command_state["command"],
            "message": "Command updated",
        })

    except json.JSONDecodeError:
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


@csrf_exempt
def esp32_api_control(request):

    if request.method == "GET":
        return JsonResponse({
            "device": esp32_command_state["device"],
            "command": esp32_command_state["command"],
        })

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            command = data.get("command")

            if command not in ["ON", "OFF"]:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid command"
                }, status=400)

            esp32_command_state["command"] = command

            return JsonResponse({
                "success": True,
                "device": esp32_command_state["device"],
                "command": esp32_command_state["command"],
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "error": "Invalid JSON"
            }, status=400)

    return JsonResponse({
        "success": False,
        "error": "Method not allowed"
    }, status=405)

@csrf_exempt
def rfid_check(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "POST required"
        }, status=405)

    try:
        data = json.loads(request.body)
        uid = data.get("uid")

        if not uid:
            return JsonResponse({
                "success": False,
                "error": "UID required"
            }, status=400)

        uid = uid.strip().upper()

        print("收到 RFID:", uid)

        # ① 查詢 RFID 卡
        try:
            card = RFIDCard.objects.select_related("employee").get(
                uid=uid,
                active=True
            )
        except RFIDCard.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "未註冊的 RFID 卡",
                "can_leave": False
            })

        employee = card.employee

        # ② 取得今天日期
        today = timezone.localdate()

        # ③ 查詢今天的派車
        dispatches = Dispatch.objects.filter(
            job__clean_date=today,
            status__in=["已排程", "出發"]
        ).filter(
            Q(driver=employee) |
            Q(cleaner=employee)
        ).select_related("job", "vehicle")

        # ④ 今天沒有派車
        if not dispatches.exists():
            return JsonResponse({
                "success": True,
                "employee": employee.name,
                "employee_id": employee.id,
                "can_leave": False,
                "message": "今日沒有派車任務"
            })

        # ⑤ 找到派車
        dispatch = dispatches.first()

        vehicle = dispatch.vehicle.plate_no if dispatch.vehicle else None

        return JsonResponse({
            "success": True,
            "employee": employee.name,
            "employee_id": employee.id,
            "can_leave": True,
            "message": "今日有派車任務，允許取鑰匙",
            "job_no": dispatch.job.job_no,
            "vehicle": vehicle
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON"
        }, status=400)

