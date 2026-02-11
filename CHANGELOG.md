# Changelog

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.1.0] - 2026-02-09

### Agregado
- README.md completo con instrucciones detalladas de instalación y deployment
- Tests básicos para shop y cart apps
- Archivo runtime.txt especificando Python 3.11.7
- Archivo CHANGELOG.md para tracking de cambios
- Validación de estado de orden en vista de pago
- Mensajes informativos al usuario durante el checkout

### Cambiado
- DEBUG=False por defecto en settings.py (más seguro)
- Email de contacto ahora usa variable de entorno CONTACT_EMAIL
- Carrito ya NO se limpia antes de confirmar pago (previene pérdida de datos)
- Procfile movido a la raíz del proyecto
- .env.example ampliamente mejorado con comentarios y ejemplos
- Mejorada configuración de email con variable CONTACT_EMAIL

### Corregido
- Procfile en ubicación incorrecta (ahora en raíz)
- Email hardcodeado en core/views.py (ahora usa settings.CONTACT_EMAIL)
- Carrito se limpiaba prematuramente causando pérdida de datos si el pago fallaba
- Falta de documentación sobre puerto de desarrollo (8000)

### Seguridad
- DEBUG ahora False por defecto para prevenir fugas de información en producción
- SECRET_KEY con advertencia clara en .env.example
- Mejor separación de configuraciones de desarrollo vs producción

## [1.0.0] - 2026-01-04

### Agregado
- Primera versión funcional del e-commerce
- Integración con Transbank Webpay Plus
- Sistema de carrito de compras
- Gestión de órdenes
- Catálogo de productos
- Formulario de contacto
- Panel de administración Django
- Soporte para imágenes de productos
- Sistema de categorías
