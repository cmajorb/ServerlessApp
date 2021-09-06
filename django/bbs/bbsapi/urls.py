# bbsapi/urls.py
from django.urls import include, path,re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'contracts', views.ContractViewSet)
router.register(r'owners', views.OwnerViewSet)
router.register(r'tenants', views.TenantViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'payments', views.PaymentViewSet, basename='payments')
router.register(r'invoices', views.InvoiceViewSet, basename='invoices')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    path('reports',views.ReportDownloadView.as_view()),
    path('generateinvoices',views.GenerateInvoices.as_view())
]
