from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('company/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('company/edit/', views.CompanyUpdateView.as_view(), name='company_edit'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('subscription/', views.SubscriptionDetailView.as_view(), name='subscription_detail'),
]