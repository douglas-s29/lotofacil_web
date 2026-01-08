# 🚀 Guia de Deployment - Lotofácil Web

## Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Deployment Local com Docker](#deployment-local-com-docker)
3. [Deployment em VPS](#deployment-em-vps)
4. [Configuração SSL com Let's Encrypt](#configuração-ssl-com-lets-encrypt)
5. [Monitoramento e Logs](#monitoramento-e-logs)
6. [Backup e Restore](#backup-e-restore)
7. [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

### Hardware Mínimo (VPS)
- CPU: 2 cores
- RAM: 4GB
- Disco: 20GB SSD
- Sistema: Ubuntu 20.04+ ou Debian 11+

### Software Necessário
- Docker 20.10+
- Docker Compose 2.0+
- Git
- (Opcional) Nginx para SSL/reverse proxy externo

---

## Deployment Local com Docker

### 1. Clone e Configuração

```bash
# Clone o repositório
git clone https://github.com/douglas-s29/lotofacil_web.git
cd lotofacil_web

# Copie os arquivos de ambiente
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

### 2. Configure as Variáveis de Ambiente

Edite o arquivo `.env`:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=postgresql://postgres:postgres@db:5432/lotofacil_web
```

### 3. Build e Start

```bash
# Build e start todos os serviços
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 4. Inicializar Banco de Dados

```bash
# Executar migrações
docker-compose exec backend alembic upgrade head

# Popular com dados iniciais
docker-compose exec backend python scripts/init_db.py
```

### 5. Acesso

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Deployment em VPS

### 1. Preparar o Servidor

```bash
# Conectar ao VPS via SSH
ssh usuario@seu-servidor.com

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar Git
sudo apt install git -y

# Re-login para aplicar grupo docker
exit
ssh usuario@seu-servidor.com
```

### 2. Clone e Configure

```bash
# Clone o projeto
cd /opt
sudo git clone https://github.com/douglas-s29/lotofacil_web.git
sudo chown -R $USER:$USER lotofacil_web
cd lotofacil_web

# Configure ambiente
cp .env.example .env
nano .env  # Editar com credenciais seguras
```

### 3. Variáveis de Ambiente de Produção

```env
# .env
SECRET_KEY=um-secret-key-muito-forte-e-aleatorio-aqui
DATABASE_URL=postgresql://lotofacil_user:senha_forte_aqui@db:5432/lotofacil_web

# backend/.env
DATABASE_URL=postgresql://lotofacil_user:senha_forte_aqui@db:5432/lotofacil_web
SECRET_KEY=um-secret-key-muito-forte-e-aleatorio-aqui
CORS_ORIGINS=["https://seu-dominio.com","https://www.seu-dominio.com"]

# frontend/.env.local
NEXT_PUBLIC_API_URL=https://api.seu-dominio.com
```

### 4. Deploy

```bash
# Build e start
docker-compose up -d --build

# Verificar status
docker-compose ps

# Inicializar banco
docker-compose exec backend alembic upgrade head

# Ver logs
docker-compose logs -f
```

### 5. Configurar Firewall

```bash
# Permitir portas necessárias
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

## Configuração SSL com Let's Encrypt

### 1. Instalar Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Obter Certificado

```bash
# Parar nginx do docker temporariamente
docker-compose stop nginx

# Obter certificado
sudo certbot certonly --standalone -d seu-dominio.com -d www.seu-dominio.com

# Reiniciar nginx
docker-compose start nginx
```

### 3. Atualizar Nginx Config

Crie um novo arquivo `nginx-ssl.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name seu-dominio.com www.seu-dominio.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name seu-dominio.com www.seu-dominio.com;

        ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Frontend
        location / {
            proxy_pass http://frontend:3000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # Backend API
        location /api {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend Docs
        location /docs {
            proxy_pass http://backend:8000;
        }
    }
}
```

### 4. Atualizar docker-compose.yml

```yaml
  nginx:
    image: nginx:alpine
    container_name: lotofacil_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-ssl.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - frontend
      - backend
```

### 5. Renovação Automática

```bash
# Adicionar ao crontab
sudo crontab -e

# Adicionar linha (renova a cada 2 meses)
0 0 1 */2 * certbot renew --quiet && docker-compose restart nginx
```

---

## Monitoramento e Logs

### Ver Logs

```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Últimas 100 linhas
docker-compose logs --tail=100 backend
```

### Monitorar Recursos

```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats

# Espaço em disco
docker system df
```

### Health Checks

```bash
# Verificar saúde do backend
curl http://localhost:8000/health

# Verificar frontend
curl http://localhost:3000
```

---

## Backup e Restore

### Backup do Banco de Dados

```bash
# Criar backup
docker-compose exec db pg_dump -U postgres lotofacil_web > backup_$(date +%Y%m%d).sql

# Ou usando docker diretamente
docker exec lotofacil_db pg_dump -U postgres lotofacil_web > backup_$(date +%Y%m%d).sql
```

### Restore do Banco de Dados

```bash
# Restore
docker-compose exec -T db psql -U postgres lotofacil_web < backup_20240101.sql
```

### Backup Automático

Crie um script `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/lotofacil_web/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do banco
docker exec lotofacil_db pg_dump -U postgres lotofacil_web | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup concluído: $BACKUP_DIR/db_$DATE.sql.gz"
```

Agendar no crontab:

```bash
# Diariamente às 2h da manhã
0 2 * * * /opt/lotofacil_web/backup.sh >> /var/log/lotofacil_backup.log 2>&1
```

---

## Troubleshooting

### Problema: Container não inicia

```bash
# Ver logs de erro
docker-compose logs backend
docker-compose logs frontend

# Reconstruir container
docker-compose up -d --build --force-recreate backend
```

### Problema: Erro de conexão com banco de dados

```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps db

# Verificar logs do banco
docker-compose logs db

# Testar conexão
docker-compose exec backend python -c "from app.db.session import engine; print(engine.connect())"
```

### Problema: Frontend não carrega

```bash
# Verificar variável de ambiente
docker-compose exec frontend printenv | grep NEXT_PUBLIC_API_URL

# Verificar build
docker-compose exec frontend npm run build

# Reiniciar container
docker-compose restart frontend
```

### Problema: Migração falha

```bash
# Ver histórico de migrações
docker-compose exec backend alembic history

# Marcar como aplicada manualmente
docker-compose exec backend alembic stamp head

# Aplicar específica
docker-compose exec backend alembic upgrade <revision>
```

### Limpar e Reconstruir Tudo

```bash
# Parar todos os containers
docker-compose down

# Remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Limpar imagens
docker system prune -a

# Reconstruir do zero
docker-compose up -d --build
```

---

## Atualização da Aplicação

```bash
# 1. Backup do banco
./backup.sh

# 2. Pull das alterações
git pull origin main

# 3. Rebuild e restart
docker-compose up -d --build

# 4. Executar migrações
docker-compose exec backend alembic upgrade head

# 5. Verificar logs
docker-compose logs -f
```

---

## Configurações de Produção Recomendadas

### 1. Limites de Recursos (docker-compose.yml)

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 2. Restart Policies

```yaml
services:
  backend:
    restart: unless-stopped
  frontend:
    restart: unless-stopped
  db:
    restart: unless-stopped
```

### 3. Health Checks

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Suporte

Para problemas ou dúvidas:
- Abra uma [issue no GitHub](https://github.com/douglas-s29/lotofacil_web/issues)
- Consulte a [documentação](README.md)
