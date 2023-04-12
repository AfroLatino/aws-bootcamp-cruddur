from datetime import datetime, timedelta, timezone
class SearchActivities:
  def run(search_term):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if search_term == None or len(search_term) < 1:
      model['errors'] = ['search_term_blank']
    else:
      results = [{
        'uuid': 'ad9da6e9-71ee-4ef1-80a1-44960b08905a',
        'handle':  'AfroLatino',
        'message': 'Cloud is fun!',
        'created_at': now.isoformat()
      }]
      model['data'] = results
    return model