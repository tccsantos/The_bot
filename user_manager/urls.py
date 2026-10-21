from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="user_home"),
    path('create/', views.create_user, name="user_create"),
    path('show/<int:user_id>/', views.show_user, name="user_show"),
    path('update/<int:user_id>/', views.update_user, name="user_update"),
    path('delete/<int:user_id>/', views.delete_user, name="user_delete"),
]