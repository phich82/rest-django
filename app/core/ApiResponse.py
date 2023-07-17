from rest_framework import status as HttpStatus
from rest_framework.response import Response


class ApiResponse:
    """Api Response Class"""

    @staticmethod
    def success(data=None, status: int = HttpStatus.HTTP_200_OK, message: any = '', headers=None) -> Response:
        """Success response

        Args:
            data (any): Returned data
            status (int): Code status. Default as 200
            message (string, array, object,...): Success message

        Returns:
            Response: Response
        """
        return Response(data={
            'success': True,
            'message': message,
            'data': data,
        }, status=status, content_type='application/json;charset=utf-8', headers=headers)

    @staticmethod
    def error(message: any ='', status: int = HttpStatus.HTTP_400_BAD_REQUEST, headers=None) -> Response:
        """Error response

        Args:
            message (string, array, object): Error message
            status (int): Code status. Default as 400

        Returns:
            Response: Response
        """
        return Response(data={
            'success': False,
            'error_message': message,
            'data': None,
        }, status=status, content_type='application/json;charset=utf-8', headers=headers)
