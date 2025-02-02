from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import OutstandingToken

from user.serializers import UserSerializer
from rest_framework.decorators import action


# Create your views here.
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permissions_classes = ()


class ManageUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        OutstandingToken.objects.filter(user=request.user).update(
            blacklisted=True
        )
        return Response(status=status.HTTP_205_RESET_CONTENT)


# @api_view(['POST'])
# def logout(request):
#     tokens = OutstandingToken.objects.filter(user=request.user)
#     for token in tokens:
#         token, _ = BlacklistedToken.objects.get_or_create(token=token)
#     return Response(status=status.HTTP_205_RESET_CONTENT)
