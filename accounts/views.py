'''
    Viewset for accounts app that contains
        - Register View
        - Login View
    Both viewset can be used as template based and API's.
    In API call, one extra parameter must be present in header.
        `Accept: application/json`
'''
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .serializers import TokenSerializer, UserSerializer, LoginSerializer

# Get the JWT settings.
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# Get User Model
User = get_user_model()


class RegisterView(APIView):
    """
    GET/POST accounts/register/
    Viewset used for registeration.
    Required parameter:
        - username
        - email
        - password
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'accounts/register.html'
    success_url = 'login'
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.accepted_renderer.format == 'html':
            serializer = UserSerializer()
            return Response({'serializer': serializer})
        return Response({'success': False},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    if request.accepted_renderer.format == 'html':
                        return redirect('login')
                    data = {
                        'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                        'email': serializer.data.get('email', ''),
                        'success': True
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                return Response(
                    {"success": False},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                if request.accepted_renderer.format == 'html':
                    return render(
                        request,
                        'accounts/error.html',
                        {"error": serializer.user_check.message}
                    )
                return Response(
                    {"success": False, "msg": serializer.user_check.message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"success": False, "msg": e},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """
    GET/POST accounts/login/
    Viewset used for login.
    Required parameter:
        - email
        - password
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'accounts/login.html'
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer})

    def post(self, request, format='json'):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if request.accepted_renderer.format == 'html':
                return redirect('index')
            data = {
                'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                'email': email,
                'success': True
            }
            serializer = TokenSerializer(data=data)
            if serializer.is_valid():
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        if request.accepted_renderer.format == 'html':
                return redirect('login')
        else:
            return Response(
                {'msg': 'Email or Password not correct.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class IndexView(TemplateView):
    template_name = 'accounts/index.html'
