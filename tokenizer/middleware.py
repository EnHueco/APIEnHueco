__author__ = 'Diego'
from models import Token
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions
from rest_framework.views import APIView
class TokenAuthenticationMiddleware():

    def process_view(self, request, view_func, view_args, view_kwargs):

        login = request.POST['login']
        tokenValue = request.POST['token']

        try:
            token = Token.objects.get(value=tokenValue)
            if token.owner.login == login:
                return None
        except exceptions.ObjectDoesNotExist:
            # TOKEN not found
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except exceptions.MultipleObjectsReturned:
            # Many Tokens found
            tokens = Token.objects.query(value=tokenValue)
            for token in tokens:
                if token.owner.login == login:
                    return None
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)