from django.urls import path, include
from apps.general.views.home import index, calculator_page, contact_page
from apps.general.views.contact_view import contact_form_send_mail
from apps.general.views.calculator_view import check_quote_validation, calculator_send_mail_quote, calculator_show_price_modal


urlpatterns = [
    path('', index, name='index'),
    path('calculator/', calculator_page, name='calculator_page'),
    path('calculator-plan-type/<str:plan_type>/', calculator_page, name='calculator_page_with_param'),
    path('contact/', contact_page, name='contact_page'),
    path('check-quote-validation/', check_quote_validation, name='check_quote_validation'),
    path('calculator-show-price-modal/', calculator_show_price_modal, name='calculator_show_price_modal'),
    path('contact-form-send-mail/', contact_form_send_mail, name='contact_form_send_mail'),
    path('calculator-send-mail-quote/', calculator_send_mail_quote, name='calculator_send_mail_quote'),
]
