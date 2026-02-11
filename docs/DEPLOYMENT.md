# Guía de Deployment para Producción

## Preparación General

### 1. Checklist Pre-Deployment

Antes de desplegar a producción, verifica:

- [ ] `DEBUG=False` en `.env`
- [ ] `SECRET_KEY` única y segura generada
- [ ] `ALLOWED_HOSTS` configurado con tu dominio
- [ ] Base de datos PostgreSQL configurada
- [ ] Variables de entorno de Transbank (producción)
- [ ] Email SMTP configurado
- [ ] `PUBLIC_BASE_URL` apuntando a tu dominio
- [ ] Tests pasando: `python manage.py test`
- [ ] Archivos estáticos recolectados: `python manage.py collectstatic`

### 2. Generar SECRET_KEY Segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment en VPS/Servidor Dedicado

### Requisitos del Servidor

- Ubuntu 22.04 LTS o superior
- 1GB RAM mínimo (2GB recomendado)
- Python 3.10+
- PostgreSQL 14+
- Nginx
- Supervisor o systemd

### Paso 1: Preparar el Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx supervisor -y

# Instalar dependencias para Pillow
sudo apt install libjpeg-dev zlib1g-dev -y
```

### Paso 2: Configurar PostgreSQL

```bash
# Conectar a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE arenita_db;
CREATE USER arenita_user WITH PASSWORD 'tu_password_segura_aqui';
ALTER ROLE arenita_user SET client_encoding TO 'utf8';
ALTER ROLE arenita_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE arenita_user SET timezone TO 'America/Santiago';
GRANT ALL PRIVILEGES ON DATABASE arenita_db TO arenita_user;
\q
```

### Paso 3: Configurar la Aplicación

```bash
# Crear usuario para la aplicación
sudo adduser --system --group --home /opt/arenita arenita

# Clonar repositorio
cd /opt/arenita
sudo -u arenita git clone https://github.com/tu-usuario/arenita_ecommerce.git app
cd app

# Crear entorno virtual
sudo -u arenita python3 -m venv venv
sudo -u arenita venv/bin/pip install -r requirements.txt

# Crear archivo .env
sudo -u arenita nano .env
```

Configuración `.env` para producción:

```env
SECRET_KEY=tu-clave-secreta-generada
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://arenita_user:tu_password@localhost/arenita_db
PUBLIC_BASE_URL=https://tudominio.com
CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
CONTACT_EMAIL=ventas@tudominio.com
DEFAULT_FROM_EMAIL=noreply@tudominio.com

# Transbank Producción
TBK_ENV=production
TBK_COMMERCE_CODE=tu_codigo_comercio
TBK_API_KEY=tu_api_key
```

### Paso 4: Ejecutar Migraciones

```bash
sudo -u arenita venv/bin/python manage.py migrate
sudo -u arenita venv/bin/python manage.py collectstatic --noinput
sudo -u arenita venv/bin/python manage.py createsuperuser
```

### Paso 5: Configurar Gunicorn con Supervisor

Crear archivo `/etc/supervisor/conf.d/arenita.conf`:

```ini
[program:arenita]
command=/opt/arenita/app/venv/bin/gunicorn arenita.wsgi:application --bind 127.0.0.1:8000 --workers 3 --timeout 120
directory=/opt/arenita/app
user=arenita
autostart=true
autorestart=true
stderr_logfile=/var/log/arenita/error.log
stdout_logfile=/var/log/arenita/access.log
environment=LANG=es_CL.UTF-8,LC_ALL=es_CL.UTF-8
```

Crear directorio de logs:

```bash
sudo mkdir -p /var/log/arenita
sudo chown arenita:arenita /var/log/arenita
```

Iniciar supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start arenita
```

### Paso 6: Configurar Nginx

Crear archivo `/etc/nginx/sites-available/arenita`:

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /opt/arenita/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /opt/arenita/app/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Activar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/arenita /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 7: Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Renovación automática (ya viene configurada)
sudo systemctl status certbot.timer
```

## Deployment en Heroku

### Preparación

Asegúrate de tener el CLI de Heroku instalado:

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login
```

### Deployment

```bash
# Crear app
heroku create tu-app-arenita

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configurar variables de entorno
heroku config:set SECRET_KEY="tu-clave-secreta"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="tu-app-arenita.herokuapp.com"
heroku config:set PUBLIC_BASE_URL="https://tu-app-arenita.herokuapp.com"
heroku config:set CSRF_TRUSTED_ORIGINS="https://tu-app-arenita.herokuapp.com"

# Email (Gmail)
heroku config:set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
heroku config:set EMAIL_HOST="smtp.gmail.com"
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER="tu-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="tu-app-password"
heroku config:set CONTACT_EMAIL="ventas@tudominio.com"

# Transbank (opcional, usa credenciales de integración por defecto)
heroku config:set TBK_ENV=production
heroku config:set TBK_COMMERCE_CODE="tu_codigo"
heroku config:set TBK_API_KEY="tu_key"

# Deploy
git push heroku main

# Migrar base de datos
heroku run python manage.py migrate

# Crear superusuario
heroku run python manage.py createsuperuser

# Ver logs
heroku logs --tail
```

## Deployment en Railway

Railway detecta automáticamente proyectos Django.

### Deployment

1. Conecta tu repositorio de GitHub a Railway
2. Configura las variables de entorno en el dashboard:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=$RAILWAY_PUBLIC_DOMAIN`
   - `PUBLIC_BASE_URL=https://$RAILWAY_PUBLIC_DOMAIN`
   - `CSRF_TRUSTED_ORIGINS=https://$RAILWAY_PUBLIC_DOMAIN`
   - Variables de email y Transbank

3. Railway automáticamente:
   - Instala dependencias de `requirements.txt`
   - Crea base de datos PostgreSQL
   - Ejecuta el `Procfile`
   - Genera URL pública

4. Ejecutar migraciones manualmente (primera vez):
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

## Configuración de Transbank Producción

### Obtener Credenciales

1. Registrarse en https://www.transbankdevelopers.cl/
2. Solicitar afiliación comercial
3. Obtener `commerce_code` y `api_key`
4. Configurar en variables de entorno:

```env
TBK_ENV=production
TBK_COMMERCE_CODE=tu_codigo_comercio
TBK_API_KEY=tu_api_key_secreta
```

### Testing en Integración

Las credenciales de testing ya están configuradas:
- Commerce Code: `597055555532`
- API Key: `579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C`

### Tarjetas de Prueba

Para ambiente de integración:

| Tarjeta | Resultado |
|---------|-----------|
| 4051885600446623 | Aprobada |
| 5186059559590568 | Rechazada |

## Monitoreo y Mantenimiento

### Logs

```bash
# Supervisor logs
sudo tail -f /var/log/arenita/error.log
sudo tail -f /var/log/arenita/access.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Backup de Base de Datos

```bash
# Backup
sudo -u postgres pg_dump arenita_db > backup_$(date +%Y%m%d).sql

# Restore
sudo -u postgres psql arenita_db < backup_20260209.sql
```

### Actualizar Aplicación

```bash
cd /opt/arenita/app
sudo -u arenita git pull
sudo -u arenita venv/bin/pip install -r requirements.txt
sudo -u arenita venv/bin/python manage.py migrate
sudo -u arenita venv/bin/python manage.py collectstatic --noinput
sudo supervisorctl restart arenita
```

## Troubleshooting

### Error 502 Bad Gateway

```bash
# Verificar Gunicorn
sudo supervisorctl status arenita
sudo supervisorctl restart arenita

# Ver logs
sudo tail -f /var/log/arenita/error.log
```

### Archivos Estáticos No Se Cargan

```bash
# Recolectar estáticos
sudo -u arenita venv/bin/python manage.py collectstatic --noinput

# Verificar permisos
sudo chown -R arenita:arenita /opt/arenita/app/staticfiles
```

### Error de Base de Datos

```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Probar conexión
sudo -u arenita psql -U arenita_user -d arenita_db -h localhost
```

## Seguridad Post-Deployment

- [ ] Cambiar contraseñas por defecto
- [ ] Configurar firewall (ufw)
- [ ] Habilitar fail2ban
- [ ] Configurar backups automáticos
- [ ] Monitorear logs regularmente
- [ ] Mantener sistema actualizado
- [ ] Configurar alertas de errores
- [ ] Revisar logs de Transbank periódicamente
