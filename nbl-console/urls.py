from django.urls import path
from . import views

urlpatterns = [

    # Custom scripts
    path('scripts/', views.ScriptManagementView.as_view(), name='scripts'),
    path('scripts/delete/', views.ScriptDeleteView.as_view(), name='scripts_delete'),

    # Reports
    path('reports/', views.ReportManagementView.as_view(), name='reports'),
    path('reports/delete/', views.ReportDeleteView.as_view(), name='reports_delete'),

    # Configuration
    path('configuration/', views.ConfigurationView.as_view(), name='configuration'),

]
