from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializers import UserSerializer


class VerifyTokenAPI(RetrieveAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
