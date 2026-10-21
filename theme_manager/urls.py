from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="theme_home"),
    path('create/', views.create_theme, name="theme_create"),
    path('show/<int:theme_id>/', views.show_theme, name="theme_show"),
    path('update/<int:theme_id>/', views.update_theme, name="theme_update"),
    path('delete/<int:theme_id>/', views.delete_theme, name="theme_delete"),
]