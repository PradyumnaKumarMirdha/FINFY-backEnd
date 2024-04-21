from django.http import JsonResponse
from django.views import View
from .stock import start  # Import your web scraping function

class ScrapingView(View):
    def get(self, request, *args, **kwargs):
        # Get page number and per page count from query parameters
        page_number = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        data = start(page_number=page_number, per_page=per_page)
        return JsonResponse(data, safe=False)  # Return the scraped data as JSON
