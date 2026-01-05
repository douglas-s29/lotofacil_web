"""
Views for the lottery application.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from .models import LotteryType, LotteryConfiguration, Draw, NumberStatistics


class HomeView(TemplateView):
    """Home page with lottery type selection."""
    template_name = 'lotteries/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lottery_types'] = LotteryConfiguration.objects.all()
        context['page_title'] = 'Cebolão Loto - Gerador de Combinações'
        return context


class LotteryDashboardView(DetailView):
    """Dashboard for a specific lottery type."""
    model = LotteryConfiguration
    template_name = 'lotteries/dashboard.html'
    slug_field = 'lottery_type'
    slug_url_kwarg = 'lottery_type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lottery_type = self.object.lottery_type
        
        # Get latest draws
        context['latest_draws'] = Draw.objects.filter(
            lottery_type=lottery_type
        )[:10]
        
        # Get statistics
        context['statistics'] = NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('-frequency')[:25]
        
        context['page_title'] = f'{self.object.get_lottery_type_display()} - Dashboard'
        return context


class DrawListView(ListView):
    """List all draws for a lottery type."""
    model = Draw
    template_name = 'lotteries/draw_list.html'
    context_object_name = 'draws'
    paginate_by = 20
    
    def get_queryset(self):
        lottery_type = self.kwargs.get('lottery_type')
        return Draw.objects.filter(lottery_type=lottery_type)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lottery_type = self.kwargs.get('lottery_type')
        context['lottery_config'] = get_object_or_404(
            LotteryConfiguration,
            lottery_type=lottery_type
        )
        context['page_title'] = f'Resultados - {context["lottery_config"].get_lottery_type_display()}'
        return context


class StatisticsView(DetailView):
    """Statistics page for a lottery type."""
    model = LotteryConfiguration
    template_name = 'lotteries/statistics.html'
    slug_field = 'lottery_type'
    slug_url_kwarg = 'lottery_type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lottery_type = self.object.lottery_type
        
        # All number statistics
        context['all_statistics'] = NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('number')
        
        # Most frequent numbers
        context['most_frequent'] = NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('-frequency')[:10]
        
        # Most delayed numbers
        context['most_delayed'] = NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('-delay')[:10]
        
        context['page_title'] = f'Estatísticas - {self.object.get_lottery_type_display()}'
        return context


class GeneratorView(DetailView):
    """Combination generator page."""
    model = LotteryConfiguration
    template_name = 'lotteries/generator.html'
    slug_field = 'lottery_type'
    slug_url_kwarg = 'lottery_type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lottery_type = self.object.lottery_type
        
        # Get statistics for filter suggestions
        context['statistics'] = NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('number')
        
        context['page_title'] = f'Gerador - {self.object.get_lottery_type_display()}'
        return context
