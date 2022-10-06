from django.urls import path
from . import views


urlpatterns = [
    
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('', views.loginPage, name="login"),
    path('home/', views.home, name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('profile/<str:pk>/',views.userProfile,name="profile"),
    path('update-user',views.updateUser,name="update-user"),
    path('topics/', views.topicPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('prescriptions/', views.prescriptionPage, name="prescriptions"),
    path('upload-prescription/', views.uploadPrescription, name="upload-prescription"),
    path('delete-prescription/<str:pk>/',views.deletePrescription,name="delete-prescription"),

]   
