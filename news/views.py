from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .news import page_request, fetchHeadlines, fetchContents
import pandas as pd

# Your Django view function
@csrf_exempt  # Use this decorator for testing purposes; ensure CSRF protection in production
def get_news_data(request):
    if request.method == 'GET':
        df = pd.DataFrame(data={'headlines': 'NaN', 'content': 'NaN', 'img_link': 'NaN'}, index=[0])
        counter, df = fetchHeadlines(page_request(1), df)
        for DataInstance in df.iterrows():
            NewsInstance = dict(DataInstance[1])
            while NewsInstance['content'].count("") != 0:
                NewsInstance['content'].remove("")
            df.iloc[DataInstance[0], 1] = NewsInstance['content']
        if counter > 0:
            data = df.to_dict(orient='records')
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'message': 'No data available.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
