from django.urls import path
from . import views

urlpatterns = [
    path('', views.CloudAPIRootView.as_view(), name='cloud-root'),
    path('stats/', views.CloudStatsView.as_view(), name='cloud-stats'),
    path('count.json', views.ModelCountAPIView.as_view(), name='count-list'),
    path('saml.xml', views.SAMLXMLAPIView.as_view(), name='saml-xml'),
]
