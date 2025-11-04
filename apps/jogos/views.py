import json
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.template.loader import render_to_string
from apps.jogos.models import Jogos, Equipas, EstatisticaJogo
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
    get_absolute_url = 'jogos_list'
    

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/jogos_form_partial.html']
        return ['jogos/jogos_form.html']
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        self.object=  form.save()
        visitado = self.object.visitado
        visitante = self.object.visitante
        jogo = self.object

        if visitado.nome.startswith('AVS'):
            for atleta in list(jogo.titulares.all()) + list(jogo.suplentes.all()):
                if not EstatisticaJogo.objects.filter(jogo=jogo, atleta=atleta).exists():
                    titular = True if atleta in list(jogo.titulares.all()) else False
                    EstatisticaJogo.objects.create(
                        jogo=jogo,
                        atleta=atleta,
                        golos=0,
                        assistencias=0,
                        total_minutos=0,
                        em_campo=titular
                    )
        elif visitante.nome.startswith('AVS'):
            for atleta in list(jogo.titulares.all()) + list(jogo.suplentes.all()):
                if not EstatisticaJogo.objects.filter(jogo=jogo, atleta=atleta).exists():
                    titular = True if atleta in list(jogo.titulares.all()) else False
                    EstatisticaJogo.objects.create(
                        jogo=jogo,
                        atleta=atleta,
                        golos=0,
                        assistencias=0,
                        total_minutos=0,
                        em_campo=titular
                    )
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
    get_absolute_url = 'jogos_list'
    
    

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/jogos_form_partial.html']
        return ['jogos/jogos_form.html']
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        self.object = form.save()
        visitado = self.object.visitado
        visitante = self.object.visitante
        jogo = self.object  


        if visitado.nome.startswith('AVS'):
            titulares = jogo.titulares.all()
            for atleta in list(jogo.titulares.all()) + list(jogo.suplentes.all()):
                if not EstatisticaJogo.objects.filter(jogo=jogo, atleta=atleta).exists():
                    titular = True if atleta in list(jogo.titulares.all()) else False
                    EstatisticaJogo.objects.create(
                        jogo=jogo,
                        atleta=atleta,
                        golos=0,
                        assistencias=0,
                        total_minutos=0,
                        em_campo=titular,
                    )
        elif visitante.nome.startswith('AVS'):
            for atleta in list(jogo.titulares.all()) + list(jogo.suplentes.all()):
                if not EstatisticaJogo.objects.filter(jogo=jogo, atleta=atleta).exists():
                    titular = True if atleta in list(jogo.titulares.all()) else False
                    EstatisticaJogo.objects.create(
                        jogo=jogo,
                        atleta=atleta,
                        golos=0,
                        assistencias=0,
                        total_minutos=0,
                        em_campo=titular,
                    )

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': "Jogo editado com sucesso!"})
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
        if self.object.visitado.startwith('AVS'):
            for atleta in self.object.visitado.atletas.all():
                EstatisticaJogo.objects.create(
                    jogo=self.object,
                    atleta=atleta,
                    golos=0,
                    assistencias=0,
                    total_minutos=0
                )
        elif self.object.visitante.startwith('AVS'):
            for atleta in self.object.visitante.atletas.all():
                EstatisticaJogo.objects.create(
                    jogo=self.object,
                    atleta=atleta,
                    golos=0,
                    assistencias=0,
                    total_minutos=0
                )
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
    


def estatistica_jogo(request, pk):
    jogo = Jogos.objects.get(pk=pk)
    estatisticas = EstatisticaJogo.objects.filter(jogo=jogo)
    data = {}

    if jogo.visitado.nome.startswith("AVS"):
        data['jogo'] = {
        'jornada': jogo.jornada,
        'equipa': jogo.visitado,
        'inicio': jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None,
        
    }   
        print(jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None)
    elif jogo.visitante.nome.startswith("AVS"):
        data['jogo'] = {
        'jornada': jogo.jornada,
        'equipa': jogo.visitante.nome,
        'inicio': jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None,
    }
        print(jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None)
    else:
        data['jogo'] = None  

    print(data['jogo'])

    data['estatisticas'] = []
    for estatistica in estatisticas:
        data['estatisticas'].append({
            'id_atleta': estatistica.atleta.id,
            'jogo': estatistica.jogo,
            'jogo_id': estatistica.jogo.id,
            'atleta': estatistica.atleta.nome,
            'golos': estatistica.golos,
            'inicio': estatistica.inicio,
            'assistencias': estatistica.assistencias,
            'total_minutos': estatistica.total_minutos,
            'em_campo': estatistica.em_campo
        })
    data['estatisticas'] = sorted(
    data['estatisticas'],
    key=lambda x: x['em_campo'],
    reverse=True
    )
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, template_name='jogos/estatisticas_partial.html',context=data)

    return render(request, template_name='jogos/estatisticas.html',context=data)




def iniciar_jogo(request,id_jogo):
    data = json.loads(request.body)
    atletas_ids = data.get('atletas', [])

    
    jogo = Jogos.objects.get(pk=id_jogo)
    jogo.inicio_jogo = timezone.now()
    jogo.save()
    print("iniciou jogo com sucesso")
    for atleta_id in atletas_ids:
            atleta = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
            print(atleta)
            atleta.inicio = timezone.now()
            atleta.em_campo = True
            atleta.save()
    
    return JsonResponse({'success': True ,'message': "Jogo iniciado com sucesso!"})