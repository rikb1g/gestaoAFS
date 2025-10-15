
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.core import serializers
from django.utils.timezone import datetime
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from apps.atletas.models import Atleta
from apps.atletas.forms import AtletaForm
from apps.jogos.models import Jogos, Equipas
from apps.equipamentos.models import EncomendaItem

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import  TA_CENTER


class AtletaListView(ListView):
    model = Atleta
    template_name = 'atletas/atletas_list.html'
    context_object_name = 'atletas'

    def get_queryset(self):
        return Atleta.objects.all().order_by('data_nascimento')

    def get_context_data(self, **kwargs):
        context = super(AtletaListView, self).get_context_data(**kwargs)
        context['altetas'] = Atleta.objects.all()
        context['jogos'] = Jogos.objects.all()
        context['equipas'] = Equipas.objects.filter(nome__contains='AVS').order_by('nome')
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
    

def gerar_pdf_lista_atletas(request):
    escalao = request.GET.get('escalao')
    response = HttpResponse(content_type= 'aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    titulo_style = ParagraphStyle(
        'titulo',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor("#183153"),
        spaceAfter=40,
        alignment=TA_CENTER

    )
    elements.append(Paragraph(f"Lista de Atletas - Escalação Sub-{str(escalao).upper() if escalao != 'todos' else escalao}", titulo_style))
    data = [["Nome", "Data de Nascimento", "Número Camisola"]]
    if escalao == 'todos':
        atletas = Atleta.objects.all().order_by('data_nascimento')
    elif escalao == '6':
        atletas = Atleta.objects.filter(data_nascimento__year__gt=(2019)).order_by('data_nascimento')
    elif escalao == '7':
        atletas = Atleta.objects.filter(data_nascimento__year=(2019)).order_by('data_nascimento')
    for atleta in atletas:
        data.append([atleta.nome,atleta.data_nascimento, atleta.numero])
    table = Table(data)
    table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(table)
    doc.build(elements)
    return response

def gerar_pdf_camisolas_atletas(request):
    escalao = request.GET.get('escalao')
    print(escalao)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    titulo_style = ParagraphStyle(
        'titulo',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor("#183153"),
        spaceAfter=40,
        alignment=TA_CENTER

    )
    elements.append(Paragraph("Relatório de Camisolas", titulo_style))
    data = [["Nome", "Número", 'Tipo', "Tamanho"]]
    if escalao == 'todos':
        atletas = Atleta.objects.all().order_by('data_nascimento')
    elif escalao == '6':
        atletas = Atleta.objects.filter(data_nascimento__year__gt=(2019)).order_by('data_nascimento')
    elif escalao == '7':
        atletas = Atleta.objects.filter(data_nascimento__year=(2020)).order_by('data_nascimento')
    else:
        atletas = Atleta.objects.all().order_by('data_nascimento')
    encomendas_equipamento_jogo = EncomendaItem.objects.filter(encomenda__atleta__in=atletas,equipamento__nome__in=["jogo principal", "guarda-redes azul"]).order_by('encomenda__atleta__data_nascimento')
    for equipamento in encomendas_equipamento_jogo:
        data.append([str(equipamento.encomenda.atleta.nome_camisola).title(), str(equipamento.encomenda.atleta.numero), str(equipamento.equipamento).capitalize(), str(equipamento.encomenda.tamanho)])

    table = Table(data)

    style = TableStyle([
    # Cabeçalho
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B7BEC")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

    # Bordas
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CED4DA")),
    ])
    for i, row in enumerate(data[1:], start=1):
        bg_color = colors.HexColor("#F4F6F8") if i % 2 == 1 else colors.white
        style.add('BACKGROUND', (0, i), (-1, i), bg_color)

    table.setStyle(style)
    

    elements.append(table)
    doc.build(elements)
    return response



def atletas_escalao_json(request):
    escalao_filter = request.GET.get('escalao')
    print(escalao_filter)

    if escalao_filter == 'todos':
        print("todos")
        qs = Atleta.objects.all()

    else: 
        qs = Atleta.objects.filter(equipa__id=escalao_filter)
        print(qs)

    
    atletas_list = [
        {
            "id": atleta.id,
            "nome": atleta.nome,
            "numero": atleta.numero,
            "nome_camisola": atleta.nome_camisola,
            'data_nascimento': atleta.data_nascimento,
            "guarda_redes": atleta.guarda_redes,
            "equipa": atleta.equipa.nome if atleta.equipa else "",
        }
        for atleta in qs
    ]
    return JsonResponse({'resultados': atletas_list})
