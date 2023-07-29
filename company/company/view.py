from django.urls import reverse
from django.views.generic import RedirectView


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('wagtail_serve', args=('liang-ba/',))

