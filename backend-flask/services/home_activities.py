from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import logging

from lib.db import pool, query_wrap_array

tracer = trace.get_tracer("home.activities")

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

      sql = query_wrap_array("""
      SELECT * FROM activities    
      """)
      print("SQL---------")
      print(sql)
      print("SQL..........")
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchone()
        return json[0]
        return results
  