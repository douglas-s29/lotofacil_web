"""
Models for the lottery application.

Adapted from Android app specification to Django ORM.
Supports: Mega-Sena, Lotofácil, Quina, Dupla Sena, Super Sete
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import json


class LotteryType(models.TextChoices):
    """Lottery types supported by the system."""
    MEGA_SENA = 'MEGA_SENA', 'Mega-Sena'
    LOTOFACIL = 'LOTOFACIL', 'Lotofácil'
    QUINA = 'QUINA', 'Quina'
    DUPLA_SENA = 'DUPLA_SENA', 'Dupla Sena'
    SUPER_SETE = 'SUPER_SETE', 'Super Sete'


class LotteryConfiguration(models.Model):
    """Configuration for each lottery type."""
    lottery_type = models.CharField(
        max_length=20,
        choices=LotteryType.choices,
        unique=True,
        verbose_name='Tipo de Loteria'
    )
    total_numbers = models.IntegerField(
        verbose_name='Total de Números',
        help_text='Total de números disponíveis para sorteio'
    )
    numbers_to_pick = models.IntegerField(
        verbose_name='Números a Escolher',
        help_text='Quantidade de números em cada aposta'
    )
    min_bet_numbers = models.IntegerField(
        verbose_name='Mínimo de Números na Aposta',
        default=None,
        null=True,
        blank=True
    )
    max_bet_numbers = models.IntegerField(
        verbose_name='Máximo de Números na Aposta',
        default=None,
        null=True,
        blank=True
    )
    primary_color = models.CharField(
        max_length=7,
        default='#009B3A',
        verbose_name='Cor Primária',
        help_text='Cor hexadecimal para o tema da loteria'
    )
    description = models.TextField(
        verbose_name='Descrição',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Configuração de Loteria'
        verbose_name_plural = 'Configurações de Loterias'
    
    def __str__(self):
        return self.get_lottery_type_display()


class Draw(models.Model):
    """Historical draw/contest results."""
    lottery_type = models.CharField(
        max_length=20,
        choices=LotteryType.choices,
        db_index=True,
        verbose_name='Tipo de Loteria'
    )
    contest_number = models.IntegerField(
        verbose_name='Número do Concurso',
        db_index=True
    )
    draw_date = models.DateField(
        verbose_name='Data do Sorteio',
        db_index=True
    )
    numbers = models.JSONField(
        verbose_name='Números Sorteados',
        help_text='Lista de números sorteados'
    )
    # For Dupla Sena (has 2 draws)
    numbers_second_draw = models.JSONField(
        verbose_name='Números do 2º Sorteio',
        null=True,
        blank=True,
        help_text='Para Dupla Sena'
    )
    prize_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Prêmio',
        null=True,
        blank=True
    )
    winners_count = models.IntegerField(
        verbose_name='Número de Ganhadores',
        null=True,
        blank=True,
        default=0
    )
    accumulated = models.BooleanField(
        verbose_name='Acumulado',
        default=False
    )
    next_estimated_prize = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Estimativa Próximo Concurso',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sorteio'
        verbose_name_plural = 'Sorteios'
        unique_together = [['lottery_type', 'contest_number']]
        ordering = ['-contest_number']
        indexes = [
            models.Index(fields=['lottery_type', '-contest_number']),
            models.Index(fields=['lottery_type', '-draw_date']),
        ]
    
    def __str__(self):
        return f"{self.get_lottery_type_display()} - Concurso {self.contest_number}"
    
    def get_numbers_display(self):
        """Return formatted numbers for display."""
        if isinstance(self.numbers, str):
            numbers = json.loads(self.numbers)
        else:
            numbers = self.numbers
        return sorted(numbers)


class UserCombination(models.Model):
    """User saved combinations."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='combinations',
        verbose_name='Usuário',
        null=True,
        blank=True
    )
    lottery_type = models.CharField(
        max_length=20,
        choices=LotteryType.choices,
        verbose_name='Tipo de Loteria'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nome da Combinação',
        blank=True
    )
    numbers = models.JSONField(
        verbose_name='Números',
        help_text='Lista de números da combinação'
    )
    session_key = models.CharField(
        max_length=40,
        verbose_name='Chave de Sessão',
        null=True,
        blank=True,
        help_text='Para usuários não autenticados'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    is_favorite = models.BooleanField(default=False, verbose_name='Favorito')
    
    class Meta:
        verbose_name = 'Combinação do Usuário'
        verbose_name_plural = 'Combinações dos Usuários'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name or 'Combinação'} - {self.get_lottery_type_display()}"
    
    def get_numbers_display(self):
        """Return formatted numbers for display."""
        if isinstance(self.numbers, str):
            numbers = json.loads(self.numbers)
        else:
            numbers = self.numbers
        return sorted(numbers)


class NumberStatistics(models.Model):
    """Cached statistics for lottery numbers."""
    lottery_type = models.CharField(
        max_length=20,
        choices=LotteryType.choices,
        verbose_name='Tipo de Loteria'
    )
    number = models.IntegerField(
        verbose_name='Número',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    frequency = models.IntegerField(
        verbose_name='Frequência',
        default=0,
        help_text='Quantidade de vezes que o número foi sorteado'
    )
    last_draw_contest = models.IntegerField(
        verbose_name='Último Concurso',
        null=True,
        blank=True,
        help_text='Número do último concurso em que apareceu'
    )
    delay = models.IntegerField(
        verbose_name='Atraso',
        default=0,
        help_text='Concursos desde a última aparição'
    )
    max_delay = models.IntegerField(
        verbose_name='Atraso Máximo',
        default=0,
        help_text='Maior atraso histórico'
    )
    average_delay = models.FloatField(
        verbose_name='Atraso Médio',
        default=0.0,
        help_text='Média de concursos entre aparições'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )
    
    class Meta:
        verbose_name = 'Estatística de Número'
        verbose_name_plural = 'Estatísticas de Números'
        unique_together = [['lottery_type', 'number']]
        indexes = [
            models.Index(fields=['lottery_type', '-frequency']),
            models.Index(fields=['lottery_type', '-delay']),
        ]
    
    def __str__(self):
        return f"{self.get_lottery_type_display()} - Número {self.number}"


class GenerationFilter(models.Model):
    """Saved filter configurations for combination generation."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='generation_filters',
        verbose_name='Usuário',
        null=True,
        blank=True
    )
    lottery_type = models.CharField(
        max_length=20,
        choices=LotteryType.choices,
        verbose_name='Tipo de Loteria'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nome do Filtro'
    )
    filter_config = models.JSONField(
        verbose_name='Configuração do Filtro',
        help_text='JSON com os parâmetros do filtro'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Filtro de Geração'
        verbose_name_plural = 'Filtros de Geração'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_lottery_type_display()}"
