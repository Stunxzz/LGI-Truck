from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, View
from transfer.forms import PlantTransferForm
from transfer.models import PlantTransfer


class CreatePlantView(LoginRequiredMixin, CreateView):

    model = PlantTransfer
    form_class = PlantTransferForm
    template_name = 'create_plant_transfer.html'
    success_url = reverse_lazy('plants_list')

    def form_valid(self, form):
        messages.success(self.request, 'Plant transfer created.')
        return super().form_valid(form)


class UpdatePlantView(LoginRequiredMixin, UpdateView):
    model = PlantTransfer
    form_class = PlantTransferForm
    template_name = 'create_plant_transfer.html'
    success_url = reverse_lazy('plants_list')

    def form_valid(self, form):
        messages.success(self.request, 'Plant transfer updated.')
        return super().form_valid(form)



class ListPlantTransfersView(LoginRequiredMixin, ListView):
    model = PlantTransfer
    template_name = 'list_plant_transfers.html'
    context_object_name = 'plant_transfers'


class DeletePlantView(LoginRequiredMixin, View):
    model = PlantTransfer

    def get(self, request, *args, **kwargs):
        plant_id = self.kwargs.get('plant_id')

        try:
           PlantTransfer.objects.get(id=plant_id)

        except PlantTransfer.DoesNotExist:
            messages.error(request, 'Plant transfer does not exist.')

        messages.success(request, 'Plant transfer deleted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('plants_list')))

