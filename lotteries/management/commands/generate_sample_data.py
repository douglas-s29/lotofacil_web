"""
Management command to generate sample lottery data for testing.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from lotteries.models import Draw, LotteryType, LotteryConfiguration
from lotteries.services import StatisticsService


class Command(BaseCommand):
    help = 'Generate sample lottery data for testing and development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--lottery',
            type=str,
            help='Specific lottery type (e.g., MEGA_SENA, LOTOFACIL)',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of draws to generate (default: 100)',
        )

    def handle(self, *args, **options):
        lottery_type = options.get('lottery')
        count = options['count']
        
        if lottery_type:
            lottery_types = [lottery_type]
        else:
            lottery_types = [choice[0] for choice in LotteryType.choices]
        
        for ltype in lottery_types:
            self.stdout.write(f'\nGerando {count} sorteios de teste para {ltype}...')
            
            try:
                config = LotteryConfiguration.objects.get(lottery_type=ltype)
                
                # Start from 100 contests ago
                base_date = timezone.now().date() - timedelta(days=count * 3)
                
                for i in range(count):
                    contest_number = i + 1
                    draw_date = base_date + timedelta(days=i * 3)
                    
                    # Generate random numbers
                    numbers = sorted(random.sample(
                        range(1, config.total_numbers + 1),
                        config.numbers_to_pick
                    ))
                    
                    # Random prize and winners
                    accumulated = random.choice([True, False, False, False])  # 25% chance
                    winners_count = 0 if accumulated else random.randint(0, 5)
                    prize_amount = random.uniform(1000000, 50000000) if winners_count > 0 else 0
                    
                    draw, created = Draw.objects.update_or_create(
                        lottery_type=ltype,
                        contest_number=contest_number,
                        defaults={
                            'draw_date': draw_date,
                            'numbers': numbers,
                            'accumulated': accumulated,
                            'winners_count': winners_count,
                            'prize_amount': prize_amount,
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  ✓ Concurso {contest_number} criado')
                
                # Calculate statistics after generating draws
                self.stdout.write('  Calculando estatísticas...')
                StatisticsService.calculate_statistics(ltype)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ {count} sorteios gerados para {ltype}'
                    )
                )
                
            except LotteryConfiguration.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Configuração não encontrada para {ltype}. '
                        f'Execute primeiro: python manage.py init_lotteries'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Erro ao gerar dados para {ltype}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Geração de dados concluída!')
        )
