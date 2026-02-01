from django.urls import path
from .views import ReportListView, ReportDetailView

urlpatterns = [
    path('', ReportListView.as_view(), name='report_list'),
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:id>/', ReportDetailView.as_view(), name='report_detail'),
]
