from django.contrib import admin
from .models import (
    LotteryConfiguration, Draw, UserCombination,
    NumberStatistics, GenerationFilter
)


@admin.register(LotteryConfiguration)
class LotteryConfigurationAdmin(admin.ModelAdmin):
    list_display = ['lottery_type', 'total_numbers', 'numbers_to_pick', 'primary_color']
    list_filter = ['lottery_type']
    search_fields = ['lottery_type', 'description']


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ['lottery_type', 'contest_number', 'draw_date', 'display_numbers', 'accumulated']
    list_filter = ['lottery_type', 'accumulated', 'draw_date']
    search_fields = ['contest_number']
    date_hierarchy = 'draw_date'
    ordering = ['-contest_number']
    
    def display_numbers(self, obj):
        return ', '.join(map(str, obj.get_numbers_display()))
    display_numbers.short_description = 'Números Sorteados'


@admin.register(UserCombination)
class UserCombinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'lottery_type', 'user', 'display_numbers', 'is_favorite', 'created_at']
    list_filter = ['lottery_type', 'is_favorite', 'created_at']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'created_at'
    
    def display_numbers(self, obj):
        return ', '.join(map(str, obj.get_numbers_display()))
    display_numbers.short_description = 'Números'


@admin.register(NumberStatistics)
class NumberStatisticsAdmin(admin.ModelAdmin):
    list_display = ['lottery_type', 'number', 'frequency', 'delay', 'average_delay', 'last_updated']
    list_filter = ['lottery_type']
    search_fields = ['number']
    ordering = ['lottery_type', '-frequency']


@admin.register(GenerationFilter)
class GenerationFilterAdmin(admin.ModelAdmin):
    list_display = ['name', 'lottery_type', 'user', 'created_at']
    list_filter = ['lottery_type', 'created_at']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'created_at'
