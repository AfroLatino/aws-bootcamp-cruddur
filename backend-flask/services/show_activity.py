from datetime import datetime, timedelta, timezone
class ShowActivities:
  def run(activity_uuid):
    now = datetime.now(timezone.utc).astimezone()
    results = [{
      'uuid': 'a8d37d5c-4b42-4a89-90e8-7cf0ab1d6c00',
      'handle':  'AfroLatino',
      'message': 'Cloud is fun!',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'replies': {
        'uuid': 'a8d37d5c-4b42-4a89-90e8-7cf0ab1d6c00',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'created_at': (now - timedelta(days=2)).isoformat()
      }
    }]
    return results