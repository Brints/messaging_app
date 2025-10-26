from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers import CreateUserSerializer, UserSerializer, UserLoginSerializer, PasswordGenerateSerializer


def get_tokens_for_user(user):
    """Generate JWT tokens for a given authentication."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@swagger_auto_schema(
    method='post',
    request_body=CreateUserSerializer,
    responses={
        201: 'User created successfully with tokens.',
        400: 'Bad request.',
    },
    operation_description='Register a new authentication and obtain JWT tokens.',
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_and_get_tokens(request):
    """Create a new authentication and return JWT tokens."""

    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        return Response({
            'status_code': status.HTTP_201_CREATED,
            'status': 'success',
            'message': 'User created successfully.',
            'authentication': user_data,
            'tokens': tokens,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={
        200: 'Login successful with tokens.',
        400: 'Bad request.',
    },
    operation_description='Authenticate authentication and obtain JWT tokens.',
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user_and_get_tokens(request):
    """Authenticate authentication and return JWT tokens."""

    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['authentication']
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        return Response({
            'status_code': status.HTTP_200_OK,
            'status': 'success',
            'message': 'Login successful.',
            'authentication': user_data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=PasswordGenerateSerializer,
    responses={
        200: 'Strong password generated successfully.',
        400: 'Bad request.',
    },
    operation_description='Generate a strong random password.',
    tags=['Users']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_strong_password(request):
    """Generate a strong random password."""

    serializer = PasswordGenerateSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.save()
        return Response({
            'status_code': status.HTTP_200_OK,
            'status': 'success',
            'message': 'Strong password generated successfully.',
            'password': password,
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
