from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from apps.atletas.models import Atleta
from apps.atletas.forms import AtletaForm
from apps.jogos.models import Jogos
from apps.equipamentos.models import EncomendaItem


class AtletaListView(ListView):
    model = Atleta
    template_name = 'atletas/atletas_list.html'
    context_object_name = 'atletas'

    def get_queryset(self):
        return Atleta.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AtletaListView, self).get_context_data(**kwargs)
        context['altetas'] = Atleta.objects.all()
        context['jogos'] = Jogos.objects.all()
        return context
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['atletas/atletas_list_partial.html']
        return ['atletas/atletas_list.html']

class AtletaCreateView(CreateView):
    model = Atleta
    form_class = AtletaForm
    template_name = 'atletas/atleta_form.html'

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['atletas/atleta_form_partial.html']
        return ['atletas/atleta_form.html']

    def get_context_data(self, **kwargs):
        context = super(AtletaCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True ,'message': "Atleta criado com sucesso!"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data() 
            html_form = render_to_string('atletas/atleta_form_partial.html', {'form': form}, request=self.request)  
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm, 'message': errors}, status=400)
        return super().form_invalid(form)



class AtletaDetailView(DetailView):
    model = Atleta
    template_name = 'atletas/detail.html'
    context_object_name = 'atleta_detail'

    def get_context_data(self, **kwargs):
        context = super(AtletaDetailView, self).get_context_data(**kwargs)
        encomendas = EncomendaItem.objects.all()
        context['encomendas'] = encomendas
        return context
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['atletas/datail_partial.html']
        return ['atletas/detail.html']

   
    
    

    

class AtletaUpdateView(UpdateView):
    model = Atleta
    form_class = AtletaForm
    template_name = 'atletas/atleta_form.html'
    success_url = reverse_lazy('atletas:atletas_list')

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['atletas/atleta_form_partial.html']
        return ['atletas/atleta_form.html']

    def get_context_data(self, **kwargs):
        context = super(AtletaUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True ,'message': "Atleta editado com sucesso!"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html_form = render_to_string(self.template_name, {'form': form}, request=self.request)
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm}, status=400)
        return super().form_invalid(form)
    
    




def atletas_delete(request, pk):
    try:
        atleta = get_object_or_404(Atleta, pk=pk)
        atleta.delete()
        return JsonResponse({'success': True,'message': f"Atleta {atleta.nome} eliminado com sucesso!"})
    except:
        return JsonResponse({'success': False,'message': "Erro ao eliminar atleta!"}, status=400)
    

