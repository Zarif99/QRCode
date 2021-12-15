from django.shortcuts import render
from .models import Customer


def index(request):
    customers = Customer.objects.all()
    return render(request, 'index.html', {'customers': customers})


def invoice(request, slug):
    customer = Customer.objects.get(slug__iexact=slug)
    return render(request, 'qrcode/invoice.html', {'post': customer})
