from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('login/', views.UserLogin, name='login'),
    path('signup/', views.UserSignup, name='signup'),
    path('logout/', views.UserLogout, name='logout'),
    path('contact-us', views.Contact_us, name='contact-us'),
]
