from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import GenerateAndSendTokenView

from .views import *



router = DefaultRouter()
router.register(r'trainers', TrainerViewSet, basename= 'trainers')

router.register(r'invoices', InvoiceViewSet, basename= 'invoices')



urlpatterns = [
    path("", include(router.urls)),
]


urlpatterns += [
    path("token/", GenerateAndSendTokenView.as_view(), name="send_token"),
    path("trainer_register/", TrainerRegisterView.as_view(), name="register"),
    

]

