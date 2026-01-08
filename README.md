# Lotofacil Web

Sistema moderno e responsivo para análise estatística e geração de combinações para loterias da Caixa Econômica Federal.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Desenvolvimento](#desenvolvimento)
- [Deployment](#deployment)
- [CI/CD](#cicd)
- [Avisos Legais](#avisos-legais)

---

## 🎯 Visão Geral

O Lotofácil Web é uma aplicação web moderna que oferece ferramentas de análise estatística e geração inteligente de combinações para as principais loterias da Caixa:

- **Mega-Sena**
- **Lotofácil**
- **Quina**
- **Dupla Sena**
- **Super Sete**

---

## 🏗 Arquitetura

### Stack Tecnológico

```
┌─────────────────────────────────────────┐
│          Nginx (Reverse Proxy)          │
│              Port 80                    │
└──────────┬───────────────────┬──────────┘
           │                   │
           ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│   Next.js 14     │  │   FastAPI        │
│   (Frontend)     │  │   (Backend)      │
│   Port 3000      │  │   Port 8000      │
└──────────────────┘  └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │   PostgreSQL     │
                      │   Port 5432      │
                      └──────────────────┘
```

### Frontend
- **Framework**: [Next.js 14](https://nextjs.org/) com App Router
- **UI**: [TailwindCSS](https://tailwindcss.com/)
- **Linguagem**: TypeScript
- **Features**: SSR, CSR, Responsive Design

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: SQLAlchemy
- **Migrações**: Alembic
- **Validação**: Pydantic
- **Linguagem**: Python 3.11+

### Database
- **SGBD**: [PostgreSQL 16](https://www.postgresql.org/)
- **Persistência**: Dados históricos, estatísticas, combinações de usuários

### Infraestrutura
- **Containerização**: Docker & Docker Compose
- **Proxy**: Nginx
- **CI/CD**: GitHub Actions
- **Deployment**: VPS-ready

---

## 🛠 Tecnologias

### Backend
- FastAPI 0.115+
- SQLAlchemy 2.0+
- Alembic 1.14+
- Pydantic 2.10+
- PostgreSQL Driver (psycopg2-binary)
- Pandas & NumPy (análise estatística)

### Frontend
- Next.js 14
- React 18
- TypeScript 5
- TailwindCSS 3
- Fetch API Client

### DevOps
- Docker & Docker Compose
- Nginx
- GitHub Actions
- PostgreSQL 16

---

## ⚡ Funcionalidades

### 1. **Home**
- Apresentação das loterias disponíveis
- Navegação intuitiva
- Cards informativos

### 2. **Gerador de Números**
- Geração de combinações personalizadas
- Filtros estatísticos:
  - Números mais frequentes
  - Números mais atrasados
  - Mistura de estratégias
- Números fixos opcionais
- Quantidade configurável de jogos
- Exportação de resultados

### 3. **Estatísticas**
- Top 10 números mais frequentes
- Top 10 números mais atrasados
- Tabela completa com:
  - Frequência de aparição
  - Atraso atual
  - Atraso máximo histórico
  - Atraso médio
- Filtros por loteria

### 4. **Conferidor**
- Verificação de combinações contra resultados
- Comparação com concurso específico ou mais recente
- Visualização de acertos
- Status de premiação

### 5. **Salvos**
- Armazenamento de combinações favoritas
- Marcação de favoritos
- Filtros por loteria
- Ações rápidas (conferir, copiar, excluir)

---

## 🚀 Instalação

### Pré-requisitos

- [Docker](https://www.docker.com/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/) 2.0+
- [Node.js](https://nodejs.org/) 20+ (para desenvolvimento local)
- [Python](https://www.python.org/) 3.11+ (para desenvolvimento local)

### Clone o Repositório

```bash
git clone https://github.com/douglas-s29/lotofacil_web.git
cd lotofacil_web
```

### Configuração de Ambiente

```bash
# Copie os arquivos de exemplo
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edite os arquivos .env com suas configurações
# IMPORTANTE: Altere o SECRET_KEY em produção
```

### Inicialização com Docker Compose

```bash
# Build e start de todos os serviços
docker-compose up --build

# Ou em modo detached
docker-compose up -d --build
```

### Inicializar Banco de Dados

```bash
# Execute as migrações
docker-compose exec backend alembic upgrade head

# Popule com dados iniciais (configurações de loterias)
docker-compose exec backend python -c "
from app.db.session import SessionLocal
from app.models import LotteryConfiguration

db = SessionLocal()

lotteries = [
    LotteryConfiguration(lottery_type='MEGA_SENA', total_numbers=60, numbers_to_pick=6, 
                        min_bet_numbers=6, max_bet_numbers=20, primary_color='#209869',
                        description='6 números de 1 a 60'),
    LotteryConfiguration(lottery_type='LOTOFACIL', total_numbers=25, numbers_to_pick=15,
                        min_bet_numbers=15, max_bet_numbers=20, primary_color='#930089',
                        description='15 números de 1 a 25'),
    LotteryConfiguration(lottery_type='QUINA', total_numbers=80, numbers_to_pick=5,
                        min_bet_numbers=5, max_bet_numbers=15, primary_color='#260085',
                        description='5 números de 1 a 80'),
    LotteryConfiguration(lottery_type='DUPLA_SENA', total_numbers=50, numbers_to_pick=6,
                        min_bet_numbers=6, max_bet_numbers=15, primary_color='#A61324',
                        description='6 números de 1 a 50'),
    LotteryConfiguration(lottery_type='SUPER_SETE', total_numbers=10, numbers_to_pick=7,
                        min_bet_numbers=7, max_bet_numbers=21, primary_color='#A8CF45',
                        description='7 colunas de 0 a 9'),
]

for lottery in lotteries:
    db.merge(lottery)
db.commit()
print('Loterias inicializadas com sucesso!')
"
```

### Acesso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Nginx**: http://localhost

---

## 💻 Desenvolvimento

### Backend (FastAPI)

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar servidor de desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)

```bash
cd frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev
```

### Migrações de Banco de Dados

```bash
cd backend

# Criar nova migração
alembic revision --autogenerate -m "Descrição da migração"

# Aplicar migrações
alembic upgrade head

# Reverter última migração
alembic downgrade -1
```

---

## 🌐 Deployment

### VPS com Docker

1. **Preparar VPS**
   ```bash
   # Atualizar sistema
   sudo apt update && sudo apt upgrade -y
   
   # Instalar Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Instalar Docker Compose
   sudo apt install docker-compose -y
   ```

2. **Clonar Repositório**
   ```bash
   git clone https://github.com/douglas-s29/lotofacil_web.git
   cd lotofacil_web
   ```

3. **Configurar Variáveis de Ambiente**
   ```bash
   cp .env.example .env
   nano .env  # Editar com credenciais de produção
   ```

4. **Build e Deploy**
   ```bash
   docker-compose -f docker-compose.yml up -d --build
   ```

5. **Configurar Nginx (opcional, para SSL)**
   ```nginx
   server {
       listen 80;
       server_name seu-dominio.com;
       
       location / {
           proxy_pass http://localhost;
       }
   }
   ```

### Variáveis de Ambiente de Produção

```env
# .env
SECRET_KEY=your-very-strong-secret-key-here
DATABASE_URL=postgresql://user:password@db:5432/lotofacil_web

# backend/.env
DATABASE_URL=postgresql://user:password@db:5432/lotofacil_web
SECRET_KEY=your-very-strong-secret-key-here

# frontend/.env.local
NEXT_PUBLIC_API_URL=https://api.seu-dominio.com
```

---

## 🔄 CI/CD

### GitHub Actions Workflows

O projeto inclui 3 workflows principais:

1. **Backend CI** (`.github/workflows/backend-ci.yml`)
   - Lint do código Python
   - Testes de API
   - Verificação de migrações

2. **Frontend CI** (`.github/workflows/frontend-ci.yml`)
   - Lint do código TypeScript
   - Build da aplicação Next.js
   - Testes unitários

3. **Docker Build** (`.github/workflows/docker-build.yml`)
   - Build das imagens Docker
   - Verificação do docker-compose

### Execução Local dos Workflows

```bash
# Backend
cd backend
flake8 app
pytest tests/

# Frontend
cd frontend
npm run lint
npm run build
```

---

## ⚖️ Avisos Legais

**IMPORTANTE:** Este sistema é apenas uma ferramenta de análise estatística e geração de combinações com fins educacionais e informativos.

- ❌ **NÃO** realiza apostas
- ❌ **NÃO** promete ou garante ganhos
- ❌ **NÃO** prevê resultados futuros
- ✅ Analisa dados históricos
- ✅ Gera combinações baseadas em estatísticas
- ✅ Ferramenta educacional

**Os sorteios de loterias são eventos completamente aleatórios. Use com responsabilidade.**

---

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## 👤 Autor

**douglas-s29**
- GitHub: [@douglas-s29](https://github.com/douglas-s29)

---

## 🤝 Contribuições

Contribuições, issues e feature requests são bem-vindos!

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma [issue](https://github.com/douglas-s29/lotofacil_web/issues) no GitHub.