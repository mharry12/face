from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_location_from_ip
from rest_framework.permissions import AllowAny
from .serializers import AdminSignupSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, AdminSignupSerializer, LoginSerializer






class VideoClickView(APIView):
    def get(self, request, *args, **kwargs):
        location = get_location_from_ip(request)
        # Update view count or log the location
        return Response(location)



from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
    "user_id": user.id,
    "email": user.email,
    "username": user.username,
    "role": "creator",  # 👈 Add this line
    "access": str(refresh.access_token),
    "refresh": str(refresh)
}, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







from rest_framework.views import APIView
from rest_framework.response import Response
from face.models import FaceUser
from face.serializers import FaceUserSerializer
from rest_framework.permissions import IsAdminUser

class AdminFetchFaceData(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = FaceUser.objects.all()
        serializer = FaceUserSerializer(users, many=True)
        return Response(serializer.data)


class AdminSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Admin account created successfully!",
                "user_id": user.id,
                "full_name": user.username,
                "email": user.email,
                "role": user.role,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # ✅ Allow only creators and admins (based on boolean flags)
            if not user.is_creator and not user.is_staff:
                return Response({"detail": "Login restricted to creators and admins."},
                                status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": "admin" if user.is_staff else "creator"  # Optional, add role string
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ImagePost
from .serializers import ImagePostSerializer

class ImagePostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        images = ImagePost.objects.all().order_by('-uploaded_at')
        serializer = ImagePostSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImagePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# views.py - Add this view to your Django backend
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ipware import get_client_ip
import requests

@csrf_exempt
@require_http_methods(["GET", "POST"])
def track_visitor(request):
    try:
        # Handle POST or GET data extraction
        if request.method == "POST":
            data = json.loads(request.body)
        else:  # GET request
            data = request.GET.dict()

        # Get client IP
        client_ip, is_routable = get_client_ip(request)
        ip_address = data.get('ip_address') or client_ip

        # Get location data
        location_data = get_location_from_ip(ip_address)

        # Build tracking data
        tracking_data = {
            'content_id': data.get('content_id'),
            'action': data.get('action', 'view'),
            'ip_address': ip_address,
            'country': data.get('country') or (location_data.get('country') if location_data else None),
            'region': data.get('region') or (location_data.get('region') if location_data else None),
            'city': data.get('city') or (location_data.get('city') if location_data else None),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'referrer': request.META.get('HTTP_REFERER'),
            'timestamp': data.get('timestamp'),
            'shared_by_ip': data.get('shared_by_ip'),
            'shared_from_country': data.get('shared_from_country'),
            'shared_from_region': data.get('shared_from_region'),
            'shared_via': data.get('shared_via')
        }

        # Here you would save to your database
        print("Tracking data received:", tracking_data)

        return JsonResponse({'status': 'success', 'data': tracking_data})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": ip,
                "country": data.get("country_name"),
                "region": data.get("region"),
                "city": data.get("city")
            }
        return None
    except:
        return None