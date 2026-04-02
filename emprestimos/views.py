from django.shortcuts import render


def emprestimos(request):
    return render(request, 'emprestimos.html', {'page': 'emprestimos'})
