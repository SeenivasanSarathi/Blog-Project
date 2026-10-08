from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('source/<slug:slug>/',views.detail,name='detail'),
    path('old_url/',views.olr_url_redirect,name='old'),
    path('new_url1/',views.new_url_view,name='new'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name = 'about'),
    path('register/',views.register,name = 'register'),
    path('login/',views.login,name = 'login'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('logout/',views.logout,name='logout'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('reset_password/<uidb64>/<token>/',views.reset_password,name='reset_password'),
    path('newpost/',views.newpost,name='newpost'),
    path('edit_post/<int:post_id>',views.edit_post,name='edit_post'),
    path('delete_post/<int:post_id>',views.delete_post,name='delete_post'),

]

