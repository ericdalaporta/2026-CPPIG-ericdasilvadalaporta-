from django.shortcuts import render


def registros(request):
    return render(request, 'registros/registros.html', {'page': 'registros'})
