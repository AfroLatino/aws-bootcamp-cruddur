import './HomeFeedPage.css';
import React from "react";

import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';
import checkAuth from '../lib/CheckAuth';

// Honeycomb-----
//import { trace } from "@opentelemetry/api";
//import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';
//import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
// import { registerInstrumentations } from '@opentelemetry/instrumentation';


export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  //const tracer = trace.getTracer();

  //const rootSpan = tracer.startActiveSpan('document_load', span => {
    //span.setAttribute('pageUrlwindow', window.location.href);
   // window.onload = (event) => {
      
   //  span.end(); 
  //  };
  //});

//  registerInstrumentations({
 //   instrumentations: [
 //     new XMLHttpRequestInstrumentation({
 //       propagateTraceHeaderCorsUrls: [
  //         /.+/g, /^http:\/\/localhost:4567\/.*$/
 //       ]
 //     }),
  //    new FetchInstrumentation({
 //       propagateTraceHeaderCorsUrls: [
//           /.+/g, /^http:\/\/localhost:4567\/.*$/
//        ]
//      }),
//    ],
//  });

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`
           
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
         method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm 
          user_handle={user} 
          popped={popped}
          setPopped={setPopped} 
          setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} 
          popped={poppedReply} 
          setPopped={setPoppedReply} 
          setActivities={setActivities} 
          activities={activities} 
        />
        <ActivityFeed 
          title="Home" 
          setReplyActivity={setReplyActivity} 
          setPopped={setPoppedReply} 
          activities={activities} 
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}