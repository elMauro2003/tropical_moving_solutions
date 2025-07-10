from django.shortcuts import render
from apps.general.forms import ContactForm
from django.http import JsonResponse
from django.views import View
from utils.osm_service import OSMService

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
        if form.is_valid() and distance <= 55.00:
            context['tags'] = 'success'
            context['tag_message'] = 'Quote Sent Successfully!'
            context['message'] = 'Quote Sent Successfully!'
        else:
            context['tags'] = 'error'
            context['tag_message'] = 'Something went wrong!'
        
    context['form'] = form
    return render(request, 'components/calculator_form.html', context)


def partial_load(request):
    size = request.GET.get('size')
    context = _show_pricing(request, size)
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