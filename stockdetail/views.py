from django.http import JsonResponse
from django.views import View
from .stockdetail import StockDetail  # Import your web scraping function

class ScrapingView(View):
    def get(self, request, *args, **kwargs):
        # Get the stock symbol from the query parameters
        stock_symbol = request.GET.get('symbol')

        # Call the StockDetail function with the provided stock symbol
        stock_data = StockDetail(stock_symbol)

        # Return the scraped data as JSON response
        return JsonResponse(stock_data)
    
    # http://127.0.0.1:8000/stockdetailapi/stock-detail/?symbol=name