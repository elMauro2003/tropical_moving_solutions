from django import forms
from apps.general.models import Contact, ContactShort

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name', 'location', 'origin', 'destination', 'phone', 
            'time', 'date', 'size', 'helpers', 'special_item'
        ]
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo dígitos.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("El número de teléfono debe tener entre 10 y 15 dígitos.")
        return phone

    def clean_helpers(self):
        helpers = self.cleaned_data.get('helpers')
        if helpers < 1:
            raise forms.ValidationError("Debe haber al menos un ayudante.")
        return helpers

    def clean_date(self):
        from datetime import date
        move_date = self.cleaned_data.get('date')
        if move_date < date.today():
            raise forms.ValidationError("La fecha de mudanza no puede ser en el pasado.")
        return move_date

    def clean_special_item(self):
        special_item = self.cleaned_data.get('special_item')
        valid_choices = [
            "grand-piano", "antique-furniture", "fine-art", "hot-tubs", "pool-tables",
            "large-appliances", "oversized-furniture", "grandfather-clocks", "vehicles",
            "chandeliers", "collectibles", "safes", "exercise-equipment", "arcade-games",
            "outdoor-furniture", "taxidermy", "musical-instruments", "above-ground-pools",
            "wine-collections", "No special items"
        ]

        if special_item not in valid_choices:
            raise forms.ValidationError("La opción seleccionada para artículos especiales no es válida.")
        
        return special_item
    
    
class ContactShortForm(forms.ModelForm):
    class Meta:
        model = ContactShort
        fields = ['name', 'email', 'date', 'message']
    