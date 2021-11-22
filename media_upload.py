from django.shortcuts import render
from django.conf import settings
from PIL import Image
from django.http import HttpResponse
import json 
import time
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def upload_img(request):
    file = request.FILES['file']
    data = {
        'error':True,
        'path':'',
    }
    if file:
        timenow = int(time.time()*1000)
        timenow = str(timenow)
        try:
            img = Image.open(file)
            img.save(settings.MEDIA_ROOT + "content/" + timenow + unicode(str(file)))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        imgUrl =  'content/' + timenow + str(file)
        data['error'] = False
        data['path'] = imgUrl
    return HttpResponse(json.dumps(data), content_type="application/json")
