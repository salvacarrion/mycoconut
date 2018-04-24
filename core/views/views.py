import os, time
import uuid
from celery.result import AsyncResult
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from mycoconut.celery import app as celery_app

from core import tasks
from dolly import *


def index(request):
    return render(request, 'core/index.html')


def demo(request):
    return render(request, 'core/demo.html')


def dolly(request):
    if request.method == 'POST' and request.FILES['myimage']:

        # Save image
        myfile = request.FILES['myimage']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        # Get local filename (path)
        MEDIA_ROOT = os.path.normpath(settings.MEDIA_ROOT)
        filename_m = MEDIA_ROOT + '/' + filename

        # Draw rectangle faces
        path_boxes = str(uuid.uuid1()) + '.jpg'
        face_0, face_locations = draw_boxes(filename_m, MEDIA_ROOT + '/' + path_boxes, console=False)

        # Crop face[0]
        path_face = str(uuid.uuid1()) + '.jpg'
        pil_face_0 = crop_image(face_0, face_locations[0], console=False)
        draw_landmarks(np.array(pil_face_0), MEDIA_ROOT + '/' + path_face, console=False)

        # Find clones
        i = celery_app.control.inspect()
        job_id = str(tasks.async_findclones.delay(filename_m, top_k=10))
        # a = i.scheduled()
        jobs_active = i.active()
        # c = i.reserved()
        # d = i.registered()
        #

        # Add params
        request.session['job_id'] = job_id
        context = {'img_boxes': fs.url(path_boxes),
                   'img_face': fs.url(path_face),
                   'job_id': job_id,
                   'jobs_ahead': len(next(iter(jobs_active.values())))}

        return render_to_response('core/dolly.html', context)
    else:
        return render(request, 'core/dolly.html')
