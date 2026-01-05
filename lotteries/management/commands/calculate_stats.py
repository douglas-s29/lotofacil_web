"""
Management command to calculate statistics for lottery numbers.
"""
from django.core.management.base import BaseCommand
from lotteries.models import LotteryType
from lotteries.services import StatisticsService


class Command(BaseCommand):
    help = 'Calculate statistics for lottery numbers based on historical draws'

    def add_arguments(self, parser):
        parser.add_argument(
            '--lottery',
            type=str,
            help='Specific lottery type to process (e.g., MEGA_SENA, LOTOFACIL)',
        )

    def handle(self, *args, **options):
        lottery_types = []
        
        if options['lottery']:
            lottery_types = [options['lottery']]
        else:
            lottery_types = [choice[0] for choice in LotteryType.choices]
        
        for lottery_type in lottery_types:
            self.stdout.write(f'Calculando estatísticas para {lottery_type}...')
            
            try:
                StatisticsService.calculate_statistics(lottery_type)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Estatísticas calculadas para {lottery_type}'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Erro ao calcular estatísticas para {lottery_type}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Processo concluído!')
        )
