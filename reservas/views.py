from django.shortcuts import render


def reservas(request):
    return render(request, 'reservas.html', {'page': 'reservas'})
