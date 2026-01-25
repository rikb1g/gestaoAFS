import json
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.template.loader import render_to_string
from apps.jogos.models import Jogos, Equipas, EstatisticaJogo, HistoricoSubstituição
from apps.jogos.forms import JogosForm, EquipasForm
from apps.atletas.models import Atleta


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
        self.object = form.save()
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
            return JsonResponse({'success': True, 'message': "Jogo criado com sucesso!"})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()
            html_form = render_to_string('jogos/jogos_form_partial.html', {'form': form}, request=self.request)
            htm = {'html-form': html_form}
            return JsonResponse({'success': False, 'html-form': htm, 'message': errors}, status=400)
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
            return JsonResponse({'success': False, 'html-form': htm}, status=400)
        return super().form_invalid(form)


def jogosDelete(request, pk):
    try:
        Jogos.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True, 'message': "Jogo eliminado com sucesso!"})
    except:
        return JsonResponse({'success': False, 'message': "Erro ao eliminar jogo!"}, status=400)


class EquipaCreateView(CreateView):
    model = Equipas
    template_name = 'jogos/equipa_form.html'
    form_class = EquipasForm

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': "Equipa criada com sucesso!"})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()
            html_form = render_to_string('jogos/equipa_form_partial.html', {'form': form}, request=self.request)
            htm = {'html-form': html_form}
            return JsonResponse({'success': False, 'html-form': htm, 'message': errors}, status=400)
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
        self.object = form.save()
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
            return JsonResponse({'success': True, 'message': "Equipa criada com sucesso!"})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get_json_data()
            html_form = render_to_string('jogos/equipa_form_partial.html', {'form': form}, request=self.request)
            htm = {'html-form': html_form}
            return JsonResponse({'success': False, 'html-form': htm, 'message': errors}, status=400)
        return super().form_invalid(form)

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['jogos/equipa_form_partial.html']
        return ['jogos/equipa_form.html']


def equipaDelete(request, pk):
    try:
        Equipas.objects.filter(pk=pk).delete()
        return JsonResponse({'success': True, 'message': "Equipa eliminada com sucesso!"})
    except:
        return JsonResponse({'success': False, 'message': "Erro ao eliminar equipa!"}, status=400)


def estatistica_jogo(request, pk):
    jogo = Jogos.objects.get(pk=pk)
    estatisticas = EstatisticaJogo.objects.filter(jogo=jogo).order_by('-em_campo')

    if jogo.visitado.nome.startswith("AVS"):
        equipa = jogo.visitado.nome
    elif jogo.visitante.nome.startswith("AVS"):
        equipa = jogo.visitante.nome
    else:
        equipa = None

    data = {
        'jogo': {
            'id': jogo.id,
            'visitado': jogo.visitado,
            'visitante': jogo.visitante,
            'golos_visitado': jogo.golos_visitado,
            'golos_visitante': jogo.golos_visitante,
            'jornada': jogo.jornada,
            'equipa': equipa,
            'inicio': jogo.inicio_jogo.isoformat() if jogo.inicio_jogo else None,
        },
        'estatisticas': estatisticas,
        'jogo_id': jogo.id,
    }
    print(data)

    template = 'jogos/estatisticas_partial.html' if request.headers.get(
        'x-requested-with') == 'XMLHttpRequest' else 'jogos/estatisticas.html'
    return render(request, template_name=template, context=data)


def iniciar_jogo(request, id_jogo):
    data = json.loads(request.body)
    atletas_ids = data.get('atletas', [])
    print(atletas_ids)

    jogo = Jogos.objects.get(pk=id_jogo)
    jogo.inicio_jogo = timezone.now()
    jogo.pausa = False
    jogo.save()
    print("primeira parte")

    for atleta_id in atletas_ids:
        atleta = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
        atleta.inicio = timezone.now()
        atleta.em_campo = True
        atleta.save()

    return JsonResponse({'success': True, 'message': "Jogo iniciado com sucesso!"})


def substituicao_jogo(request):
    data = json.loads(request.body)
    atleta_id = data.get('atleta')
    jogo_id = data.get('jogo')

    try:
        jogo = Jogos.objects.get(pk=jogo_id)
        estatistica = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
    except (Jogos.DoesNotExist, EstatisticaJogo.DoesNotExist):
        return JsonResponse({'error': 'Jogo ou atleta não encontrado'}, status=404)

    if estatistica.em_campo:
        if not jogo.pausa:
            estatistica.fim = timezone.now()
            estatistica.em_campo = False

            if estatistica.inicio:
                total_minutos = (estatistica.fim - estatistica.inicio).total_seconds() / 60
                estatistica.total_minutos += total_minutos

            HistoricoSubstituição.objects.create(jogo=jogo, atleta=estatistica.atleta, entrou=estatistica.inicio,
                                                 saiu=estatistica.fim, total_minutos=estatistica.total_minutos)
            estatistica.inicio = None
            estatistica.fim = None
            estatistica.save()
            return JsonResponse({'success': True, 'status': 'saiu', 'total_minutos': estatistica.total_minutos})
        else:
            estatistica.em_campo = False
            estatistica.save()
            return JsonResponse({'success': True, 'status': 'entrou'})
    else:
        if not jogo.pausa:
            estatistica.inicio = timezone.now()
            estatistica.em_campo = True
            estatistica.save()
            return JsonResponse({'success': True, 'status': 'entrou'})
        else:
            estatistica.em_campo = True
            estatistica.save()
            return JsonResponse({'success': True, 'status': 'Jogo em intervalo'})


def intervalo_jogo(request, id_jogo):
    data = json.loads(request.body)
    atletas_ids = data.get('atletas', [])
    try:
        jogo = Jogos.objects.get(pk=id_jogo)

        jogo.inicio_jogo = None
        jogo.pausa = True
        jogo.save()
        for atleta_id in atletas_ids:
            atleta_estatistica = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
            atleta_estatistica.fim = timezone.now()
            atleta_estatistica.em_campo = False
            atleta_estatistica.save()
            if atleta_estatistica.inicio:
                total_minutos = (atleta_estatistica.fim - atleta_estatistica.inicio).total_seconds() / 60
                atleta_estatistica.total_minutos += total_minutos

            HistoricoSubstituição.objects.create(jogo=jogo, atleta=atleta_estatistica.atleta,
                                                 entrou=atleta_estatistica.inicio, saiu=atleta_estatistica.fim,
                                                 total_minutos=atleta_estatistica.total_minutos)
            atleta_estatistica.inicio = None
            atleta_estatistica.fim = None
            atleta_estatistica.save()
        return JsonResponse({'success': True, 'message': "Intervalo iniciado com sucesso!"})
    except:
        return JsonResponse({'success': False, 'message': "Erro ao iniciar intervalo!"}, status=400)


def finalizar_jogo(request, id_jogo):
    data = json.loads(request.body)
    atletas_ids = data.get('atletas', [])
    try:
        jogo = Jogos.objects.get(pk=id_jogo)
        jogo.pausa = True
        jogo.inicio_jogo = None
        jogo.fim_jogo = timezone.now()
        jogo.save()
        for atleta_id in atletas_ids:
            atleta_estatistica = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
            atleta_estatistica.fim = timezone.now()
            atleta_estatistica.em_campo = False
            atleta_estatistica.save()
            if atleta_estatistica.inicio:
                total_minutos = (atleta_estatistica.fim - atleta_estatistica.inicio).total_seconds() / 60
                atleta_estatistica.total_minutos += total_minutos

            HistoricoSubstituição.objects.create(jogo=jogo, atleta=atleta_estatistica.atleta,
                                                 entrou=atleta_estatistica.inicio, saiu=atleta_estatistica.fim,
                                                 total_minutos=atleta_estatistica.total_minutos)
            atleta_estatistica.inicio = None
            atleta_estatistica.fim = None
            atleta_estatistica.save()
        return JsonResponse({'success': True, 'message': "Jogo finalizado com sucesso!"})
    except:
        return JsonResponse({'success': False, 'message': "Erro ao finalizar jogo!"}, status=400)


def golo(request, atleta_id, jogo_id):
    try:
        jogo = Jogos.objects.get(pk=jogo_id)
        atleta = Atleta.objects.get(pk=atleta_id)
        estatistica = EstatisticaJogo.objects.get(atleta__id=atleta_id, jogo=jogo)
        estatistica.golos += 1
        estatistica.save()
        if atleta.equipa == jogo.visitado:
            jogo.golos_visitado += 1
            jogo.save()

        else:
            jogo.golos_visitante += 1
            jogo.save()
        return JsonResponse({'success': True, 'message': "Golo marcado com sucesso!"})
    except Exception as e:
        print("ERRO:", e)
        return JsonResponse({'success': False, 'message': "Erro ao marcar golo!"}, status=400)


def golo_equipa(request, id_jogo, id_equipa):
    try:
        jogo = Jogos.objects.get(pk=id_jogo)

        if id_equipa == jogo.visitado.id:
            jogo.golos_visitado += 1
        elif id_equipa == jogo.visitante.id:
            jogo.golos_visitante += 1
        else:
            return JsonResponse({'success': False, 'message': 'Equipa inválida'}, status=400)

        jogo.save()

        return JsonResponse({'success': True, 'message': 'Golo marcado com sucesso!'})

    except Exception as e:
        print("ERRO:", e)
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def atletas_por_equipa(request, equipa_id):
    equipa_ = Equipas.objects.get(pk=equipa_id)
    if equipa_.nome == "AVS sub-7":
        print("AVS sub-7")
        equipas = Atleta.objects.filter(equipa__nome__icontains="AVS sub-7").values('id', 'nome')
        print("equipas")
        print(equipas)
        return JsonResponse(list(equipas), safe=False)
    else:
        equipas = Equipas.objects.filter(nome__icontains="AVS sub-7")
        print(equipas)


    atletas = Atleta.objects.filter(equipa_id=equipa_id).values('id', 'nome')
    return JsonResponse(list(atletas), safe=False)
