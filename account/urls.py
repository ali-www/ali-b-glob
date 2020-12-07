from django.urls import path
from . import views
from .views import UserUpdateViews
from django.contrib.auth import views as auth_views
#from django.urls reverse_lazy

urlpatterns= [
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='page/login.html'),name='login'),
    path('settings/change_password/',auth_views.PasswordChangeView.as_view(template_name='page/change_password.html'),name='password_change'),
    path('settings/change_password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='page/change_password_done.html'),name='password_change_done'),
    path('account/',UserUpdateViews.as_view(),name='my_account'),
  
]                                                   