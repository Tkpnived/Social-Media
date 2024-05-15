from django.urls import path
from socialapp import views


urlpatterns = [
    path('',views.home,name="home"),
    path('reg', views.reg, name="reg"),
    path('register', views.register, name="register"),
    path('web', views.web, name="web"),
    path('loginusers', views.loginusers, name="loginusers"),
    path('search', views.search, name="search"),
    path('profile/<dataid>/<item>', views.profile, name="profile"),
    path('message/<dataid>', views.message, name="message"),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('person/<dataid>/<item>', views.person, name="person"),
    path('updbs/<dataid>/<item>', views.updbs, name="updbs"),
    path('follow/<dataid>/<item>', views.follow, name="follow"),
    path('likess/<dataids>/<items>', views.likess, name="likess"),
    path('postmessage/<dataid>', views.postmessage, name="postmessage"),
    path('logout', views.logout, name="logout"),
    path('edit/<dataids>', views.edit, name="edit"),
    path('update_image/<dataid>/<item>', views.update_image, name="update_image"),
    path('update_profile/<dataid>/<item>', views.update_profile, name="update_profile"),
    path('status/<dataid>', views.status, name="status"),
    path('addstatus', views.addstatus, name="addstatus"),
    path('foll/<dataid>/<item>', views.foll, name="foll"),
    path('followers/<dataid>/<item>', views.followers, name="followers"),
    path('mes/<dataid>', views.mes, name="mes"),

]