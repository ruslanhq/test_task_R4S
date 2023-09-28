import json

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest

from apps.robots.utils import process_data


@csrf_exempt
def create_robot(request: HttpRequest) -> JsonResponse:
    """
    API endpoint that receives and processes information.

    Args:
        request (HttpRequest): HTTP request object.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            robot = process_data(data)
            return JsonResponse(
                {"message": "Robot successfully created."}, status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not supported."}, status=400)
