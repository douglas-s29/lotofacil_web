"""
URL configuration for lotteries app.
"""
from django.urls import path
from . import views

app_name = 'lotteries'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<str:lottery_type>/', views.LotteryDashboardView.as_view(), name='dashboard'),
    path('<str:lottery_type>/resultados/', views.DrawListView.as_view(), name='draws'),
    path('<str:lottery_type>/estatisticas/', views.StatisticsView.as_view(), name='statistics'),
    path('<str:lottery_type>/gerador/', views.GeneratorView.as_view(), name='generator'),
]
