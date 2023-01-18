from django.urls import path
from .views import SignUp, SignIn, update_profile, logout

app_name='registration'

urlpatterns = [
    path('signup/', SignUp, name='signup'),
    path('signin/', SignIn, name='signin'),
    path('update_profile/', update_profile, name='update_profile'),
    path('logout/', logout, name='logout'),
]