import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .document_chat import retrieval_chat

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def getchatresponse(request):
    if request.body:
        try:
            data = json.loads(request.body)
            chat_prompt = data.get("prompt", "")

            # Initialize  retrieval_chat object
            qa = retrieval_chat()

            # Call answer_question method to get a response
            response = qa.answer_question(chat_prompt)

            return JsonResponse({"response": response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Empty request body"}, status=400)
