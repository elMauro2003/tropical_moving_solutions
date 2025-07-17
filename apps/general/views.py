from django.shortcuts import render, redirect
from apps.general.forms import ContactForm, ContactShortForm
from django.http import JsonResponse
from django.views import View
from utils.osm_service import OSMService
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    return render(request, 'base.html')

def calculator_page(request):
    return render(request, 'calculator.html')

def contact_page(request):
    return render(request, 'contact.html')

def send_quote(request):
    context = {}
    service = OSMService()
    distance = service.calculate_distance(
        request.POST.get('origin'),
        request.POST.get('destination')
    )
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        # Verificando si la alguna ruta es invalida dentro de Miami
        if distance is None:
            context['tags'] = 'error'
            context['tag_message'] = 'Make sure you entered a valid origin and destination inside Miami!'
            context['form'] = form
            return render(request, 'components/calculator_form.html', context)
        
        if form.is_valid() and distance <= 55.00:
            context['tags'] = 'success'
            context['tag_message'] = 'Quote Sent Successfully!'
            context['message'] = 'Quote Sent Successfully!'
        elif distance >= 55.00:
            context['tags'] = 'error'
            context['tag_message'] = 'Distance can only be lower than 50 miles!'
        else:
            context['tags'] = 'error'
            context['tag_message'] = 'Something went wrong!'
        
    context['form'] = form
    return render(request, 'components/calculator_form.html', context)


def send_mail_quote(request):
    context = {}
    service = OSMService()
    distance = service.calculate_distance(
        request.POST.get('origin'),
        request.POST.get('destination')
    )
    if request.method == 'POST':
        try:
            # Procesar datos
            name = request.POST.get('name')
            location = request.POST.get('location')
            origin = request.POST.get('origin')
            destination = request.POST.get('destination')
            phone = request.POST.get('phone')
            time = request.POST.get('time')
            date = request.POST.get('date')
            helpers = request.POST.get('helpers')
            special_item = request.POST.get('special_item')
            size = request.POST.get('size')
            
                
            # Crear contenido del email (HTML)
            context = {
                'name': name,
                'location': location,
                'origin': origin,
                'destination': destination,
                'phone': phone,
                'time': time,
                'date': date,
                'helpers': helpers,
                'special_item': special_item,
                'size': size,
                'distance': distance,
                'total_amount': _show_pricing(request, size).get('total_amount', 0),
                'white_glove': _show_pricing(request, size).get('white_glove', 0),
                'packing': _show_pricing(request, size).get('packing', 0),
                
            }
            content = render_to_string('components/mail/email_quote.html', context)
                
            # Enviar email
            email = EmailMessage(
                f'Contact message from: {name}',
                content,
                settings.EMAIL_HOST_USER,
                [settings.DESTINATARIO_EMAIL],
            )
            email.content_subtype = "html"  # Habilitar HTML
            email.send()
            context['tags'] = 'success'
            context['tag_message'] = 'Quote sent successfully!'
        except Exception as e:
                context['tags'] = 'error'
                context['tag_message'] = f'Error: {str(e)}'
    
    context['form'] = ''
    return render(request, 'components/calculator_form.html', context)
    
    

def partial_load(request):
    
    # Procesar datos
    name = request.GET.get('name')
    location = request.GET.get('location')
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    phone = request.GET.get('phone')
    time = request.GET.get('time')
    date = request.GET.get('date')
    helpers = request.GET.get('helpers')
    special_item = request.GET.get('special_item')
    size = request.GET.get('size')
    
    # Pasar al contexto
    context = _show_pricing(request, size)
    context['name'] = name
    context['location'] = location
    context['origin'] = origin
    context['destination'] = destination
    context['phone'] = phone
    context['time'] = time
    context['date'] = date
    context['helpers'] = helpers
    context['special_item'] = special_item
    context['size'] = size
    
    return render(request, 'components/price_modal.html', context)

def _show_pricing(request, size):
    context = {}
    if size == 'studio':
        context['base_price'] = '240'
        context['packing'] = '150'
        context['white_glove'] = '300'
    elif size == '1bed':
        context['base_price'] = '300'
        context['white_glove'] = '500'
        context['packing'] = '250'
    elif size == '2bed':
        context['base_price'] = '585'
        context['white_glove'] = '700'
        context['packing'] = '350'
    elif size == '3bed':
        context['base_price'] = '1020'
        context['white_glove'] = '900'
        context['packing'] = '550'
    elif size == '4bed':
        context['base_price'] = '1350'
        context['packing'] = '750'
        context['white_glove'] = '1300'
    
    context['total_amount'] = float(context.get('base_price', 0)) + float(context.get('packing', 0)) + float(context.get('white_glove', 0)) + float(250)
    return context
        
    

class DistanceView(View):
    def get(self, request):
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')

        if not origin or not destination:
            return JsonResponse(
                {'error': 'Parameters "origin" and "destination" are required'},
                status=400
            )

        service = OSMService()
        distance = service.calculate_distance(origin, destination)

        if distance is not None:
            origin_data = service.geocode(origin)
            dest_data = service.geocode(destination)
            return JsonResponse({
                'origin': origin_data['display_name'],
                'destination': dest_data['display_name'],
                'distance_miles': distance,
                'status': 'success'
            })
        return JsonResponse(
            {'error': 'Could not calculate distance for given locations'},
            status=404
        )
        

import os
def send_mail(request):
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
                content = render_to_string('components/mail/email.html', context)

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