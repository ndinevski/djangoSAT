from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from . import serializers
from . import forms
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.core.mail import send_mail

# Create your views here.
@api_view(['GET'])
def getHome(request):
    return render(request, 'home.html')

@api_view(['GET'])
def getCompanies(request):
    companies = models.Company.objects.filter(owner=request.user)

    form = forms.CompanyOrderingForm(request.GET)

    if form.is_valid():
        order_by = form.cleaned_data['order_by']
        if order_by == 'alphabetical':
            companies = companies.order_by('company_name')
        elif order_by == 'reverse_alphabetical':
            companies = companies.order_by('-company_name')
        else:
            companies = companies.order_by('id')

    serializer = serializers.CompanySerializer(companies, many=True)

    return render(request, 'allcompanies.html', {'companies': companies, 'form': form})
    # return Response(serializer.data)

@api_view(['GET'])
def getCompany(request, pk):
    company = models.Company.objects.filter(owner=request.user).get(id=pk)
    serializer = serializers.CompanySerializer(company, many=False)
    return render(request, 'company.html', {'company': company})
    # return Response(serializer.data)
    
def createCompany(request):
    if request.method == 'POST':
        form = forms.CompanyForm(request.POST)
        if form.is_valid() and models.Company.objects.filter(owner=request.user).count()<5:
            form.instance.owner = request.user
            form.save()
            # send_mail(
            #     "Created new Company",
            #     "You have created a new Company " + " " + form.cleaned_data['company_name'] + " " + "with" + " " + str(form.cleaned_data['number_of_employees']) + " " + "employees",
            #     "ndinevski@djangostacompany.com",
            #     [str(request.user.email)],
            #     fail_silently=False,
            # )
            return redirect('/companies/')
        elif models.Company.objects.filter(owner=request.user).count()>=5:
            return HttpResponse('<p>You cannot create more than 5 Companies.</p>')
        else:
            return HttpResponse('<p>Info is not Valid</p>')

    else:
        form = forms.CompanyForm
        context = {
                'form': form,
        }

        return render(request, 'create_company.html', context)

def updateCompanyEmployees(request, pk):
    company = models.Company.objects.filter(owner=request.user).get(id=pk)

    if request.method == "POST": 
        PartialCompanyForm = modelform_factory(
            models.Company, form=forms.EditCompanyForm, fields=('number_of_employees',)
        )
        form = PartialCompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save()
            return redirect('/companies/')
    else:
        form = forms.EditCompanyForm(instance=company)
        context = {
                'form': form,
                'company': company,
        }

        return render(request, 'edit_company.html', context)