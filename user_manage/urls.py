
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


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
   




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
