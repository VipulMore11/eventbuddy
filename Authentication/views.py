from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from .models import *


@api_view(['POST'])
@permission_classes([AllowAny])
def register_organiser_view(request):
    serializer = OrganiserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        organiser, created = Organiser.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': str(organiser.role)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_staff_view(request):
    user_serializer = StaffSerializer(data=request.data)

    if user_serializer.is_valid():
        user = user_serializer.save() 
        staff, created= Staff.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': str(staff.role)
        }, status=status.HTTP_201_CREATED)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        mutable_data = request.data.copy()
        email = mutable_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        mutable_data['username'] = user.username
        serializer = LoginSerializer(data=mutable_data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data
            try:
                staff = Staff.objects.get(user=user)
                role = staff.role
            except Staff.DoesNotExist:
                try:
                    org = Organiser.objects.get(user=user)
                    role = org.role
                except Organiser.DoesNotExist:
                    role = None
            refresh = RefreshToken.for_user(user)
            response = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': str(role)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_view(request):
        try :
            user = request.user
            try:
                userprofile = Organiser.objects.get(user=user)
            except Organiser.DoesNotExist:
                try:
                    userprofile = Staff.objects.get(user=user)
                except Staff.DoesNotExist:
                    return Response({'message': 'User Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = GetProfileSerializer(userprofile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Organiser.DoesNotExist :
            return Response('No Profile Found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)