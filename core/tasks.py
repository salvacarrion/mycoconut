from __future__ import absolute_import, unicode_literals
from celery import shared_task

from dolly.findclones import Finder as f
from dolly.processing import analyze_face
from dolly.utils import image_loader
from dolly.config import get_default_ds

finder = f(get_default_ds(), in_memory=True)


@shared_task()
def async_findclones(filename, *args, **kwargs):
    f_enc = analyze_face(np_image=image_loader(filename), model='hog')[2]
    clones_res = finder.findclones(face_encoding=f_enc, *args, **kwargs)
    return {'job_type': 'findclones', 'res': clones_res}
