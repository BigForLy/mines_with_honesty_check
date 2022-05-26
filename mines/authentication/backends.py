import jwt
from datetime import datetime
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token.encode(
                'utf-8'), options={"verify_signature": False})
        except Exception:
            raise exceptions.AuthenticationFailed('Authentication error.')

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        if not payload.get('timestamp') or datetime.fromtimestamp(payload.get('timestamp')) < datetime.now():
            raise exceptions.AuthenticationFailed('Token expired')

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'This user has been deactivated')

        # Если token валидный записываем его пользователю, чтобы не пересоздавать новый token
        user.token = token

        return (user, token)

    def authenticate_header(self, request):
        return self.authentication_header_prefix
