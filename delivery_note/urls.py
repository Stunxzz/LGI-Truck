from django.urls import path
from .views import CreateDeliveryNoteView, UpdateDeliveryNoteView, DeliveryNoteListView

urlpatterns = [
    path('', DeliveryNoteListView.as_view(), name='delivery_note_list'),
    path('create/', CreateDeliveryNoteView.as_view(), name='create_delivery_note'),
    path('update/<int:pk>', UpdateDeliveryNoteView.as_view(), name='update_delivery_note'),

    path('delete/<int:plant_id>/', DeliveryNoteListView.as_view(), name='delete_delivery_note')

]