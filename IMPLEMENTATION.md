# 🍀 Cebolão Loto Generator - Documentação de Implementação

## Visão Geral

Este documento descreve a implementação completa do sistema de análise estatística e geração de combinações para loterias da Caixa, adaptado da especificação original para Android para uma aplicação web Django.

## Arquitetura

### Camadas da Aplicação

```
┌─────────────────────────────────────────────┐
│          Templates (Presentation)           │
│  - home.html, dashboard.html, etc.         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           Views (Controllers)               │
│  - HomeView, DashboardView, etc.           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Services (Business Logic)           │
│  - StatisticsService                       │
│  - CombinationGeneratorService             │
│  - ResultCheckerService                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            Models (Data Layer)              │
│  - LotteryConfiguration, Draw, etc.        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│             Database (SQLite)               │
└─────────────────────────────────────────────┘
```

## Modelos de Dados

### LotteryConfiguration
Armazena configurações de cada tipo de loteria.

**Campos:**
- `lottery_type`: Tipo da loteria (MEGA_SENA, LOTOFACIL, etc.)
- `total_numbers`: Total de números disponíveis
- `numbers_to_pick`: Quantidade de números em cada jogo
- `min_bet_numbers`: Mínimo de números por aposta
- `max_bet_numbers`: Máximo de números por aposta
- `primary_color`: Cor hexadecimal para o tema
- `description`: Descrição da loteria

### Draw
Armazena resultados históricos de sorteios.

**Campos:**
- `lottery_type`: Tipo da loteria
- `contest_number`: Número do concurso
- `draw_date`: Data do sorteio
- `numbers`: JSON com números sorteados
- `numbers_second_draw`: JSON (para Dupla Sena)
- `prize_amount`: Valor do prêmio
- `winners_count`: Quantidade de ganhadores
- `accumulated`: Boolean se acumulou
- `next_estimated_prize`: Estimativa próximo concurso

**Índices:**
- `lottery_type + contest_number` (único)
- `lottery_type + draw_date`

### NumberStatistics
Cache de estatísticas por número.

**Campos:**
- `lottery_type`: Tipo da loteria
- `number`: Número analisado
- `frequency`: Vezes que foi sorteado
- `last_draw_contest`: Último concurso em que apareceu
- `delay`: Concursos desde última aparição
- `max_delay`: Maior atraso histórico
- `average_delay`: Atraso médio

**Índices:**
- `lottery_type + number` (único)
- `lottery_type + frequency` (para ordenação)
- `lottery_type + delay` (para ordenação)

### UserCombination
Combinações salvas pelos usuários.

**Campos:**
- `user`: ForeignKey para User (opcional)
- `lottery_type`: Tipo da loteria
- `name`: Nome da combinação
- `numbers`: JSON com os números
- `session_key`: Para usuários não autenticados
- `is_favorite`: Boolean favorito
- `created_at`: Data de criação

### GenerationFilter
Filtros salvos para geração de combinações.

**Campos:**
- `user`: ForeignKey para User (opcional)
- `lottery_type`: Tipo da loteria
- `name`: Nome do filtro
- `filter_config`: JSON com configuração
- `created_at`: Data de criação

## Serviços

### StatisticsService

**Métodos:**
- `calculate_statistics(lottery_type)`: Calcula estatísticas para todos os números
- `get_statistics(lottery_type, force_refresh)`: Retorna estatísticas (cached)
- `get_most_frequent(lottery_type, limit)`: Números mais frequentes
- `get_most_delayed(lottery_type, limit)`: Números mais atrasados

**Cache:**
- Timeout: 3600 segundos (1 hora)
- Chave: `stats_{lottery_type}`
- Invalidado após recálculo

### CombinationGeneratorService

**Métodos:**
- `generate_combinations(...)`: Gera combinações com filtros
  - Parâmetros:
    - `lottery_type`: Tipo de loteria
    - `numbers_count`: Quantidade de números por jogo
    - `games_count`: Quantidade de jogos
    - `fixed_numbers`: Números fixos (opcional)
    - `include_frequent`: Incluir frequentes
    - `include_delayed`: Incluir atrasados
    - `mix_strategy`: Misturar estratégias

- `validate_combination(lottery_type, numbers)`: Valida uma combinação
  - Retorna: `{valid, errors, warnings}`

**Algoritmo de Geração:**
1. Monta pool de números baseado nos filtros
2. Se `include_frequent`: adiciona top 20 mais frequentes
3. Se `include_delayed`: adiciona top 20 mais atrasados
4. Se `mix_strategy`: adiciona números aleatórios
5. Para cada jogo:
   - Começa com números fixos
   - Preenche slots restantes aleatoriamente do pool
   - Garante quantidade correta de números

### ResultCheckerService

**Métodos:**
- `check_combination(lottery_type, numbers, contest_number)`: Verifica combinação contra resultado
  - Retorna:
    ```python
    {
        'found': bool,
        'contest_number': int,
        'draw_date': date,
        'drawn_numbers': list,
        'user_numbers': list,
        'matches': list,
        'match_count': int,
        'is_winner': bool
    }
    ```

## Views

### HomeView (TemplateView)
- Rota: `/`
- Template: `lotteries/home.html`
- Contexto: `lottery_types` (todas as configurações)

### LotteryDashboardView (DetailView)
- Rota: `/<lottery_type>/`
- Template: `lotteries/dashboard.html`
- Contexto:
  - `object`: Configuração da loteria
  - `latest_draws`: Últimos 10 sorteios
  - `statistics`: Top 25 estatísticas

### DrawListView (ListView)
- Rota: `/<lottery_type>/resultados/`
- Template: `lotteries/draw_list.html`
- Paginação: 20 itens por página
- Contexto: `draws`, `lottery_config`

### StatisticsView (DetailView)
- Rota: `/<lottery_type>/estatisticas/`
- Template: `lotteries/statistics.html`
- Contexto:
  - `all_statistics`: Todas as estatísticas
  - `most_frequent`: Top 10 frequentes
  - `most_delayed`: Top 10 atrasados
  - `max_frequency`: Para cálculo de progress bar

### GeneratorView (DetailView)
- Rota: `/<lottery_type>/gerador/`
- Template: `lotteries/generator.html`
- Contexto:
  - `statistics`: Para sugestões
  - `number_range`: Range de números disponíveis
  - `bet_count_range`: Range de quantidades de aposta

## Templates

### Estrutura Base
- `base.html`: Template base com navbar, footer, Bootstrap 5
- Todas as páginas estendem `base.html`

### Componentes Reutilizáveis

**Number Ball:**
```html
<div class="number-ball" style="background: {{ color }}">
    {{ number|stringformat:"02d" }}
</div>
```

**Stats Card:**
```html
<div class="stats-card most-frequent">
    <!-- Conteúdo -->
</div>
```

### JavaScript
- Tooltips Bootstrap
- Gerador de combinações client-side
- Seletor de números interativo
- Funções de cópia e exportação

## Design System

### Cores por Loteria
```css
--mega-sena: #209869
--lotofacil: #930089
--quina: #260085
--dupla-sena: #A61324
--super-sete: #A8CF45
```

### Componentes CSS
- `.number-ball`: Bola de número (45x45px)
- `.number-ball-small`: Bola pequena (35x35px)
- `.stats-card`: Card de estatística
- `.lottery-card`: Card de loteria (home)
- `.filter-section`: Seção de filtros

### Responsividade
- Mobile-first design
- Breakpoints: 768px, 992px, 1200px
- Grid Bootstrap 5
- Flex layouts

## Comandos de Gerenciamento

### init_lotteries
```bash
python manage.py init_lotteries
```
Inicializa as 5 configurações de loteria com valores padrão.

### generate_sample_data
```bash
python manage.py generate_sample_data --lottery LOTOFACIL --count 100
```
Gera dados de teste para desenvolvimento.

**Opções:**
- `--lottery`: Tipo específico (opcional)
- `--count`: Quantidade de sorteios (padrão: 100)

### calculate_stats
```bash
python manage.py calculate_stats --lottery MEGA_SENA
```
Calcula estatísticas baseadas em sorteios históricos.

**Opções:**
- `--lottery`: Tipo específico (opcional, calcula todos se omitido)

## Fluxo de Uso

### 1. Primeiro Acesso
1. Usuário acessa a home
2. Vê cards das 5 loterias
3. Clica em uma loteria

### 2. Dashboard
1. Vê último resultado
2. Top números frequentes
3. Últimos concursos
4. Acesso rápido às ferramentas

### 3. Gerador
1. Seleciona quantidade de números
2. Define quantidade de jogos
3. Escolhe filtros estatísticos
4. Opcionalmente seleciona números fixos
5. Clica "Gerar Combinações"
6. Vê resultados
7. Pode copiar ou exportar

### 4. Estatísticas
1. Vê top 10 mais frequentes
2. Vê top 10 mais atrasados
3. Acessa tabela completa
4. Entende métricas com tooltips

### 5. Resultados
1. Navega pelos sorteios históricos
2. Vê números sorteados
3. Informações de prêmio
4. Paginação

## Performance

### Otimizações Implementadas
- Cache de estatísticas (1 hora)
- Índices de banco de dados
- Queryset otimizado com select_related/prefetch_related
- Paginação de resultados
- Lazy loading de estatísticas

### Métricas Esperadas
- Home: < 100ms
- Dashboard: < 200ms (com cache)
- Estatísticas: < 300ms (com cache)
- Gerador: < 50ms (client-side)
- Resultados: < 150ms

## Segurança

### Medidas Implementadas
- ✅ CSRF protection (Django padrão)
- ✅ XSS prevention (template auto-escape)
- ✅ SQL Injection prevention (ORM)
- ✅ Validação de inputs
- ✅ Sanitização de dados JSON
- ✅ Debug=False em produção
- ✅ SECRET_KEY em variável de ambiente (recomendado)

### CodeQL Scan
- **Resultado**: 0 vulnerabilidades encontradas

## Avisos Legais

**Implementado em todas as páginas:**
- Disclaimers sobre não realizar apostas
- Aviso que não promete previsões
- Esclarecimento sobre aleatoriedade
- Nota sobre uso analítico/informativo

## Próximos Passos (Backlog)

### Funcionalidades Futuras
1. **Autenticação de Usuários**
   - Django auth
   - Salvar combinações por usuário
   - Histórico pessoal

2. **Exportação**
   - PDF com combinações geradas
   - TXT para impressão
   - Formato para volante

3. **API REST**
   - Django REST Framework
   - Endpoints para mobile
   - Webhook para novos resultados

4. **PWA**
   - Service Workers
   - Offline-first completo
   - App-like experience

5. **Analytics**
   - Padrões de combinações
   - Análise de pares/trios
   - Visualizações gráficas

6. **Importação de Dados**
   - Scraper para site da Caixa
   - Atualização automática
   - Sincronização incremental

### Melhorias Técnicas
1. Testes unitários (models, services)
2. Testes de integração (views, templates)
3. CI/CD pipeline
4. Deploy automatizado
5. Monitoramento (Sentry, etc.)
6. PostgreSQL em produção
7. Redis para cache
8. CDN para assets

## Conclusão

A aplicação Django foi completamente adaptada da especificação original Android, mantendo todos os conceitos e funcionalidades principais:

✅ **Design System**: Adaptado de Material 3 para Bootstrap 5 com CSS customizado
✅ **Offline-first**: Cache implementado com Django cache framework
✅ **Explicabilidade**: Tooltips e textos explicativos em português
✅ **Performance**: Cache LRU-like, índices otimizados
✅ **Clean Architecture**: Separação clara de camadas
✅ **5 Loterias**: Todas configuradas e funcionais
✅ **Compliance**: Avisos legais em todas as páginas

A aplicação está pronta para uso em desenvolvimento e pode ser facilmente adaptada para produção com as configurações apropriadas.
