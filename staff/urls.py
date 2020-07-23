from django.urls import path
from staff import views

app_name = "staff"
urlpatterns = [
    path('', views.index, name = "index"),
    path('check/', views.check, name = "check"),
    path('success/', views.success, name = "success")
]
