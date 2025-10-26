from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.serializers import CreateUserSerializer, UserSerializer, UserLoginSerializer, \
    PasswordGenerateSerializer
from config.utils import ResponseUtils


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
    responses={201: 'User created successfully with tokens.', 400: 'Bad request.'},
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

        return ResponseUtils.success_response(
            message='User created successfully.',
            data={
                'user': user_data,
                'tokens': tokens,
            },
            status_code=status.HTTP_201_CREATED
        )

    # global exception handler takes care of validation errors
    return ResponseUtils.error_response(
        message='Validation failed.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={200: 'Login successful with tokens.', 400: 'Bad request.'},
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

        return ResponseUtils.success_response(
            message='Login successful.',
            data={
                'user': user_data,
                'tokens': tokens,
            },
            status_code=status.HTTP_200_OK
        )

    return ResponseUtils.error_response(
        message='Authentication failed.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@swagger_auto_schema(
    method='post',
    request_body=PasswordGenerateSerializer,
    responses={200: 'Strong password generated successfully.', 400: 'Bad request.'},
    operation_description='Generate a strong random password.',
    tags=['Users']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_strong_password(request):
    """Generate a strong random password."""
    serializer = PasswordGenerateSerializer(data=request.data)
    if serializer.is_valid():
        password_data = serializer.save()

        return ResponseUtils.success_response(
            message='Strong password generated successfully.',
            data=password_data,
            status_code=status.HTTP_200_OK
        )

    return ResponseUtils.error_response(
        message='Invalid request.',
        errors=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )
