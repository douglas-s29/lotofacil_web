"""
Management command to initialize lottery configurations.
"""
from django.core.management.base import BaseCommand
from lotteries.models import LotteryConfiguration, LotteryType


class Command(BaseCommand):
    help = 'Initialize lottery configurations with default values'

    def handle(self, *args, **options):
        """Create or update lottery configurations."""
        
        configs = [
            {
                'lottery_type': LotteryType.MEGA_SENA,
                'total_numbers': 60,
                'numbers_to_pick': 6,
                'min_bet_numbers': 6,
                'max_bet_numbers': 15,
                'primary_color': '#209869',
                'description': 'Escolha de 6 a 15 números entre 1 e 60. Sorteio duas vezes por semana.'
            },
            {
                'lottery_type': LotteryType.LOTOFACIL,
                'total_numbers': 25,
                'numbers_to_pick': 15,
                'min_bet_numbers': 15,
                'max_bet_numbers': 20,
                'primary_color': '#930089',
                'description': 'Escolha de 15 a 20 números entre 1 e 25. Sorteios de segunda a sábado.'
            },
            {
                'lottery_type': LotteryType.QUINA,
                'total_numbers': 80,
                'numbers_to_pick': 5,
                'min_bet_numbers': 5,
                'max_bet_numbers': 15,
                'primary_color': '#260085',
                'description': 'Escolha de 5 a 15 números entre 1 e 80. Sorteios de segunda a sábado.'
            },
            {
                'lottery_type': LotteryType.DUPLA_SENA,
                'total_numbers': 50,
                'numbers_to_pick': 6,
                'min_bet_numbers': 6,
                'max_bet_numbers': 15,
                'primary_color': '#A61324',
                'description': 'Escolha de 6 a 15 números entre 1 e 50. Dois sorteios por concurso.'
            },
            {
                'lottery_type': LotteryType.SUPER_SETE,
                'total_numbers': 10,
                'numbers_to_pick': 7,
                'min_bet_numbers': 7,
                'max_bet_numbers': 7,
                'primary_color': '#A8CF45',
                'description': '7 colunas com números de 0 a 9. Sorteios às segundas, quartas e sextas.'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for config_data in configs:
            config, created = LotteryConfiguration.objects.update_or_create(
                lottery_type=config_data['lottery_type'],
                defaults=config_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Criada configuração: {config.get_lottery_type_display()}'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'↻ Atualizada configuração: {config.get_lottery_type_display()}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Concluído! {created_count} criadas, {updated_count} atualizadas.'
            )
        )
