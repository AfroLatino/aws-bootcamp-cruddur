# Week 2 — Distributed Tracing

## Required Homework Challenges

Instrumented my backend flask application to use Open Telemetry (OTEL) with Honeycomb.io as the provider.

Watched the security video of Observability vs Monitoring in AWS.

Instrumented WAS X-Ray into backend flask application.

Configured logging in AWS Cloud Watch using CLI.

All these are evident on my repository and AWS account.

### Challenges faced

I was unable to view some of the contents of the frontend page last week, so had to start delete some files and re-start some of the exercises from Week 0.

I have now completed all my mandatory homework from Week 0 - 2.


## Stretch Homework Challenges

### Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend

I was unable to implement this. However, I read the documentation below:

[Open Telemetry By Marc Pichler](https://github.com/open-telemetry/opentelemetry-js)

[HoneyComb Open Telemetry](https://docs.honeycomb.io/getting-data-in/opentelemetry/browser-js/)

[Open Telemetry Docs](https://opentelemetry.io/docs/instrumentation/js/getting-started/browser/)

### •	Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span

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
