from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, View
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from transfer.models import PlantTransfer
from .models import DeliveryNote
from .forms import DeliveryNoteForm

class CreateDeliveryNoteView(LoginRequiredMixin ,SuccessMessageMixin, CreateView):
    model = DeliveryNote
    form_class = DeliveryNoteForm
    template_name = 'create_delivery_note.html'
    success_url = reverse_lazy('delivery_note_list')  # Пренасочваме към списъка с Delivery Notes
    success_message = "Delivery Note successfully created."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Plant transfer created.')
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant_transfers'] = PlantTransfer.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # подаваме user към формата
        return kwargs


class UpdateDeliveryNoteView(LoginRequiredMixin ,SuccessMessageMixin, UpdateView):
    model = DeliveryNote
    form_class = DeliveryNoteForm
    template_name = 'create_delivery_note.html'
    success_url = reverse_lazy('delivery_note_list')
    success_message = "Delivery Note successfully updated."

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant_transfers'] = PlantTransfer.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # подаваме user към формата
        return kwargs



class DeliveryNoteListView(LoginRequiredMixin, ListView):
    model = DeliveryNote
    template_name = 'delivery_note_list.html'
    context_object_name = 'delivery_notes'

    def get_queryset(self):
        return DeliveryNote.objects.select_related('package_type', 'created_by').filter(value__isnull=True)




class DeleteDeliveryNoteView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = DeliveryNote
    def get(self, request, *args, **kwargs):
        delivery_note_id = self.kwargs['delivery_note_id']
        try:
            DeliveryNote.objects.get(id=delivery_note_id).delete()

        except DeliveryNote.DoesNotExist:
            messages.error(request, 'Plant transfer does not exist.')
        messages.success(request, 'Delivery Note deleted.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('delivery_note_list')))

