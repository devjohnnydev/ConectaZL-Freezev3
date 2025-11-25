# Conecta ZL - Portal de Notícias

## Project Overview
Community news portal developed in Django for São Paulo's East Zone (Zona Leste). Allows local journalists to publish content and enables community interaction through comments and likes.

## Recent Changes
- **2025-11-25**: Configured for Replit environment and Railway deployment
  - Installed Python 3.11 and all dependencies
  - Configured workflow to run Django development server on port 5000
  - Set up environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
  - Ran database migrations
  - Configured deployment with Gunicorn for Replit and Railway
  - Added Railway deployment support with PostgreSQL
  - Added WhiteNoise for static file serving
  - Created automatic database initialization script
  - Added .pythonlibs and .cache to .gitignore

## Project Architecture
- **Framework**: Django 5.2.8
- **Frontend**: HTML5, CSS3, JavaScript with TailwindCSS via CDN
- **Database**: SQLite (development), PostgreSQL (production - Railway)
- **Static Files**: WhiteNoise for efficient serving
- **WSGI Server**: Gunicorn (production)
- **Key Features**:
  - User roles: Readers, Journalists, Administrators
  - Article creation with rich text editor (Summernote)
  - Geolocation with interactive maps (Folium)
  - Comment system with moderation
  - Tags and categorization (django-taggit)
  - REST API (Django REST Framework)

## Configuration

### Environment Variables (shared)
- `SECRET_KEY`: Django secret key for security
- `DEBUG`: Set to True for development, False for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: PostgreSQL connection string (Railway auto-provides)

### Workflow (Replit)
- **Django Server**: Runs the development server
  - Command: `python3.11 manage.py runserver 0.0.0.0:5000`
  - Port: 5000 (webview)
  - Note: Must use python3.11 explicitly due to Replit environment

### Deployment

#### Replit
- **Type**: Autoscale
- **Server**: Gunicorn
- **Command**: `gunicorn --bind=0.0.0.0:5000 --reuse-port portal_noticias.wsgi:application`

#### Railway (Recommended for Production)
- **Platform**: Railway.app
- **Database**: PostgreSQL (automatic provisioning)
- **Static Files**: WhiteNoise
- **Configuration Files**:
  - `Procfile`: Defines web server command
  - `runtime.txt`: Specifies Python 3.11.13
  - `railway.json`: Build and deploy configuration
  - `init_db.py`: Automatic database initialization script
- **Documentation**: See `DEPLOY_RAILWAY.md` for complete guide

## Apps Structure
- **users/**: User authentication and profiles with role-based permissions
- **articles/**: News articles with approval workflow, likes, and views tracking
- **comments/**: Comment system with moderation
- **api/**: REST API endpoints
- **portal_noticias/**: Main project configuration

## Deployment Files
- **Procfile**: Railway/Heroku process configuration
- **runtime.txt**: Python version specification
- **railway.json**: Railway-specific build and deploy settings
- **init_db.py**: Automated database setup script
- **DEPLOY_RAILWAY.md**: Complete deployment guide for Railway

## User Preferences
None specified yet.

## Important Notes
- The project uses Python 3.11 specifically - do not upgrade to Python 3.12 as it causes numpy compatibility issues
- Database auto-switches between SQLite (local) and PostgreSQL (production) based on DATABASE_URL
- WhiteNoise handles static file serving in production
- Static files are served from `/static/` directory
- Media uploads go to `/media/` directory
- CSRF trusted origins include *.replit.dev, *.replit.app, and *.up.railway.app
- Automatic database initialization creates superuser if none exists
- For Railway deployment, see DEPLOY_RAILWAY.md for step-by-step instructions
