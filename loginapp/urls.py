from django import views
from django.urls import path


from .views import signup, activate,login1 

urlpatterns = [  
    #path('', home, name = 'home'),  
    path('form/', signup, name = 'firstindex'),  
    # re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
    #     activate, name='activate'),  
    path('activate/<slug:uidb64>/<slug:token>/',activate, name='activate'),
    path('login1',login1,name = 'login1'),
]
