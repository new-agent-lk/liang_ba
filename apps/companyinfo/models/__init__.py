#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .choices import (
    JOB_CATEGORY_CHOICES,
    RECRUITMENT_TYPE_CHOICES,
    EDUCATION_CHOICES,
)
from .province import Province
from .city import City
from .company_info import CompanyInfo
from .friendly_links import FriendlyLinks
from .job_position import JobPosition
from .resume import Resume

__all__ = [
    'JOB_CATEGORY_CHOICES',
    'RECRUITMENT_TYPE_CHOICES',
    'EDUCATION_CHOICES',
    'Province',
    'City',
    'CompanyInfo',
    'FriendlyLinks',
    'JobPosition',
    'Resume',
]
