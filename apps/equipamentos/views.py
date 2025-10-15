from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, ListView,UpdateView
from django.views.decorators.csrf import csrf_exempt
import json
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import  TA_CENTER
from apps.atletas.models import Atleta
from apps.equipamentos.models import Equipamentos, Tamanho, EncomendaItem, Encomenda, encomenda_kit
from apps.equipamentos.forms import EquipamentosForm,EncomendaItemForm , TamanhoForm, EncomendaForm


# Views and functions for Tamanho
class TamanhoCreateView(CreateView):
    model = Tamanho
    form_class = TamanhoForm
    success_url = reverse_lazy('equipamentos:encomendas_equipamentos_list')
    template_name = 'equipamentos/tamanho_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TamanhoForm()
        return context
    def form_invalid(self, form):
        return super().form_invalid(form)
    def form_valid(self, form):
        return super().form_valid(form)

class TamanhoUpdateView(CreateView):
    model = Tamanho
    form_class = TamanhoForm
    success_url = reverse_lazy('equipamentos:encomendas_equipamentos_list')
    template_name = 'equipamentos/tamanho_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TamanhoForm()
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

def tamanho_delete(request, pk):
    if request.method == 'POST':
        tamanho = Tamanho.objects.get(pk=pk)
        tamanho.delete()
    return redirect('equipamentos: equipamentos_list')

# Views and functions for  Equipamentos

class EquipamentosCreateView(CreateView):
    model = Equipamentos
    form_class = EquipamentosForm
    success_url = reverse_lazy('equipamentos:encomendas_equipamentos_list')
    template_name = 'equipamentos/equipamentos_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EquipamentosForm()
        return context

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html_form = render_to_string(self.template_name, {'form': form}, request=self.request)
            htm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htm}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({'success': True ,'mensagem': "Encomenda criada com sucesso!"})
        return super().form_valid(form)




class EquipamentosUpdateView(CreateView):
    model = Equipamentos
    form_class = EquipamentosForm
    success_url = reverse_lazy('equipamentos:encomendas_equipamentos_list')
    template_name = 'equipamentos/equipamentos_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EquipamentosForm()
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)



# Views and functions for EncomendaEquipamentos

class EncomendaEquipamentosListView(ListView):
    model = EncomendaItem
    template_name = 'equipamentos/encomenda_equipamentos_list.html'
    context_object_name = 'encomenda_equipamentos'


    def get_queryset(self):
        queryset = EncomendaItem.objects.all()
        status = self.request.GET.get('status')
        print(status)
        if status == 'todos':
            queryset = EncomendaItem.objects.all()
        elif status == 'true':
            queryset = EncomendaItem.objects.filter(entregue=True)
        elif status == 'false':
            queryset = EncomendaItem.objects.filter(entregue=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atletas'] = Atleta.objects.all()
        return context
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['equipamentos/encomenda_equipamentos_list_partial.html']
        return ['equipamentos/encomenda_equipamentos_list.html']

class EncomendaItemCreateView(CreateView):
    def get(self,request):
        form_encomenda  = EncomendaForm()
        form_item= EncomendaItemForm()
        

        template = 'equipamentos/encomenda_item_create_partial.html' if request.headers.get('HX-Request') or request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'equipamentos/encomenda_item_create.html'

        return render(request, template, {'form_encomenda': form_encomenda, 'form_item': form_item})
    
    def post(self,request):
        form_encomenda = EncomendaForm(request.POST)
        form_item = EncomendaItemForm(request.POST)
        if form_encomenda.is_valid() and form_item.is_valid():
            encomenda = form_encomenda.save()
            artigos = form_item.save(commit=False)
            equipamentos = form_item.cleaned_data['equipamento']
            if equipamentos.nome == "Kit Completo":
                print("Kit Completo")
                atleta = form_encomenda.cleaned_data['atleta']
                tamanho = form_encomenda.cleaned_data['tamanho']
                encomenda_kit(atleta,tamanho)
            else:
                artigos.encomenda = encomenda
                artigos.atleta = form_encomenda.cleaned_data['atleta']
                artigos.save()
            return JsonResponse({'success': True ,'message': "Encomenda criada com sucesso!"})
        else:
            html_form = render_to_string('equipamentos/encomenda_item_create.html', {'form_encomenda':form_encomenda,'form_item':form_item}, request=self.request)
            htlm = {'html-form': html_form}
            return JsonResponse({'success': False ,'html-form': htlm}, status=400)
        
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['equipamentos/encomenda_item_create_partial.html']
        return ['equipamentos/encomenda_item_create.html']
    

    
        
class EncomendaItemUpdateView(UpdateView):
    def get(self, request, pk):
        item = get_object_or_404(EncomendaItem, pk=pk)
        form_encomenda = EncomendaForm(instance=item.encomenda)
        form_item = EncomendaItemForm(instance=item)
        template = 'equipamentos/encomenda_item_create_partial.html' if request.headers.get('HX-Request') or request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'equipamentos/encomenda_item_create.html'

        return render(request, template, {'form_encomenda': form_encomenda, 'form_item': form_item})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aqui'] = EncomendaItemForm(instance=self.object)
        return context

    def post(self, request, pk):
        item = get_object_or_404(EncomendaItem, pk=pk)
        form_encomenda = EncomendaForm(request.POST, instance=item.encomenda)
        form_item = EncomendaItemForm(request.POST, instance=item)

        if form_encomenda.is_valid() and form_item.is_valid():
            encomenda = form_encomenda.save()
            artigos = form_item.save(commit=False)
            equipamento = form_item.cleaned_data['equipamento']

            if equipamento.nome == "Kit Completo":
                atleta = form_encomenda.cleaned_data['atleta']
                tamanho = form_encomenda.cleaned_data['tamanho']
                encomenda_kit(atleta, tamanho)
            else:
                artigos.encomenda = encomenda
                artigos.atleta = form_encomenda.cleaned_data['atleta']
                artigos.save()

            return JsonResponse({'success': True, 'message': "Encomenda editada com sucesso!"})

        else:
            html_form = render_to_string(
                'equipamentos/encomenda_item_create.html',
                {'form_encomenda': form_encomenda, 'form_item': form_item},
                request=request
            )
            return JsonResponse({'success': False, 'html_form': html_form}, status=400)

    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("ajax")
            return ['equipamentos/encomenda_item_create_partial.html']
        return ['equipamentos/encomenda_item_create.html']



def encomenda_delete(request,pk):
    try:
        encomenda = EncomendaItem.objects.get(pk=pk)
        encomenda.delete()
        return JsonResponse({'success': True,'message': f"Encomenda de  {encomenda.encomenda.atleta} eliminada com sucesso!"})
    except:
        return JsonResponse({'success': False,'message': "Erro ao eliminar encomenda!"}, status=400)
def equipamentos_delete(request, pk):
    try:
        equipamentos = Equipamentos.objects.get(pk=pk)
        equipamentos.delete()
        return JsonResponse({'success': True,'message': f"Equipamento {equipamentos.nome} eliminado com sucesso!"})
    except:
        return JsonResponse({'success': False,'message': "Erro ao eliminar equipamento!"}, status=400)

def encomendas_por_atleta(request, pk,status):
    
    
    if (pk == 'todos' or pk == 'todosAtletas') and status == 'todos':
        print("todos")
        encomendas = EncomendaItem.objects.all()
    elif (pk == 'todos' or pk == 'todosAtletas') and status !='todos':
        print("todos mas entregue ou nao entregue")
        status_bool = True if status == 'entregue' else False
        encomendas = EncomendaItem.objects.filter(entregue=status_bool)
    elif pk != 'todos' and status == 'todos':
        print("um atleta todas as encomendas")
        encomendas = EncomendaItem.objects.filter(encomenda__atleta__id=pk)
    else:
        print("um atleta entregue ou nao entregue")
        status_bool = True if status == 'entregue' else False
        print(status_bool)
        encomendas = EncomendaItem.objects.filter(encomenda__atleta__id=pk, entregue=status_bool)
    
    resultados = [
        {
            'id' : encomenda.id,
            'atleta': encomenda.encomenda.atleta.nome,
            'equipamento': encomenda.equipamento.nome,
            'tamanho': encomenda.encomenda.tamanho.tamanho,
            'data_pedido': encomenda.encomenda.data_pedido,
            'entregue': encomenda.entregue,
            'edit_icon': static('images/edit_img.svg'),
            'delete_icon': static('images/delete_img.svg'),
 
        } for encomenda in encomendas
    ]
    return JsonResponse({'resultados': resultados})

def alterar_estado_encomenda(request, pk):
    encomenda = EncomendaItem.objects.get(pk=pk)
    encomenda.entregue = not encomenda.entregue
    encomenda.save()
    return JsonResponse({'success': True,'message': f"Encomenda entregue com sucesso!"})

@csrf_exempt
def gerar_pdf_encomendas(request):
    print(request.method)
    if request.method == 'POST':
        try:
            encomendas_json = request.POST.get("encomendas", "[]")
            lista_ids = json.loads(encomendas_json)
            print(lista_ids)

            encomendas = EncomendaItem.objects.filter(id__in=lista_ids)
            return gerar_pdf_encomendas_atleta("Encomendas Sub-6/7", encomendas)

        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': "Erro ao gerar PDF!"}, status=400)

    return JsonResponse({"success": False, "message": "Método não permitido"}, status=405)


def gerar_pdf_encomendas_atleta(titulo, contexto):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    titulo_style = ParagraphStyle(
        'titulo',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor("#183153"),
        spaceAfter=40,
        alignment=TA_CENTER

    )

    elements.append(Paragraph(titulo, titulo_style))

    data = [["Atleta", "Equipamento", "Tamanho", "Data Pedido"]]  
    for encomenda in contexto:
        data.append([
            str(encomenda.encomenda.atleta),
            str(encomenda.equipamento),
            str(encomenda.encomenda.tamanho),
            encomenda.encomenda.data_pedido.strftime("%d/%m/%Y"),
        ])

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

# Linhas alternadas
    for i, row in enumerate(data[1:], start=1):
        bg_color = colors.HexColor("#F4F6F8") if i % 2 == 1 else colors.white
        style.add('BACKGROUND', (0, i), (-1, i), bg_color)

    table.setStyle(style)
    

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="encomendas.pdf")