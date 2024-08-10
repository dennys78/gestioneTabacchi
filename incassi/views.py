from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView, UpdateView)
from django.db.models import Sum


from .forms import (
    IncassoForm, DettagliFormSet, ImageFormSet
)
from .models import (
    Image,
    Dettagli,
    Incasso
)


class IncassoInline():
    form_class = IncassoForm
    model = Incasso
    template_name = "incassi/incasso_aggiorna_crea.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('incassi:list_incassi')


    def formset_dettagli_valid(self, formset):
        dettagli = formset.save(commit=False)  
        for obj in formset.deleted_objects:
            obj.delete() 
        for dettaglio in dettagli:
            dettaglio.incasso = self.object
            dettaglio.save() #In questo punto salviamo i dati finali ed usciamo dalla maschera di inserimento 


    def formset_images_valid(self, formset):
        images = formset.save(commit=False)  
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.product = self.object
            image.save()
                


class IncassoCreate(IncassoInline, CreateView): 

    def get_context_data(self, **kwargs):
        ctx = super(IncassoCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'dettagli': DettagliFormSet(prefix='dettagli'),
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'dettagli': DettagliFormSet(self.request.POST or None, self.request.FILES or None, prefix='dettagli'),
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class IncassoUpdate(IncassoInline, UpdateView):
    
    def get_context_data(self, **kwargs):
        ctx = super(IncassoUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'dettagli': DettagliFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='dettagli'),
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }
    

def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('incassi:update_Incasso', pk=image.incasso.id)
 
    image.delete()
    messages.success(request, 'Image deleted successfully')
    return redirect('incassi:update_incasso', pk=image.incasso.id)


def delete_dettaglio(request, pk):
    try:
        dettagli = Dettagli.objects.get(id=pk)
    except Dettagli.DoesNotExist:
        messages.success(request, 'Object Does not exit')
        return redirect('incassi:update_incasso', pk=dettagli.incasso.id)

    dettagli.delete()
    messages.success(request,'Variant deleted successfully')
    return redirect('incassi:update_incasso', pk=dettagli.incasso.id)


def delete_incasso(request, pk):
    try:
        incasso = Incasso.objects.get(id=pk)
    except Incasso.DoesNotExist:
        messages.success(request, 'Incasso non trovato')
        return redirect('incassi:list_incassi')  # Reindirizzamento alla vista elenco

    incasso.delete()
    messages.success(request, 'Incasso eliminato')
    return redirect('incassi:list_incassi')  # Reindirizzamento alla vista elenco dopo l'eliminazione


class IncassoList(ListView):
    model = Incasso
    template_name = "incassi/list_incassi.html"
    context_object_name = "incassi"

class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = ''

class HomeView(ListView):
    model = Incasso
    template_name = "incassi/list_incassi.html"
    context_object_name = "incassi"
    def get_queryset(self):
        # Ordina gli oggetti per data in ordine decrescente (i dati più recenti per primi)
        return Incasso.objects.order_by('data')