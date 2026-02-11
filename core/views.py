from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import smtplib
from .forms import ContactForm

def inicio(request):
    return render(request, 'core/inicio.html')

def acerca(request):
    return render(request, 'core/acerca.html')

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = f"Contacto Arenita - {data['nombre']}"
            body = (
                f"Nombre: {data['nombre']}\n"
                f"Email: {data['email']}\n\n"
                f"Mensaje:\n{data['mensaje']}"
            )

            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  # Usa variable de entorno
                )
                messages.success(request, "🎉 ¡Gracias! Te responderemos pronto.")
            except (BadHeaderError, smtplib.SMTPException, ConnectionRefusedError) as e:
                # Evita 500 y da feedback
                messages.error(request, "😿 No se pudo enviar tu mensaje. Intenta más tarde.")
                # Opcional: loguear e para depurar

            return redirect('contacto')
    else:
        form = ContactForm()

    return render(request, 'core/contacto.html', {'form': form})
