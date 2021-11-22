from django.shortcuts import render
from django.conf import settings
from PIL import Image
from django.http import HttpResponse
import json
import time
from django.views.decorators.csrf import csrf_exempt
import os
from pathlib import Path

# Create your views here.


@csrf_exempt
def upload_img(request):
    file = request.FILES['file']
    print(file)
    data = {
        'location': '',
    }
    print(data)
    if file:
        timenow = int(time.time()*1000)
        timenow = str(timenow)
        try:
            img = Image.open(file)
            path = Path(settings.MEDIA_ROOT)
            name = str(request.user)+timenow+str(file)
            os.chdir(path)
            img.save(name)
            print(name)
            #img.save(os.path.join(settings.MEDIA_ROOT + "content/" + timenow + unicode(str(file))))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        imgUrl = settings.MEDIA_URL + str(request.user)+timenow + str(file)
        data['location'] = imgUrl
        print(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


def create(request):
    return render(request, 'change_form.html', {})
