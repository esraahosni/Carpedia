from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/new/', views.car_list, {'condition': 'new'}, name='new_cars'),
    path('cars/used/', views.car_list, {'condition': 'used'}, name='used_cars'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('about/', views.about_us, name='about_us'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add-car/', views.add_car, name='add_car'),
    path('edit-car/<int:pk>/', views.edit_car, name='edit_car'),
    path('delete-car/<int:pk>/', views.delete_car, name='delete_car'),
    path('manage-cars/', views.manage_cars, name='manage_cars'),
    path('user-management/', views.user_management, name='user_management'),
    path('promote-user/<int:user_id>/', views.promote_user, name='promote_user'),
    path('demote-user/<int:user_id>/', views.demote_user, name='demote_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('favourite/<int:pk>/', views.toggle_favourite, name='toggle_favourite'),
]
