from sys import exception

from django.http import JsonResponse
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError
from rest_framework.decorators import api_view

def index(request):
    return JsonResponse({"message": "This is the user authentication microservice"})

@api_view(['GET'])
def check_if_user_exists(request):
    email = request.GET.get('email', None)
    if email is None:
        return JsonResponse({'message':'Please provide a email'}, status=400)
    else:
        try:
            user = auth.get_user_by_email(email)
            if user is not None:
                return JsonResponse({'message':'User exists'}, status=200)
        except UserNotFoundError as e:
            return JsonResponse({'message':'User does not exist'}, status=200)
        except exception as e:
            return JsonResponse({'message':e}, status=500)

