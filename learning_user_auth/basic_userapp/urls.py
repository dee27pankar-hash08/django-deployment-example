from django.urls import path

from basic_userapp import views

from django.conf import settings

from django.conf.urls.static import static

#TEMPLATE URLS!
app_name = 'basic_userapp'

urlpatterns = [

    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
]


#urlpatterns = [  ... the rest of your URLconf goes here ... ]
