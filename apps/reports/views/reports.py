from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import Http404

from apps.reports.models import ResearchReport
from apps.companyinfo.models import CompanyInfo


class ReportListView(ListView):
    """
    报告列表页
    """
    template_name = 'reports_list.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        # 只返回已发布且公开的报告
        queryset = ResearchReport.objects.filter(
            is_public=True,
            status='published'
        ).select_related('author').order_by('-is_top', '-published_at')

        # 按年月筛选
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')

        if year:
            queryset = queryset.filter(published_at__year=int(year))
        if month:
            queryset = queryset.filter(published_at__month=int(month))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取所有有报告的年份
        years = ResearchReport.objects.filter(
            is_public=True,
            status='published'
        ).annotate(
            year=ExtractYear('published_at')
        ).values_list('year', flat=True).distinct().order_by('-year')

        # 如果有年份筛选，获取该年的月份
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        if year:
            months = ResearchReport.objects.filter(
                is_public=True,
                status='published',
                published_at__year=int(year)
            ).annotate(
                month=ExtractMonth('published_at')
            ).values_list('month', flat=True).distinct().order_by('month')
        else:
            months = []

        # 获取当前筛选的年月
        current_year = int(year) if year else None
        current_month = int(month) if month else None

        context.update({
            'companyinfo': CompanyInfo.objects.first(),
            'available_years': sorted(years, reverse=True),
            'available_months': list(months),
            'current_year': current_year,
            'current_month': current_month,
        })
        return context


class ReportDetailView(DetailView):
    """
    报告详情页
    """
    template_name = 'report_detail.html'
    context_object_name = 'report'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        # 只返回已发布且公开的报告
        return ResearchReport.objects.filter(
            is_public=True,
            status='published'
        ).select_related('author')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 增加阅读量
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取公司信息
        context['companyinfo'] = CompanyInfo.objects.first()
        # 将标签字符串转换为列表
        report = self.object
        if report.tags:
            context['report_tags'] = [tag.strip() for tag in report.tags.split(',')]
        else:
            context['report_tags'] = []
        return context
