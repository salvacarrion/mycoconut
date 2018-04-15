import json
from django.views.decorators.csrf import csrf_exempt

from core.utils import json_response
from raefinder import *


@csrf_exempt
def get_number(request):

    try:
        if request.method == 'POST':
            number = int(request.POST['number'])
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