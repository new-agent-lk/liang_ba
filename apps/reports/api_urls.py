from rest_framework.routers import DefaultRouter

from .viewsets.public import PublicReportViewSet
from .viewsets.research_report import ResearchReportViewSet

router = DefaultRouter()
router.register(r"reports", ResearchReportViewSet, basename="report")
router.register(r"public/reports", PublicReportViewSet, basename="public-report")

urlpatterns = router.urls
