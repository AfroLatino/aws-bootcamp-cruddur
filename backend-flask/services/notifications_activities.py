from datetime import datetime, timedelta, timezone
class NotificationsActivities:
  def run():
     now = datetime.now(timezone.utc).astimezone()
     results = [{
      'uuid': 'a8d37d5c-4b42-4a89-90e8-7cf0ab1d6c00',
      'handle':  'coco',
      'message': 'I am a white unicorn!',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 5,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
        'uuid': 'a8d37d5c-4b42-4a89-90e8-7cf0ab1d6c00',
        'reply_to_activity_uuid': ' ',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'likes_count': 0,
        'replies_count': 0,
        'reposts_count': 0,
        'created_at': (now - timedelta(days=2)).isoformat()
      }],
    }
    ]
     return results