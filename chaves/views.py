from django.shortcuts import render


def chaves(request):
    return render(request, 'chaves/chaves.html', {'page': 'chaves'})
