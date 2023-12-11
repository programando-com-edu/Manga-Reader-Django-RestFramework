from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from base.serializers import UserSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def post(self, request, *arg, **kwargs):
        data = request.data
        password = data.get('password')
        username = data.get('username')
        data.pop('username', None)
        data.pop('password', None)

        user = User.objects.create_user(username, password, **data)
        serialized_user = self.get_serializer(user)

        return Response(serialized_user.data, status=status.HTTP_201_CREATED)


class MeAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        instance = User.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)