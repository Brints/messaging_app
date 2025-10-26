from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns a standardized JSON error response.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response format
        custom_response = {
            'status_code': response.status_code,
            'status': 'error',
            'message': get_error_message(response.data),
            'errors': format_errors(response.data),
        }
        return Response(custom_response, status=response.status_code)

    # Handle non-DRF exceptions
    return Response({
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'status': 'error',
        'message': 'An unexpected error occurred.',
        'errors': {'detail': str(exc)},
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_error_message(data):
    """Extract a user-friendly error message from the error data."""
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        # Get first error message from the dict
        for key, value in data.items():
            if isinstance(value, list):
                return value[0] if value else 'Validation error.'
            return str(value)
    elif isinstance(data, list):
        return data[0] if data else 'An error occurred.'
    return str(data)


def format_errors(data):
    """Format error data into a consistent structure."""
    if isinstance(data, dict):
        return {key: value if isinstance(value, list) else [value]
                for key, value in data.items()}
    elif isinstance(data, list):
        return {'detail': data}
    return {'detail': [str(data)]}
