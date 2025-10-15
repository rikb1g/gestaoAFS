from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.template.loader import render_to_string
from apps.jogos.models import Jogos, Equipas
from apps.jogos.forms import JogosForm, EquipasForm


class JogosListView(ListView):
    model = Jogos
    template_name = 'jogos/jogos_list.html'
    context_object_name = 'jogos'

    def get_queryset(self):
        return super().get_queryset().order_by('data')
    
    def get_context_data(self, **kwargs):
        context = super(JogosListView, self).get_context_data(**kwargs)
        context['jogos'] = Jogos.objects.all()
        return context
    

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/jogos_list_partial.html']
        return ['jogos/jogos_list.html']
    

class JogosCreateView(CreateView):
    model = Jogos
    template_name = 'jogos/jogos_form.html'
    form_class = JogosForm
    

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/jogos_form_partial.html']
        return ['jogos/jogos_form.html']
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        self.object=  form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True ,'message': "Jogo criado com sucesso!"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data() 
            html_form = render_to_string('jogos/jogos_form_partial.html', {'form': form}, request=self.request)  
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm, 'message': errors}, status=400)
        return super().form_invalid(form)


class JogosUpdateView(UpdateView):
    model = Jogos
    template_name = 'jogos/jogos_form.html'
    form_class = JogosForm

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/jogos_form_partial.html']
        return ['jogos/jogos_form.html']
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True ,'message': "Jogo editado com sucesso!"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html_form = render_to_string('jogos/jogos_form_partial.html', {'form': form}, request=self.request)
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm}, status=400)
        return super().form_invalid(form)
    

def jogosDelete(request, pk):
    try:
        Jogos.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True ,'message': "Jogo eliminado com sucesso!"})
    except:
        return JsonResponse({'success': False,'message': "Erro ao eliminar jogo!"}, status=400)
    


class EquipaCreateView(CreateView):
    model =Equipas
    template_name = 'jogos/equipa_form.html'
    form_class = EquipasForm

    def form_valid(self, form):
        self.object=  form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True ,'message': "Equipa criada com sucesso!"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data() 
            html_form = render_to_string('jogos/equipa_form_partial.html', {'form': form}, request=self.request)  
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm, 'message': errors}, status=400)
        return super().form_invalid(form)
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/equipa_form_partial.html']
        return ['jogos/equipa_form.html']


class EquipaUpdateView(UpdateView):
    model = Equipas
    template_name = 'jogos/equipa_form.html'
    form_class = EquipasForm
    def form_valid(self, form):
        self.object=  form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True ,'message': "Equipa criada com sucesso!"})
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data() 
            html_form = render_to_string('jogos/equipa_form_partial.html', {'form': form}, request=self.request)  
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm, 'message': errors}, status=400)
        return super().form_invalid(form)
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/equipa_form_partial.html']
        return ['jogos/equipa_form.html']

def equipaDelete(request, pk):
    try:
        Equipas.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True ,'message': "Equipa eliminada com sucesso!"})
    except:
        return JsonResponse({'success': False,'message': "Erro ao eliminar equipa!"}, status=400)