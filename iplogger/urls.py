from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name ="index"),
    path('createlink/',views.createlink, name ="createlink"),
    path('results/<int:tracking_code>/',views.results, name ="results"),
    path('track/<int:tracking_code>/', views.track, name = 'track'),
    path('accounts/register/', views.register, name='registration'),
    path('mylogs/', views.mylogs, name='mylogs'),
]