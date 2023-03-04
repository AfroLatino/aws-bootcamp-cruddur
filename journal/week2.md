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

### Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend

```sh
// tracing.js
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource }  from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const exporter = new OTLPTraceExporter({
  url: 'https://<your collector endpoint>:443/v1/traces'
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

I was unable to implement this. I made good progress in following the steps on Honeycomb's website. However, with my limited react JavaScript knowledge, I was unable to fully implement this. 


### References

[OpenTelemetry By Marc Pichler](https://github.com/open-telemetry/opentelemetry-js)

[HoneyComb OpenTelemetry](https://docs.honeycomb.io/getting-data-in/opentelemetry/browser-js/)

[OpenTelemetry Docs](https://opentelemetry.io/docs/instrumentation/js/getting-started/browser/)

[OpenTelemetry Bootcamp](https://github.com/aspecto-io/opentelemetry-bootcamp/blob/master/src/ws-instrumentation/ws.ts)


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


