import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chale.settings')
django.setup()

from propriedades.models import Propriedade

# Criar Propriedades genéricas
Propriedade.objects.create(nome='Propriedade Genérica 1', tipo='propriedade')

# Criar 3 Chales Comuns
Propriedade.objects.create(nome='Chale Comum Praia', tipo='chale_comum')
Propriedade.objects.create(nome='Chale Comum Serra', tipo='chale_comum')
Propriedade.objects.create(nome='Chale Comum Lago', tipo='chale_comum')

# Criar 2 Chales Exclusivos
Propriedade.objects.create(nome='Chale Exclusivo Penthouse', tipo='chale_exclusivo')
Propriedade.objects.create(nome='Chale Exclusivo VIP', tipo='chale_exclusivo')

print('Dados criados com sucesso!')
print(f'Total Propriedades: {Propriedade.objects.count()}')
print(f'Genéricas: {Propriedade.objects.filter(tipo="propriedade").count()}')
print(f'Chales Comuns: {Propriedade.objects.filter(tipo="chale_comum").count()}')
print(f'Chales Exclusivos: {Propriedade.objects.filter(tipo="chale_exclusivo").count()}')
