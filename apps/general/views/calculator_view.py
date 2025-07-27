from django.shortcuts import render
from apps.general.forms import ContactForm
from utils.osm_service import OSMService
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Instanciar el servicio de OSM
service = OSMService()

def check_quote_validation(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form'] = form
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            
            distance = service.calculate_distance(origin, destination)
            #print(f"Distance: {distance}")
            
            if distance is None:
                    context.update({
                        'tags': 'error',
                        'tag_message': 'Could not validate addresses'
                    })
            elif distance > 55:
                context.update({
                    'tags': 'error',
                    'tag_message': 'Distance exceeds maximum allowed (55 miles)',
                    'distance': distance
                })
            else:
                context.update({
                    'tags': 'success',
                    'tag_message': 'Quote validated successfully!',
                    'distance': distance
                })
    
    return render(request, 'components/calculator/calculator_form.html', context)

def calculator_send_mail_quote(request):
    context = {}
    
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
            distance = request.POST.get('distance')  
                
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
            content = render_to_string('components/mail/quote_email.html', context)
                
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
    return render(request, 'components/calculator/calculator_form.html', context)

def calculator_show_price_modal(request):
    try:
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
        distance = request.POST.get('distance')
        
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
        context['distance'] = distance
    except Exception as e:
        context['tags'] = 'error'
        context['tag_message'] = f'Error: {str(e)}'
        
    return render(request, 'components/calculator/price_modal.html', context)

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
