from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView,  View
from .forms import PackageForm
from .models import Package


class PackageCreateView(LoginRequiredMixin, CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'create_packages.html'
    success_url = reverse_lazy('package_list')

    def form_valid(self, form):
        messages.success(self.request, 'Package created successfully.')
        return super().form_valid(form)






class PackageUpdateView(LoginRequiredMixin, UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'create_packages.html'
    success_url = reverse_lazy('package_list')

    def form_valid(self, form):
        messages.success(self.request, 'Package updated successfully.')
        return super().form_valid(form)





class PackageListView(LoginRequiredMixin, ListView):
    model = Package
    template_name = 'packages_list.html'
    context_object_name = 'packages'






class DeletePackageView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        package_id = kwargs.get('package_id')

        try:
            package = Package.objects.get(id=package_id)
            package.delete()
            messages.success(request, f'Package "{package.type}" deleted successfully.')
        except Package.DoesNotExist:
            messages.error(request, "Package does not exist.")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('package_list')))