from django.shortcuts import render


def propriedades(request):
    return render(request, 'propriedades.html', {'page': 'propriedades'})
