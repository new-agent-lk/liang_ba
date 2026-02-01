from rest_framework.routers import DefaultRouter
from .viewsets.research_report import ResearchReportViewSet
from .viewsets.public import PublicReportViewSet

router = DefaultRouter()
router.register(r'reports', ResearchReportViewSet, basename='report')
router.register(r'public/reports', PublicReportViewSet, basename='public-report')

urlpatterns = router.urls
