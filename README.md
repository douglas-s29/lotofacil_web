# 🍀 Cebolão Loto Generator - Django Web Application

Sistema de análise estatística e geração de combinações para loterias da Caixa Econômica Federal.

## 📋 Sobre o Projeto

Aplicação web desenvolvida em Django adaptada da especificação original para Android, oferecendo:

- **Análise Estatística**: Frequência de números, atrasos, padrões históricos
- **Gerador Inteligente**: Criação de combinações com filtros personalizados
- **Histórico Completo**: Acesso a todos os resultados anteriores
- **Design Responsivo**: Interface adaptada para desktop e mobile
- **Offline-first**: Dados em cache para melhor performance

### Loterias Suportadas

- 🎰 **Mega-Sena**: 6 de 60 números
- 🍀 **Lotofácil**: 15 de 25 números
- 🎲 **Quina**: 5 de 80 números
- 🎯 **Dupla Sena**: 2x 6 de 50 números
- 7️⃣ **Super Sete**: 7 colunas de 0-9

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.12+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/douglas-s29/lotofacil_web.git
cd lotofacil_web
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Inicialize as configurações de loterias:
```bash
python manage.py init_lotteries
```

5. (Opcional) Crie um superusuário para acessar o admin:
```bash
python manage.py createsuperuser
```

6. Execute o servidor de desenvolvimento:
```bash
python manage.py runserver
```

7. Acesse em seu navegador:
```
http://localhost:8000
```

## 📁 Estrutura do Projeto

```
cebolao_loto/           # Configurações do Django
lotteries/              # App principal de loterias
├── models.py           # Modelos de dados
├── views.py            # Views/Controllers
├── urls.py             # Rotas
├── admin.py            # Configuração do admin
└── management/         # Comandos personalizados
templates/              # Templates HTML
├── base.html           # Template base
└── lotteries/          # Templates da app
static/                 # Arquivos estáticos
└── css/                # Estilos customizados
```

## 🎨 Funcionalidades

### Dashboard
- Visualização do último resultado
- Estatísticas resumidas
- Acesso rápido às ferramentas

### Gerador de Combinações
- Configuração de quantidade de números
- Filtros estatísticos
- Números fixos opcionais
- Exportação de resultados

### Análise Estatística
- Números mais frequentes
- Números mais atrasados
- Tabela completa de estatísticas
- Métricas de atraso médio e máximo

### Histórico de Resultados
- Lista paginada de todos os sorteios
- Filtros por data
- Visualização de números sorteados

## 🔒 Aviso Legal

**⚠️ IMPORTANTE**: Este aplicativo é puramente analítico e informativo. 

- Não realiza apostas
- Não promete previsões
- Não aumenta chances matemáticas de ganhar
- Os sorteios são eventos aleatórios e independentes
- Resultados passados não influenciam resultados futuros

Jogue com responsabilidade. Este sistema é apenas uma ferramenta de auxílio para análise de dados históricos.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.0.1
- **Frontend**: Bootstrap 5.3, Material Icons
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção recomendado)
- **Cache**: Django Cache Framework
- **Python**: 3.12+

## 📝 Comandos de Gerenciamento

### Inicializar Configurações
```bash
python manage.py init_lotteries
```

### Criar Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Executar Testes
```bash
python manage.py test
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é apenas para fins educacionais e de estudo.

## 👥 Autor

Douglas S29 - [@douglas-s29](https://github.com/douglas-s29)

---

**Desenvolvido com 💚 para a comunidade de analistas de loterias**