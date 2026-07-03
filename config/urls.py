from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from references.views import (
    CategoryViewSet,
    OperationTypeViewSet,
    StatusViewSet,
    SubcategoryViewSet,
)
from transactions.views import OperationViewSet

router = DefaultRouter()

router.register(
    'statuses', StatusViewSet, basename='status'
)
router.register(
    'operation-types', OperationTypeViewSet, basename='operation-type'
)
router.register(
    'categories', CategoryViewSet, basename='category'
)
router.register(
    'subcategories', SubcategoryViewSet, basename='subcategory'
)
router.register(
    'operations', OperationViewSet, basename='operation'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
