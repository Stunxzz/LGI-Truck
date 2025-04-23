from django.contrib import messages
from django.views.generic import ListView
from .models import Order
from .forms import OrderFilterForm

# views.py
class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.none()

        loading_date = self.request.GET.get('loading_date')
        status = self.request.GET.get('status')

        if loading_date and status:
            queryset = Order.objects.prefetch_related('delivery_notes')

            if status == 'pending':
                queryset = queryset.filter(status=0)
            elif status == 'sent':
                queryset = queryset.filter(status=1)

            queryset = queryset.filter(loading_date=loading_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = OrderFilterForm(self.request.GET)
        context['submitted'] = 'loading_date' in self.request.GET and 'status' in self.request.GET
        if context['submitted'] and not context['orders']:
            messages.info(self.request, "No orders found for the selected date and status.")
        return context

