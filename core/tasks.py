from __future__ import absolute_import, unicode_literals
from celery import shared_task

from dolly import findclones


@shared_task()
def async_findclones(*args, **kwargs):
    clones_res = findclones(*args, **kwargs)
    return {'job_type': 'findclones', 'res': clones_res}
