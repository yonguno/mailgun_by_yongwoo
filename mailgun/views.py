from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import httpRes

@csrf_exempt
def post(req):
  if req.method == 'GET':
    return HttpResponse('<html><body>send post</body></html>')
  return httpRes.on_incoming_message(req)

def test(req):
  return HttpResponse('<html><body>test</body></html>')
