from django.urls import path
from .views import CreateUserView, MeAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('me/', MeAPIView.as_view(), name='my_user'),
    path('create-user/', CreateUserView.as_view(), name='create-user-api'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]