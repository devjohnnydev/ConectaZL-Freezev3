#!/usr/bin/env python
"""
Script de inicialização automática do banco de dados PostgreSQL para Railway.
Este script executa as migrations e cria dados iniciais se necessário.
"""
import os
import sys
import django

def main():
    """Inicializa o banco de dados PostgreSQL."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_noticias.settings')
    django.setup()

    from django.core.management import execute_from_command_line
    from django.contrib.auth import get_user_model

    print("🚀 Iniciando configuração do banco de dados PostgreSQL...")

    print("\n📦 Aplicando migrações...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    print("\n📂 Coletando arquivos estáticos...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        print("\n👤 Verificando credenciais para criação de superusuário...")
        
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        if not all([admin_username, admin_email, admin_password]):
            print("⚠️  AVISO: Variáveis de ambiente de superusuário não definidas.")
            print("⚠️  Configure DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL e DJANGO_SUPERUSER_PASSWORD")
            print("⚠️  Ou crie o superusuário manualmente com: python manage.py createsuperuser")
            print("\n✨ Banco de dados inicializado (sem superusuário)!")
        else:
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            print(f"✅ Superusuário '{admin_username}' criado com sucesso!")
            print(f"📧 Email: {admin_email}")
            print("⚠️  Altere a senha após o primeiro login!")
            print("\n✨ Banco de dados inicializado com sucesso!")
    else:
        print("\n✅ Superusuário já existe, pulando criação...")
        print("\n✨ Banco de dados inicializado com sucesso!")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
