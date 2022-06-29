from django.urls import path

from mechat import views
from . import views

urlpatterns = [
    path('',views.index,name = "index"),
]

