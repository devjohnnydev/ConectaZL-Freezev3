# 🚂 Deploy no Railway - Conecta ZL

Guia completo para fazer deploy do Conecta ZL no Railway com PostgreSQL.

## 📋 Pré-requisitos

- Conta no [Railway](https://railway.app)
- Repositório no GitHub com o código
- Conta no GitHub conectada ao Railway

## 🚀 Passo a Passo

### 1. Preparação do Repositório

O projeto já está configurado com os arquivos necessários:
- ✅ `Procfile` - Define o comando para iniciar a aplicação
- ✅ `runtime.txt` - Especifica a versão do Python
- ✅ `railway.json` - Configurações de build e deploy
- ✅ `requirements.txt` - Dependências do projeto
- ✅ `init_db.py` - Script de inicialização do banco de dados

### 2. Deploy no Railway

#### Opção A: Via Dashboard (Recomendado)

1. Acesse [railway.app](https://railway.app) e faça login
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Escolha o repositório `conecta-zl`
5. Railway detectará automaticamente que é um projeto Django

#### Opção B: Via Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar projeto
railway init

# Deploy
railway up
```

### 3. Adicionar PostgreSQL

#### Via Dashboard:
1. No projeto, clique em **"+ New"**
2. Selecione **"Database"**
3. Escolha **"Add PostgreSQL"**
4. Railway criará automaticamente a variável `DATABASE_URL`

#### Via CLI:
```bash
railway add
# Selecione PostgreSQL
```

### 4. Configurar Variáveis de Ambiente

No Railway Dashboard → **Variables**, adicione:

```env
# Obrigatórias
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-app.up.railway.app

# DATABASE_URL é criado automaticamente pelo PostgreSQL
# Não precisa configurar manualmente

# Opcionais - para criar superusuário automaticamente
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@conectazl.com
DJANGO_SUPERUSER_PASSWORD=SuaSenhaSegura123!
```

**⚠️ IMPORTANTE:**
- Gere um SECRET_KEY seguro com: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Substitua `seu-app.up.railway.app` pelo domínio real do seu projeto
- Nunca commite credenciais no código!

### 5. Inicializar o Banco de Dados

Após o primeiro deploy:

#### Via Railway CLI:
```bash
# Conectar ao projeto
railway link

# Executar script de inicialização
railway run python init_db.py

# Ou executar migrations manualmente
railway run python manage.py migrate

# Criar superusuário
railway run python manage.py createsuperuser
```

#### Automático:
O `railway.json` está configurado para executar migrations automaticamente em cada deploy via `startCommand`.

### 6. Verificar o Deploy

1. Acesse o domínio do Railway (ex: `https://seu-app.up.railway.app`)
2. Verifique se a página inicial carrega
3. Acesse o admin: `https://seu-app.up.railway.app/admin`
4. Faça login com o superusuário criado

### 7. Configurar Domínio Customizado (Opcional)

1. No Railway Dashboard → **Settings**
2. Clique em **"Generate Domain"** ou **"Custom Domain"**
3. Se usar domínio customizado, adicione-o em `ALLOWED_HOSTS` nas variáveis

## 🔧 Comandos Úteis

### Ver Logs
```bash
railway logs
```

### Conectar ao Banco de Dados
```bash
railway run psql $DATABASE_URL
```

### Executar Comandos Django
```bash
# Migrations
railway run python manage.py migrate

# Criar superusuário
railway run python manage.py createsuperuser

# Collectstatic (já executado automaticamente)
railway run python manage.py collectstatic --noinput

# Shell
railway run python manage.py shell
```

### Fazer Backup do Banco
```bash
# Dump do banco
railway run pg_dump $DATABASE_URL > backup.sql

# Restaurar backup
railway run psql $DATABASE_URL < backup.sql
```

## 📊 Monitoramento

### Logs em Tempo Real
No Dashboard: **Deployments** → **View Logs**

### Métricas
Railway fornece métricas de:
- CPU
- Memória
- Requisições
- Tempo de resposta

## 🐛 Troubleshooting

### Erro: "DisallowedHost"
- Verifique se `ALLOWED_HOSTS` contém seu domínio Railway
- Exemplo: `seu-app.up.railway.app`

### Erro: "Static files not found"
- Execute: `railway run python manage.py collectstatic --noinput`
- Verifique se `whitenoise` está em `requirements.txt`

### Erro: "Database connection failed"
- Verifique se o serviço PostgreSQL está ativo
- Confirme que `DATABASE_URL` existe nas variáveis

### Build falha
- Verifique `requirements.txt` está atualizado
- Veja os logs de build no Dashboard
- Confirme que `runtime.txt` tem Python 3.11

## 🔐 Segurança em Produção

Após o deploy, certifique-se de:

- ✅ `DEBUG=False` em produção
- ✅ `SECRET_KEY` único e seguro
- ✅ `ALLOWED_HOSTS` restrito ao seu domínio
- ✅ HTTPS habilitado (Railway faz automaticamente)
- ✅ Alterar senha padrão do superusuário
- ✅ Fazer backup regular do banco de dados

## 📚 Recursos

- [Documentação Railway](https://docs.railway.com)
- [Railway Django Guide](https://docs.railway.com/guides/django)
- [Railway PostgreSQL](https://docs.railway.com/databases/postgresql)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## 🎉 Pronto!

Seu Conecta ZL agora está rodando no Railway com PostgreSQL! 🚀

Para atualizações futuras, basta fazer push para o GitHub e Railway fará deploy automaticamente.
