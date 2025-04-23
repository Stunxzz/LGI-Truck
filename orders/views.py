import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, View
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
        context['ordersId'] = list(self.get_queryset().values_list('id', flat=True))

        return context



class UpdateOrderStatusView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order_ids = data.get('orderIds', [])

            if not order_ids:
                return JsonResponse({'success': False, 'message': 'No order IDs provided.'})
            updated_count = Order.objects.filter(id__in=order_ids).update(status=1)
            messages.success(request, f'{updated_count} orders were successfully updated.')

            return JsonResponse({'success': True, 'updated': updated_count})

        except Exception as e:
            messages.error(request, 'An error occurred while updating orders.')
            return JsonResponse({'success': False, 'message': str(e)})
#
# from django.shortcuts import redirect

