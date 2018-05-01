import json

from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings

from celery.result import AsyncResult
from mycoconut.celery import app as celery_app

from core.utils import json_response
from raefinder import *
from dolly import *

from dolly.config import get_default_ds, get_db_path
from dolly.db import create_connection

DB_PATH = get_db_path(get_default_ds())


def job_response(async_result):
    cel_get = async_result.get()
    job_type = cel_get['job_type']

    # Prepare response based on the processed job
    if job_type == 'findclones':
        context = cache.get('res-' + async_result.id)

        # Get candidates info
        if not context.get('top_candidates'):
            conn = create_connection(DB_PATH)
            cur = conn.cursor()
            with conn:

                top_candidates = []
                for c in cel_get['res']:
                    face_id, freebase_mid, entity_name, dist = c
                    isr = cur.execute('SELECT * FROM faces WHERE id=?', (face_id,)).fetchone()[6]  # REALLY BAD CODE!

                    image_url = '{}/{}/{}-FaceId-0.jpg'.format('msceleb', freebase_mid, isr)
                    top_candidates.append({'id': face_id, 'freebase_mid': freebase_mid, 'image_url': image_url,
                                           'name': entity_name, 'dist': dist})

            # Render html
            clones_html = render_to_string('core/includes/findclones.html', context={'top_candidates': top_candidates})

            # Save params
            context['top_candidates'] = top_candidates
            context['clones_html'] = clones_html

        # Get info from Google Knowledge Graph
        if not context.get('gkg_entity'):
            matched = context['top_candidates'][0]
            gkg_res = get_more_info(api_key=getattr(settings, 'GKG_API', None), ids=matched['freebase_mid'],
                                    languages='es', limit=1)
            if len(gkg_res.get('itemListElement')):
                gkg_entity = gkg_res['itemListElement'][0]['result']
                matched_html = render_to_string('core/includes/matched.html', context={'matched': matched,
                                                                                       'gkg_entity': gkg_entity})
                # Save params
                context['gkg_entity'] = gkg_entity
                context['matched_html'] = matched_html

        # Save in cached
        cache.set('res-' + async_result.id, context)
        return {'clones_html': context.get('clones_html', ''), 'matched_html': context.get('matched_html', '')}

    return None


def check_job_status(request):
    try:
        async_result = AsyncResult(request.GET.get('job_id'))
        if async_result.ready():
            return JsonResponse({'status': 'finished', 'result': job_response(async_result)})
        else:
            i = celery_app.control.inspect()
            jobs_active = i.active()
            return JsonResponse({'status': 'computing', 'jobs_ahead': len(next(iter(jobs_active.values())))})
    except KeyError as e:
        return JsonResponse({'error': 'Invalid Job ID'})


@csrf_exempt
def get_number(request):

    try:
        if request.method == 'POST':
            number = request.POST['number']  # MUST BE STRING => CASE int('021') -> 21 ('0' missing)
            rules = json.loads(request.POST['rules'])

            # Check rules (keys must be int)
            rules = {int(k): [i for i in v] for k, v in rules.items()}

            # Get words
            start_t = time.time()
            words_matched, total_lines, regex = get_words(number, mnemo=rules)
            end_t = time.time() - start_t

            # Prepare result
            res = '-----------------------------\n'
            res += '--        RAEFINDER        --\n'
            res += '-----------------------------\n'

            res += '\n'.join(words_matched)

            # Print results
            if len(words_matched):
                res += '\n\n'
                res += '-------------------------------\n'
                res += '- Words matched: {:,}\n'.format(len(words_matched))
                res += '- Words analyzed: {:,}\n'.format(total_lines)
                res += '- Elapsed time: %.5fs\n' % end_t
                res += '- Regex used: "%s"' % regex
            else:
                res += 'No words matched the expression'

            return json_response(msg=res)
        else:
            return json_response(msg='Invalid request', error=True)

    except Exception as e:
        return json_response(msg=str(e), error=True)

