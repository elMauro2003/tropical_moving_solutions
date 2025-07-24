from django.shortcuts import render
from apps.general.forms import ContactShortForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def contact_form_send_mail(request):
    context = {}
    if request.method == 'POST':
        form = ContactShortForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                date = form.cleaned_data['date']
                message = form.cleaned_data['message']

                # Crear contenido del email (HTML)
                context = {
                    'name': name,
                    'email': email,
                    'date': date,
                    'message': message,
                }
                content = render_to_string('components/mail/contact_email.html', context)

                # Enviar email con EmailMessage (forma correcta)
                email_msg = EmailMessage(
                    f'Contact message from: {name}',
                    content,
                    settings.EMAIL_HOST_USER,
                    [settings.DESTINATARIO_EMAIL],
                )
                email_msg.content_subtype = "html"
                email_msg.send()  # No se usa fail_silently aquí

                context['tags'] = 'success'
                context['tag_message'] = 'Message delivered successfully!'
            except Exception as e:
                context['tags'] = 'error'
                context['tag_message'] = f'Error sending email: {str(e)}'
        else:
            context['tags'] = 'error'
            context['tag_message'] = 'Form is not valid!'
    if form.errors:
        context['form'] = form
    else:
        context['form'] = ''
    return render(request, 'components/contact_form.html', context)