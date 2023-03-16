from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import logging

from lib.db import db

#tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None): 
     # logger.info("HomeActivities")
    ## HoneyComb Span addition
    #with tracer.start_as_current_span("http-handler") as outer_span:
    #    outer_span.set_attribute("http-handler", True)
    #with tracer.start_as_current_span("home-activities-mock-data"):
      #span = trace.get_current_span()
      #now = datetime.now(timezone.utc).astimezone()
      #span.set_attribute("user.id", 'AfroLatino')
      #span.set_attribute("app.now", now.isoformat())  
    sql = db.template('activities','home')
    results = db.query_array_json(sql)     
    return results
  