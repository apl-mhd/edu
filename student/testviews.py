from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User


class ExampleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        a = User.objects.first()
        print(a)
        token = Token.objects.get_or_create(user=a)
        print(token)

        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }

        return Response(content)
