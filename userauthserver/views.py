from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User  # Assuming you are using Django's default User model

# Index endpoint: Verifies that the microservice is running
def index(request):
    return JsonResponse({"message": "This is the user authentication microservice"})

# Update password endpoint
@csrf_exempt
def update_password(request):
    if request.method == 'POST':  # Only allow POST requests
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            email = data.get('email')
            new_password = data.get('newPassword')

            # Validate inputs
            if not email or not new_password:
                return JsonResponse({"status": 400, "message": "Email and new password are required"}, status=400)

            # Find the user in the database by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"status": 404, "message": "User not found"}, status=404)

            # Update the user's password
            user.set_password(new_password)  # Use Django's built-in password hashing
            user.save()

            # Return a success response
            return JsonResponse({"status": 200, "message": "Password successfully updated"})

        # Handle invalid JSON input
        except json.JSONDecodeError as e:
            return JsonResponse({"status": 400, "message": f"Invalid JSON format: {str(e)}"}, status=400)

        # Handle unexpected errors
        except Exception as e:
            return JsonResponse({"status": 500, "message": f"Internal server error: {str(e)}"}, status=500)

    # If the request method is not POST
    return JsonResponse({"status": 405, "message": "Method not allowed. Use POST."}, status=405)
