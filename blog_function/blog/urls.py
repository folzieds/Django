from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home ,name='blog_home'),
    path('about/',views.about, name='blog_about')
]