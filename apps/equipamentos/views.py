from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from apps.equipamentos.models import Equipamentos, Tamanho, EncomendaEquipamentos
from apps.equipamentos.forms import EquipamentosForm, EncomendaEquipamentosForm, TamanhoForm


# Views and functions for Tamanho
class TamanhoCreateView(CreateView):
    model = Tamanho
    model_form = TamanhoForm
    success_url = '/equipamentos/'
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
    model_form = TamanhoForm
    success_url = '/equipamentos/'
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
    model_form = EquipamentosForm
    success_url = '/equipamentos/'
    template_name = 'equipamentos/equipamentos_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EquipamentosForm()
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

class EquipamentosUpdateView(CreateView):
    model = Equipamentos
    model_form = EquipamentosForm
    success_url = '/equipamentos/'
    template_name = 'equipamentos/equipamentos_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EquipamentosForm()
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

def equipamentos_delete(request, pk):
    if request.method == 'POST':
        equipamentos = Equipamentos.objects.get(pk=pk)
        equipamentos.delete()
    return redirect('equipamentos: equipamentos_list')

# Views and functions for EncomendaEquipamentos

class EncomendaEquipamentosListView(ListView):
    model = EncomendaEquipamentos
    template_name = 'equipamentos/encomenda_equipamentos_list.html'
    context_object_name = 'encomenda_equipamentos'

    def get_queryset(self):
        return EncomendaEquipamentos.objects.all()


class EncomendaEquipamentosCreateView(CreateView):
    model = EncomendaEquipamentos
    model_form = EncomendaEquipamentosForm
    success_url = '/equipamentos/'
    template_name = 'equipamentos/encomenda_equipamentos_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EncomendaEquipamentosForm()
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

class EncomendaEquipamentosUpdateView(CreateView):
    model = EncomendaEquipamentos
    model_form = EncomendaEquipamentosForm
    success_url = '/equipamentos/'
    template_name = 'equipamentos/encomenda_equipamentos_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EncomendaEquipamentosForm()
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class EncomendaEquipamentosDetailView(DetailView):
    model = EncomendaEquipamentos
    template_name = 'equipamentos/encomenda_equipamentos_detail.html'
    context_object_name = 'encomenda_equipamentos'

def encomenda_equipamentos_delete(request, pk):
    if request.method == 'POST':
        encomenda_equipamentos = EncomendaEquipamentos.objects.get(pk=pk)
        encomenda_equipamentos.delete()
    return redirect('equipamentos: equipamentos_list')



