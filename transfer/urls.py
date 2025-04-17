from django.urls import path
from .views import (
    CreatePlantView,
    UpdatePlantView,
    DeletePlantView,
    ListPlantTransfersView,
)

urlpatterns = [
    path('', ListPlantTransfersView.as_view(), name='plants_list'),
    path('create/', CreatePlantView.as_view(), name='create_plant'),
    path('update/<int:pk>/', UpdatePlantView.as_view(), name='update_plant'),
    path('delete/<int:plant_id>/', DeletePlantView.as_view(), name='delete_plant'),
]
