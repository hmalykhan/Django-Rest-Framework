from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            refresh = RefreshToken.for_user(account)
            # return Response({"data":serializer.data, "Token":Token.objects.get_or_create(user=account)[0].key})   #Normal Token generation
            return Response({"data":serializer.data, "Token":{"refresh":str(refresh),"access":str(refresh.access_token)}}) #JWT Token generation for new user
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@authentication_classes( [TokenAuthentication])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    