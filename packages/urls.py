from django.urls import path

from packages.views import PackageListView, PackageUpdateView, PackageCreateView, DeletePackageView

urlpatterns = [
    path('', PackageListView.as_view(), name='package_list'),
    path('create/', PackageCreateView.as_view(), name='package_create'),
    path('<int:pk>/edit/', PackageUpdateView.as_view(), name='package_edit'),
    path('<int:package_id>/delete/', DeletePackageView.as_view(), name='package_delete'),
]