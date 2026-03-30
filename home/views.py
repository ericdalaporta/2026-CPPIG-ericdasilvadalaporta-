from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'page': 'index'})


def reservas(request):
    return render(request, 'reservas.html', {'page': 'reservas'})


def emprestimos(request):
    return render(request, 'emprestimos.html', {'page': 'emprestimos'})


def registros(request):
    return render(request, 'registros.html', {'page': 'registros'})


def propriedades(request):
    return render(request, 'propriedades.html', {'page': 'propriedades'})


def chaves(request):
    return render(request, 'chaves.html', {'page': 'chaves'})


def notificacoes(request):
    return render(request, 'notificacoes.html', {'page': 'notificacoes'})


def usuarios(request):
    return render(request, 'usuarios.html', {'page': 'usuarios'})


def acessos(request):
    return render(request, 'acessos.html', {'page': 'acessos'})
