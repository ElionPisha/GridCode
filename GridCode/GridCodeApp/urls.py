from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload.html', views.upload, name='upload'),
    path('index2.html', views.index, name='index2'),
    path('get_group/<slug:val>/', views.get_group, name='get_group')
]

