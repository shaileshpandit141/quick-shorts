from django.http import JsonResponse
from django.views.generic import TemplateView


def custom_404_apiview(request, exception=None):
    """
    Custom 404 error handler that returns a JSON response when a page/endpoint is not found.

    This view handles 404 errors by returning a JSON response with error details instead of
    the default HTML 404 page. This is useful for API endpoints where JSON responses are expected.
    """
    return JsonResponse(
        {
            "message": "The requested endpoint could not be found.",
            "errors": [
                {
                    "field": "none",
                    "code": "404_not_found",
                    "message": "The requested endpoint could not be found. Please check the URL and try again.",
                    "details": None,
                }
            ],
        },
        status=404,
    )


class IndexTemplateView(TemplateView):
    """
    View for rendering the main index.html template.

    This view inherits from Django's TemplateView to provide a simple way to render
    the index.html template. The template_name class variable specifies which template
    to use.
    """

    template_name = "index.html"
