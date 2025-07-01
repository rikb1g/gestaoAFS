from django.shortcuts import  redirect
from django.views.generic import CreateView, DetailView
from apps.atletas.models import Atleta
from apps.atletas.forms import AtletaForm


class AtletaListView(CreateView):
    model = Atleta
    template_name = 'atletas/atletas_list.html'
    context_object_name = 'atletas'

class AtletaCreateView(CreateView):
    model = Atleta
    model_form_class = AtletaForm
    success_url = '/atletas/'


    def get_context_data(self, **kwargs):
        context = super(AtletaCreateView, self).get_context_data(**kwargs)
        context['form'] = AtletaForm()
        return context

    def form_invalid(self, form):
        return super(AtletaCreateView, self).form_invalid(form)

    def form_valid(self, form):
        return super(AtletaCreateView, self).form_valid(form)

class AtletaDetailView(DetailView):
    model = Atleta
    template_name = 'atletas/detail.html'
    context_object_name = 'atleta'

class AtletaUpdateView(CreateView):
    model = Atleta
    form_class = AtletaForm
    success_url = '/atletas/'

    def get_context_data(self, **kwargs):
        context = super(AtletaUpdateView, self).get_context_data(**kwargs)
        context['form'] = AtletaForm(instance=self.object)
        return context

    def form_invalid(self, form):
        return super(AtletaUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        return super(AtletaUpdateView, self).form_valid(form)


def atletas_delete(request, pk):
    if request.method == 'POST':
        atleta = Atleta.objects.get(pk=pk)
        atleta.delete()
    return redirect('atletas:atletas_list')

