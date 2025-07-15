from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from apps.atletas.models import Atleta
from apps.atletas.forms import AtletaForm
from apps.jogos.models import Jogos


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

class AtletaCreateView(CreateView):
    model = Atleta
    form_class = AtletaForm
    success_url = reverse_lazy('atletas:atletas_list')


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
    context_object_name = 'atleta_detail'

    def form_invalid(self, form):
        return super(AtletaDetailView, self).form_invalid(form)

    def form_valid(self, form):
        return super(AtletaDetailView, self).form_valid(form)

    def get_absolute_url(self):
        return reverse_lazy('atletas:atletas_list')

class AtletaUpdateView(UpdateView):
    model = Atleta
    form_class = AtletaForm
    success_url = reverse_lazy('atletas:atletas_list')


    def form_invalid(self, form):
        return super(AtletaUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        return super(AtletaUpdateView, self).form_valid(form)




def atletas_delete(request, pk):
    atleta = get_object_or_404(Atleta, pk=pk)
    atleta.delete()
    return redirect('atletas:atletas_list')

