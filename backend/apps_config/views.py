from django.http import JsonResponse
from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    """View for rendering the main index.html template
    for index page.
    """

    template_name = "index.html"
