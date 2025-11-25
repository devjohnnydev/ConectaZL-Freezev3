# 📰 Conecta ZL - Portal de Notícias da Zona Leste

<div align="center">
  <img src="static/images/logo_new.png" alt="Conecta ZL Logo" width="200"/>
  
  **Notícias que nos unem**
  
  Portal comunitário de notícias desenvolvido em Django, focado em conectar a comunidade da Zona Leste de São Paulo com informações locais relevantes.
</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Rodar no VSCode](#-como-rodar-no-vscode)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API REST](#-api-rest)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Comandos Úteis](#-comandos-úteis)
- [Permissões e Roles](#-permissões-e-roles)
- [Contribuindo](#-contribuindo)

---

## 🎯 Sobre o Projeto

O **Conecta ZL** é uma plataforma digital que conecta a comunidade da Zona Leste com notícias e acontecimentos do bairro. O projeto permite que jornalistas locais publiquem conteúdo e que a comunidade interaja através de comentários e curtidas.

### Destaques

- ✨ **Design Moderno**: Interface inspirada em redes sociais com paleta roxa (#8B3DFF)
- 🗺️ **Geolocalização**: Marcação de localização nas notícias com mapas interativos
- 💬 **Engajamento Comunitário**: Sistema de comentários e curtidas
- 🔐 **Sistema de Aprovação**: Moderação de conteúdo por administradores
- 📱 **Responsivo**: Funciona perfeitamente em desktop e mobile
- 🚀 **API REST**: Integração fácil com outras aplicações

---

## ✨ Funcionalidades

### Para Leitores
- ✅ Visualizar notícias publicadas e aprovadas
- ✅ Comentar em artigos (com moderação)
- ✅ Curtir notícias
- ✅ Visualizar perfis de jornalistas
- ✅ Explorar notícias por tags e localização
- ✅ Ver mapas interativos das notícias geolocalizadas

### Para Jornalistas
- ✅ Criar e editar artigos com editor rico (Summernote)
- ✅ Upload de imagens
- ✅ Adicionar tags e geolocalização
- ✅ Gerenciar próprios artigos
- ✅ Acompanhar estatísticas (visualizações, curtidas, comentários)
- ✅ Editar perfil com foto de banner e avatar

### Para Administradores
- ✅ Dashboard administrativo completo
- ✅ Aprovar/rejeitar artigos de jornalistas
- ✅ Moderar comentários
- ✅ Gerenciar usuários
- ✅ Visualizar estatísticas em tempo real
- ✅ Acesso total ao painel Django Admin

### Sistema de Aprovação
- 📝 Artigos de jornalistas são criados com status "pendente"
- ✔️ Administradores aprovam ou rejeitam com notas de feedback
- 🚫 Apenas artigos aprovados aparecem no feed público
- 📊 Dashboard mostra artigos pendentes, aprovados e rejeitados

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 4.2.7** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados (Neon em produção)
- **SQLite** - Banco de dados (desenvolvimento local)

### Frontend
- **HTML5, CSS3, JavaScript Vanilla**
- **Google Fonts** - Almarai (títulos) e Kameron (subtítulos)
- **TailwindCSS** via CDN

### Integrações e Bibliotecas
- **django-summernote** - Editor de texto rico WYSIWYG
- **django-taggit** - Sistema de tags
- **folium** - Mapas interativos
- **Pillow** - Processamento de imagens
- **python-decouple** - Gerenciamento de variáveis de ambiente
- **psycopg2-binary** - Adapter PostgreSQL

---

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (gerenciador de pacotes Python)
- **Git** ([Download](https://git-scm.com/downloads))
- **PostgreSQL** (opcional, para produção - [Download](https://www.postgresql.org/download/))

### Verificar instalações

```bash
python --version
pip --version
git --version
```

---

## 🚀 Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd conecta-zl
```

### 2. Crie um Ambiente Virtual

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Desenvolvimento Local (SQLite)
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# Produção (PostgreSQL) - Opcional
DATABASE_URL=postgresql://usuario:senha@host:porta/database
PGDATABASE=nome_do_banco
PGUSER=usuario
PGPASSWORD=senha
PGHOST=host
PGPORT=5432
```

### 5. Execute as Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções e insira:
- Username (ex: admin)
- Email (opcional)
- Password (ex: admin123)

### 7. Colete Arquivos Estáticos (Produção)

```bash
python manage.py collectstatic --noinput
```

### 8. Execute o Servidor

```bash
python manage.py runserver 0.0.0.0:5000
```

Acesse: **http://localhost:5000**

---

## 💻 Como Rodar no VSCode

### 1. Abra o Projeto no VSCode

```bash
code .
```

### 2. Instale Extensões Recomendadas

- **Python** (Microsoft)
- **Django** (Baptiste Darthenay)
- **Pylance** (Microsoft)
- **SQLite Viewer** (opcional)

### 3. Configure o Interpretador Python

1. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
2. Digite: "Python: Select Interpreter"
3. Selecione o ambiente virtual criado (`venv`)

### 4. Configure o Terminal Integrado

Abra o terminal integrado (`Ctrl+`` ` ou View > Terminal) e ative o ambiente virtual:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 5. Execute Comandos Django no Terminal

```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver 0.0.0.0:5000
```

### 6. Depuração (Debug)

Crie um arquivo `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "0.0.0.0:5000"
            ],
            "django": true,
            "justMyCode": true
        }
    ]
}
```

Agora você pode iniciar o debug pressionando `F5`!

### 7. Acesse a Aplicação

- **Frontend**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **API**: http://localhost:5000/api

---

## 📁 Estrutura do Projeto

```
conecta-zl/
├── portal_noticias/          # Projeto Django principal
│   ├── settings.py           # Configurações do projeto
│   ├── urls.py               # URLs principais
│   └── wsgi.py               # WSGI para produção
│
├── users/                    # App de usuários e perfis
│   ├── models.py             # Profile com roles (leitor, jornalista, admin)
│   ├── views.py              # Login, registro, perfil
│   ├── admin.py              # Admin customizado
│   └── templates/            # Templates de usuário
│
├── articles/                 # App de artigos/notícias
│   ├── models.py             # Article, Like
│   ├── views.py              # CRUD de artigos
│   ├── admin_views.py        # Dashboard administrativo
│   ├── admin.py              # Admin com Summernote
│   └── templates/            # Templates de artigos
│
├── comments/                 # App de comentários
│   ├── models.py             # Comment com moderação
│   ├── views.py              # Criar/deletar comentários
│   └── admin.py              # Moderação
│
├── api/                      # API REST
│   ├── serializers.py        # Serializers DRF
│   ├── views.py              # ViewSets
│   ├── permissions.py        # Permissões customizadas
│   └── urls.py               # Rotas da API
│
├── templates/                # Templates globais
│   ├── base.html             # Template base
│   └── ...
│
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── style.css         # Estilos principais
│   ├── images/               # Imagens do site
│   └── js/                   # Scripts JavaScript
│
├── media/                    # Uploads de usuários
│   ├── articles/             # Imagens de artigos
│   ├── profiles/             # Fotos de perfil
│   └── banners/              # Banners de perfil
│
├── manage.py                 # CLI do Django
├── requirements.txt          # Dependências Python
├── .env                      # Variáveis de ambiente (criar)
└── README.md                 # Este arquivo
```

---

## 🔌 API REST

A API REST está disponível em `/api/` e utiliza Django REST Framework.

### Base URL
```
http://localhost:5000/api/
```

### Endpoints

#### **Artigos**

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/api/articles/` | Lista todos os artigos publicados | Não |
| `GET` | `/api/articles/{slug}/` | Detalhe de um artigo | Não |
| `POST` | `/api/articles/` | Criar artigo | Jornalista/Admin |
| `PUT` | `/api/articles/{slug}/` | Atualizar artigo | Autor/Admin |
| `DELETE` | `/api/articles/{slug}/` | Deletar artigo | Autor/Admin |

**Exemplo de Requisição (GET):**
```bash
curl http://localhost:5000/api/articles/
```

**Exemplo de Resposta:**
```json
{
  "count": 10,
  "next": "http://localhost:5000/api/articles/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Nova praça inaugurada no bairro",
      "slug": "nova-praca-inaugurada-no-bairro",
      "excerpt": "Comunidade celebra nova área de lazer...",
      "image": "http://localhost:5000/media/articles/praca.jpg",
      "author": "jornalista1",
      "created_at": "2025-11-18T10:30:00Z",
      "views": 150,
      "total_likes": 23,
      "tags": ["comunidade", "lazer"]
    }
  ]
}
```

#### **Comentários**

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/api/comments/` | Lista comentários aprovados | Não |
| `POST` | `/api/comments/` | Criar comentário | Sim |

**Exemplo de Criação de Comentário:**
```bash
curl -X POST http://localhost:5000/api/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token seu-token-aqui" \
  -d '{
    "article": 1,
    "content": "Ótima notícia!"
  }'
```

### Filtros e Ordenação

**Busca:**
```
/api/articles/?search=praça
```

**Ordenação:**
```
/api/articles/?ordering=-created_at
/api/articles/?ordering=views
```

**Paginação:**
```
/api/articles/?page=2
```

**Combinação:**
```
/api/articles/?search=comunidade&ordering=-views&page=1
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Ambiente
DEBUG=True

# Segurança
SECRET_KEY=sua-chave-secreta-super-segura-aqui

# Banco de Dados PostgreSQL (Produção)
DATABASE_URL=postgresql://usuario:senha@localhost:5432/conecta_zl
PGDATABASE=conecta_zl
PGUSER=seu_usuario
PGPASSWORD=sua_senha
PGHOST=localhost
PGPORT=5432

# Hosts Permitidos (separados por vírgula)
ALLOWED_HOSTS=localhost,127.0.0.1,.replit.dev,.replit.app
```

### Para Desenvolvimento Local (SQLite)

Se quiser usar SQLite em desenvolvimento, basta definir:

```env
DEBUG=True
SECRET_KEY=chave-de-desenvolvimento
```

O projeto automaticamente usará SQLite se as variáveis PostgreSQL não estiverem definidas.

---

## ⚙️ Comandos Úteis

### Gerenciamento Django

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor de desenvolvimento
python manage.py runserver 0.0.0.0:5000

# Abrir shell interativo
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Criar dump do banco de dados
python manage.py dumpdata > backup.json

# Carregar dados de um dump
python manage.py loaddata backup.json
```

### Limpeza e Manutenção

```bash
# Limpar sessões expiradas
python manage.py clearsessions

# Verificar integridade do projeto
python manage.py check

# Listar todas as URLs
python manage.py show_urls  # (requer django-extensions)
```

### Testes

```bash
# Rodar todos os testes
python manage.py test

# Testar app específico
python manage.py test articles

# Com verbosidade
python manage.py test --verbosity=2
```

---

## 👥 Permissões e Roles

O projeto possui 3 tipos de usuários com permissões diferentes:

### 🔵 Leitor (role='leitor')

**Pode:**
- ✅ Visualizar artigos publicados e aprovados
- ✅ Comentar em artigos (sujeito a moderação)
- ✅ Curtir artigos
- ✅ Deletar próprios comentários
- ✅ Visualizar perfis de jornalistas

**Não pode:**
- ❌ Criar artigos
- ❌ Editar artigos
- ❌ Acessar dashboard administrativo

### 📝 Jornalista (role='jornalista')

**Pode:**
- ✅ Todas as permissões de Leitor
- ✅ Criar artigos (status: pendente)
- ✅ Editar próprios artigos
- ✅ Deletar próprios artigos
- ✅ Upload de imagens
- ✅ Adicionar tags e geolocalização
- ✅ Editar perfil (foto de banner, avatar, bio, localização)

**Não pode:**
- ❌ Aprovar próprios artigos
- ❌ Editar artigos de outros
- ❌ Moderar comentários
- ❌ Acessar dashboard administrativo

### 👑 Administrador (role='admin')

**Pode:**
- ✅ Todas as permissões de Jornalista
- ✅ Aprovar/rejeitar artigos
- ✅ Criar artigos já aprovados
- ✅ Editar/deletar qualquer artigo
- ✅ Moderar comentários
- ✅ Gerenciar usuários
- ✅ Acessar dashboard administrativo
- ✅ Acesso total ao Django Admin Panel
- ✅ Visualizar estatísticas em tempo real

### Como Definir Roles

1. **Via Django Admin** (`/admin/`):
   - Login como superusuário
   - Users → Profile
   - Edite o campo "Role"

2. **Durante Registro**:
   - Usuários escolhem seu perfil no formulário de cadastro
   - Por padrão: "Leitor"

3. **Via Shell**:
```python
python manage.py shell

from users.models import Profile
profile = Profile.objects.get(user__username='usuario')
profile.role = 'jornalista'  # ou 'admin'
profile.save()
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Commit** suas mudanças:
   ```bash
   git commit -m "Add: Minha nova feature"
   ```
4. **Push** para a branch:
   ```bash
   git push origin feature/minha-feature
   ```
5. Abra um **Pull Request**

### Padrões de Código

- Siga a [PEP 8](https://peps.python.org/pep-0008/) para código Python
- Use nomes descritivos para variáveis e funções
- Comente código complexo
- Escreva testes para novas funcionalidades
- Atualize a documentação quando necessário

### Reportar Bugs

Abra uma **issue** descrevendo:
- O que aconteceu
- O que era esperado
- Passos para reproduzir
- Screenshots (se aplicável)

---

## 📄 Licença

Este projeto é um software livre para fins educacionais e comunitários.

---

## 📞 Contato

- **Website**: [Conecta ZL](https://conecta-zl.replit.app)
- **Email**: contato@conectazl.com.br

---

## 🙏 Agradecimentos

Desenvolvido com ❤️ para a comunidade da Zona Leste de São Paulo.

**Conecta ZL - Notícias que nos unem!**

---

<div align="center">
  <p>⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!</p>
</div>
