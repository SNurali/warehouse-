from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('widgets/', views.WidgetListView.as_view(), name='widget_list'),
    path('widgets/add/', views.WidgetCreateView.as_view(), name='widget_add'),
    path('widgets/<int:pk>/edit/', views.WidgetUpdateView.as_view(), name='widget_edit'),
    path('widgets/<int:pk>/delete/', views.WidgetDeleteView.as_view(), name='widget_delete'),
    path('layout/', views.LayoutUpdateView.as_view(), name='layout_update'),
]