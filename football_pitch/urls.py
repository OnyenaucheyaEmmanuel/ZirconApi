# # YourApp/urls.py
# from django.urls import path
# from .views import initiate_payment, verify_payment

# urlpatterns = [
#     path('initiate-payment/', initiate_payment, name='initiate_payment'),
#     path('verify-payment/<str:ref>/', verify_payment, name='verify_payment'),
#     # Add other URLs as needed
# ]
# booking/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    # other urlpatterns...
]
