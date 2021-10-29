
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve 
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [

    path('', views.home, name="home"),
    path('register/',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('loginUser/', views.login_user, name='login_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('uploadFile/', views.uploadFile, name='uploadFile'),
    path('user_create/', views.user_create, name='user_create'),
    path('likepost/<int:id>', views.likepost, name='likepost'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('uploadExcelFile/', views.uploadExcelFile, name='uploadExcelFile'),
    path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    # rest API
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('upload_file/', views.upload_file),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
