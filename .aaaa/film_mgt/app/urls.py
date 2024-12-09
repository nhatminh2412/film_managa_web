from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('authorize', views.authorize),
    path('login/', views.login_view, name='login'),
    path('api/employees/', views.get_employee, name='get_employees'),
    path('api/employees/add/', views.add_employee, name='add_employee'),
    path('api/employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('api/employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('api/movies/', views.get_movies, name='get_movies'),
    path('api/movies/add/', views.add_movie, name='add_movie'),  
    path('api/movies/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('api/movies/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
]