from rest_framework import routers
from .views import ImageViewSet, TemplateViewSet, TransactionViewSet

router = routers.DefaultRouter();
router.register(r'template', TemplateViewSet)
router.register(r'image', ImageViewSet)
router.register(r'transaction', TransactionViewSet)

