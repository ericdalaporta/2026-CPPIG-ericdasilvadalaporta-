from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina'] = 'index'
        return contexto
