import os
import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, render_to_response, redirect, reverse
from django.core.cache import cache

from mycoconut.celery import app as celery_app

import numpy as np

from core import tasks
from dolly.processing import draw_boxes, draw_landmarks
from dolly.utils import image_loader, crop_image


def index(request):
    return render(request, 'core/index.html')


def demo(request):
    return render(request, 'core/demo.html')


def dolly(request, job_id=None):
    if request.method == 'POST' and request.FILES['myimage']:
        # Save image
        myfile = request.FILES['myimage']
        fs = FileSystemStorage()
        filename = fs.save('uploads/' + myfile.name, myfile)

        # Get local filename (path)
        MEDIA_ROOT = os.path.normpath(settings.MEDIA_ROOT)
        filename_m = MEDIA_ROOT + '/' + filename

        # Draw rectangle faces
        path_boxes = 'processed/' + str(uuid.uuid1()) + '.jpg'
        face_0, face_locations = draw_boxes(np_image=image_loader(filename_m), save_path=MEDIA_ROOT + '/' + path_boxes)

        # Check number of faces
        if len(face_locations) > 0:
            # Crop face[0]
            path_face = 'processed/' + str(uuid.uuid1()) + '.jpg'
            pil_face_0 = crop_image(np_image=image_loader(filename_m), coords=face_locations[0])
            draw_landmarks(np_image=image_loader(pil_face_0), save_path=MEDIA_ROOT + '/' + path_face)

            # Find clones
            i = celery_app.control.inspect()
            job_id = str(tasks.async_findclones.delay(filename_m, top_k=10))
            jobs_active = i.active()

            # Add params
            request.session['job_id'] = job_id
            context = {'img_boxes': fs.url(path_boxes),
                       'img_face': fs.url(path_face),
                       'job_id': job_id,
                       'jobs_ahead': len(next(iter(jobs_active.values())))}

            # Save result in cache
            cache.set('res-' + job_id, context)
            return redirect(reverse('dolly_get_job', args=[job_id]))

        else:  # No faces were found
            context = {'error': 'no_faces'}
            return render(request, 'core/dolly.html', context)
    return render(request, 'core/dolly.html')


def dolly_get_job(request, job_id=None):
    # Get page params from cache
    context = cache.get('res-' + job_id)

    if job_id and context:
        return render(request, 'core/dolly.html', context)
    else:  # No job or invalid
        return redirect('dolly')
