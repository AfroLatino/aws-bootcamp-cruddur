# Week 2 — Distributed Tracing

## Required Homework Challenges

Instrumented my backend flask application to use Open Telemetry (OTEL) with Honeycomb.io as the provider.

Watched the security video of Observability vs Monitoring in AWS.

Instrumented WAS X-Ray into backend flask application.

Configured logging in AWS Cloud Watch using CLI.

All these are evident on my repository and AWS account. I have attached some screemshots below:

![Rollbar sceenshot](https://user-images.githubusercontent.com/78261965/222268656-3de67036-5210-4981-b105-4fbfbb7929ad.png)

![WAS Xray Traces](https://user-images.githubusercontent.com/78261965/222268717-a8372539-39f3-4bbe-a9ee-aeb7f74898cc.png)

![CloudWatch Logs](https://user-images.githubusercontent.com/78261965/222268732-24f32359-142d-4a22-95b6-e935c6ae24f6.png)


### Challenges faced

I was unable to view some of the contents of the frontend page last week, so had to start delete some files and re-start some of the exercises from Week 0.

I have now completed all my mandatory homework from Week 0 - 2.


## Stretch Homework Challenges

### AWS X-Ray Subsegments

Subsegments extend a trace's segment with details about work done in order to serve a request. Each time you make a call with an instrumented client, the X-Ray SDK records the information generated in a subsegment

After watching the live stream video, I was able to create an AWS Subsegment as seen from the screenshots below:

![subsegment nodes](https://user-images.githubusercontent.com/78261965/223013359-1796090e-6ef6-4c09-807d-75be37caaa3c.png)

![Subsegments screenshot](https://user-images.githubusercontent.com/78261965/223013365-00977f00-dc9f-447b-aacd-d165496a1d65.png)


### Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend

I did a test span through Postman on my Honeycomb application and got the results below:

![TestWithCurl](https://user-images.githubusercontent.com/78261965/222917353-8b170471-c735-455a-90de-928767754eb4.png)

I created an OTEL collector yaml file to receive, process and export telemetry data. It removes the need to run, operate, and maintain multiple agents/collectors.

I added the packages below to instrument my Web Page.

```sh
npm install --save \
    @opentelemetry/api \
    @opentelemetry/sdk-trace-web \
    @opentelemetry/exporter-trace-otlp-http \
    @opentelemetry/context-zone
```

An initiation file called ```tracing.js``` was created as seen below:

```sh
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource }  from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const exporter = new OTLPTraceExporter({
 url: `${process.env.REACT_APP_OTEL_COLLECTOR_URL}/v1/traces`
});
const provider = new WebTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'browser',
  }),
});
provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register({
  contextManager: new ZoneContextManager()
});
```

#### Instrumentation for actions were added to my HomeFeedPage as seen below:

```sh
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer();

const rootSpan = tracer.startActiveSpan('document_load', span => {
  //start span when navigating to page
  span.setAttribute('pageUrlwindow', window.location.href);
  window.onload = (event) => {
    span.end(); //once page is loaded, end the span
  };
```

Then, I was able to view my frontend-react-js dataset in Honeycomb. Find the screenshots below:

![frontend screenshot](https://user-images.githubusercontent.com/78261965/222918108-4caf9a70-8555-4b60-807c-ef2b49e68632.png)

![Frontend query](https://user-images.githubusercontent.com/78261965/222918119-cf9a61fc-0bbf-4c97-af67-98898297159a.png)

#### Connecting the Frontend and Backend Traces 

I installed the packages below

```sh
npm install --save \
    @opentelemetry/instrumentation \
    @opentelemetry/instrumentation-xml-http-request \
    @opentelemetry/instrumentation-fetch
```

I propagated the trace header automatically by setting this configuration property of instrumentation-xml-http-request and instrumentation-fetch packages.

```sh
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { registerInstrumentations } from '@opentelemetry/instrumentation';

registerInstrumentations({
  instrumentations: [
    new XMLHttpRequestInstrumentation({
      propagateTraceHeaderCorsUrls: [
         /.+/g, //Regex to match your backend urls. This should be updated.
      ]
    }),
    new FetchInstrumentation({
      propagateTraceHeaderCorsUrls: [
         /.+/g, //Regex to match your backend urls. This should be updated.
      ]
    }),
  ],
});
```
Find below the screenshot of the tracing between the frontend and backend application.

![Frontend to backend tracing](https://user-images.githubusercontent.com/78261965/222918396-704b3269-da59-4517-a898-f408174c1723.png)

### References

[OpenTelemetry By Marc Pichler](https://github.com/open-telemetry/opentelemetry-js)

[HoneyComb OpenTelemetry](https://docs.honeycomb.io/getting-data-in/opentelemetry/browser-js/)

[OpenTelemetry Docs](https://opentelemetry.io/docs/instrumentation/js/getting-started/browser/)

[OpenTelemetry Bootcamp](https://github.com/aspecto-io/opentelemetry-bootcamp/blob/master/src/ws-instrumentation/ws.ts)

[Honeycomb Blog](https://www.honeycomb.io/blog/test-span-opentelemetry-collector)

[Otel Collector](https://opentelemetry.io/docs/collector/)

[Support from Discord](https://github.com/annleefores/aws-bootcamp-cruddur-2023)


### Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span

I added UserID and a custom span of http-handler to the home-activities.py page as seen below:

```sh
span = trace.get_current_span()
 span.set_attribute("user.id", 'AfroLatino')
```
```sh
with tracer.start_as_current_span("http-handler") as outer_span:
        outer_span.set_attribute("http-handler", True)        
```

![Custom Instrumentation UserID](https://user-images.githubusercontent.com/78261965/222267130-022ea7b6-e719-4341-ac3a-2d50776bc442.png)

![Custom Span Instrumentation](https://user-images.githubusercontent.com/78261965/222267195-dbabe541-d289-4905-a2ba-b721f8fc27e9.png)

These are all available within my HoneyComb account via the link below:

[Honeycomb Share Link](https://ui.honeycomb.io/afrolatino/environments/bootcamp/datasets/backend-flask/result/4WadRwe72UB)


### Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces

Please see screenshots of my queries below:

![Latency By UserID](https://user-images.githubusercontent.com/78261965/222270205-a98a7d20-ca36-4c35-b299-149d35d64cb4.png)

![RecentTraces](https://user-images.githubusercontent.com/78261965/222270228-b53ec6b3-fc58-4e35-a452-93541a2e7d78.png)

![Honeycomb Saved Queries](https://user-images.githubusercontent.com/78261965/222272946-771061b0-a02c-4f26-ae6c-d20b77a51629.png)


