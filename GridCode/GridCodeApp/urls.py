from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload.html', views.upload, name='upload'),
    path('get_group/<slug:val>/', views.get_group, name='get_group')
]

