from django.forms import ModelForm, Form, ChoiceField
from .models import Company

class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ['company_name','description','number_of_employees']

class EditCompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ['number_of_employees']

class CompanyOrderingForm(Form):
    ORDER_CHOICES = [
        ('alphabetical', 'A-Z'),
        ('reverse_alphabetical', 'Z-A'),
        ('id', 'By ID'),
    ]

    order_by = ChoiceField(required=False, choices=ORDER_CHOICES)