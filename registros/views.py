from django.shortcuts import render


def registros(request):
    return render(request, 'registros.html', {'page': 'registros'})
