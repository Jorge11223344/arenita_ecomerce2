# 🐾 Arenita E-commerce

E-commerce moderno para venta de arena sanitaria para gatos, desarrollado con Django 6.0 y integración con Transbank Webpay Plus.

## 🚀 Características

- ✅ Catálogo de productos con imágenes y descripciones
- 🛒 Carrito de compras con gestión de sesiones
- 💳 Integración con Transbank Webpay Plus
- 📧 Sistema de notificaciones por email
- 📦 Gestión de órdenes y estados
- 🎨 Interfaz responsive y moderna
- 🔒 Seguridad y validaciones implementadas

## 📋 Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git
- PostgreSQL (opcional, recomendado para producción)

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/arenita_ecommerce.git
cd arenita_ecommerce
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta los valores:

```bash
cp .env.example .env
```

Edita `.env` con tus configuraciones:

```env
SECRET_KEY=tu-clave-secreta-aleatoria-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
CONTACT_EMAIL=tu-email@ejemplo.com
PUBLIC_BASE_URL=http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

**Importante:** En producción cambia `DEBUG=False` y configura tu dominio real.

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Abre tu navegador en: **http://localhost:8000**

## 🏭 Configuración para Producción

### PostgreSQL

1. Instala PostgreSQL en tu servidor
2. Crea una base de datos:

```sql
CREATE DATABASE arenita_db;
CREATE USER arenita_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE arenita_db TO arenita_user;
```

3. Configura en `.env`:

```env
DATABASE_URL=postgresql://arenita_user:tu_password@localhost:5432/arenita_db
```

### Transbank Webpay Plus

#### Modo Integración (Testing)

Las credenciales de prueba están preconfiguradas. No necesitas hacer nada.

#### Modo Producción

1. Obtén tus credenciales en [Transbank Developers](https://www.transbankdevelopers.cl/)
2. Configura en `.env`:

```env
TBK_ENV=production
TBK_COMMERCE_CODE=tu_codigo_comercio
TBK_API_KEY=tu_api_key
```

### Email

Configura tu servidor SMTP en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
CONTACT_EMAIL=ventas@tudominio.cl
DEFAULT_FROM_EMAIL=noreply@tudominio.cl
```

### Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

## 🚢 Deployment

### Heroku

```bash
heroku create tu-app-arenita
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY=tu-clave
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=tu-app-arenita.herokuapp.com
git push heroku main
heroku run python manage.py migrate
```

### Railway

1. Conecta tu repositorio de GitHub
2. Configura las variables de entorno en el dashboard
3. Railway detectará automáticamente Django y lo desplegará

## 📁 Estructura del Proyecto

```
arenita_ecommerce/
├── arenita/              # Configuración principal
├── cart/                 # App de carrito de compras
├── core/                 # App principal (inicio, contacto)
├── orders/               # App de órdenes
├── payments/             # App de pagos (Transbank)
├── shop/                 # App de tienda y productos
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Templates HTML
├── media/                # Archivos subidos por usuarios
├── manage.py             # CLI de Django
├── requirements.txt      # Dependencias Python
├── Procfile             # Para deployment en Heroku/Railway
├── runtime.txt          # Versión de Python
└── .env.example         # Ejemplo de variables de entorno
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test shop
```

## 🔐 Seguridad

- ✅ SECRET_KEY única por entorno
- ✅ DEBUG=False en producción
- ✅ ALLOWED_HOSTS configurado
- ✅ CSRF protection habilitado
- ✅ Validaciones en formularios

## 📝 Variables de Entorno

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| SECRET_KEY | Clave secreta de Django | (generada) | Sí |
| DEBUG | Modo debug | False | Sí |
| ALLOWED_HOSTS | Dominios permitidos | ejemplo.com | Sí |
| DATABASE_URL | URL de base de datos | postgresql://... | No |
| CONTACT_EMAIL | Email para contacto | info@ejemplo.cl | Sí |
| PUBLIC_BASE_URL | URL pública del sitio | https://ejemplo.com | Sí |

## 📊 Admin Panel

Accede al panel de administración en: `/admin/`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
