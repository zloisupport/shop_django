from .views import test_view
from django.urls import path, include
urlpatterns = [
    path('',test_view,name='base')
]
