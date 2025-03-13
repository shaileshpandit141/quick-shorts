from django.http import JsonResponse
from django.views.generic import TemplateView


def custom_404_apiview(request, exception=None) -> JsonResponse:
    """Custom 404 error handler that returns a JSON response when a
    page/endpoint is not found.
    """
    return JsonResponse(
        {
            "message": "The requested endpoint could not be found.",
            "data": {},
            "errors": {
                "detail": "The requested endpoint could not be found. Please check the URL and try again.",
            },
        },
        status=404,
    )


class IndexTemplateView(TemplateView):
    """View for rendering the main index.html template
    for index page.
    """

    template_name = "index.html"
