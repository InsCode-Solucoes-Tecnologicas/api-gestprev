from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, SaudeSerializer, UsuarioSerializer


class SaudeView(APIView):
    """Verificacao de vida usada pelo nginx/orquestrador."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(responses=SaudeSerializer)
    def get(self, request):
        return Response({"status": "ok"})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):
    """Entrega o cookie csrftoken para a SPA antes do login."""

    permission_classes = [AllowAny]

    @extend_schema(responses={204: None})
    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    """Login por sessao. CSRF exigido tambem para anonimo (o DRF so checa autenticado)."""

    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: UsuarioSerializer, 400: None})
    def post(self, request):
        dados = LoginSerializer(data=request.data)
        dados.is_valid(raise_exception=True)
        usuario = authenticate(
            request,
            username=dados.validated_data["username"],
            password=dados.validated_data["password"],
        )
        if usuario is None:
            return Response(
                {"detail": "Usuario ou senha invalidos."}, status=status.HTTP_400_BAD_REQUEST
            )
        login(request, usuario)
        return Response(UsuarioSerializer(usuario).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={204: None})
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EuView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=UsuarioSerializer)
    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)
