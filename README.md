# Red Hat One 2025 Distributed Tracing with OpenShift ServiceMesh

## local requirements

* get the `otel-cli` from https://github.com/equinix-labs/otel-cli/releases/tag/v0.4.5
* run the otel-collector with

    ``` 
    chcon -t container_file_t collector.yml
    ./otel-collector
    ``` 

* install the python packages for the otel libraries

    ``` 
    pip install --user -r requirements.txt
    ``` 

### running on Linux 

* deploy the rsyslog otel configuration

    ```
    sudo cp rsyslog-otel.conf /etc/rsyslog.d/otel.conf
    ``` 

* if you want to use the default logger for user logs, enable the socket accordingly

    ```file:/etc/rsyslog.conf
    module(load="imuxsock"
       SysSock.Use="off") # change to on instead
    ```  

* restart rsyslog to load the new configurations

    ``` 
    sudo systemctl restart rsyslog
    ``` 

## basic trace setup

* generate a new traceid

    ```
    export trace_id=$(otel generate trace_id)
    ```

* generate a new spanid
 
    ```
    export span_id=$(otel generate span_id)
    ``` 

* craft the traceparent 

    ``` 
    export TRACEPARENT="01-${trace_id}-${span_id}-01"
    ``` 

## create a simple trace 

* with the `TRACEPARENT` crafted we can use the otel-cli or the example-trace script

    ``` 
    python example-trace.py
    ``` 

* check the otel pod logs to see the trace being received

    ```
    podman logs otel
    ```

        ```
        2025-02-13T14:05:12.046Z        info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
        2025-02-13T14:05:12.046Z        info    ResourceSpans #0
        Resource SchemaURL:
        Resource attributes:
             -> telemetry.sdk.language: Str(python)
             -> telemetry.sdk.name: Str(opentelemetry)
             -> telemetry.sdk.version: Str(1.14.0)
             -> service.name: Str(example)
             -> service.namespace: Str(example)
             -> service.version: Str(v1.0)
        ScopeSpans #0
        ScopeSpans SchemaURL:
        InstrumentationScope __main__
        Span #0
            Trace ID       : bcc240ae671572d0625810db5a8e0dda
            Parent ID      : fcf926aa13a16bee
            ID             : a0d8f460016db704
            Name           : example
            Kind           : Internal
            Start time     : 2025-02-13 14:05:11.952752 +0000 UTC
            End time       : 2025-02-13 14:05:11.97405 +0000 UTC
            Status code    : Ok
            Status message :
        Events:
        SpanEvent #0
             -> Name: Hello World
             -> Timestamp: 2025-02-13 14:05:11.974035 +0000 UTC
             -> DroppedAttributesCount: 0
             -> Attributes::
                  -> name: Str(example)
                  -> another: Str(attribute)
                {"kind": "exporter", "data_type": "traces", "name": "debug"}
       ```

* using the otel-cli instead and listing the directory 

    ```
    otel-cli exec -- ls 
    ```

        ```
        2025-02-13T14:06:32.818Z        info    Traces  {"kind": "exporter", "data_type": "traces", "name": "debug", "resource spans": 1, "spans": 1}
        2025-02-13T14:06:32.818Z        info    ResourceSpans #0
        Resource SchemaURL: https://opentelemetry.io/schemas/1.17.0
        Resource attributes:
             -> service.name: Str(otel-cli)
        ScopeSpans #0
        ScopeSpans SchemaURL: https://opentelemetry.io/schemas/1.17.0
        InstrumentationScope github.com/equinix-labs/otel-cli 0.4.5 0d4b8a9c49f60a6fc25ed22863259ff573332060 2024-04-01T20:56:07Z
        Span #0
            Trace ID       : bcc240ae671572d0625810db5a8e0dda
            Parent ID      : fcf926aa13a16bee
            ID             : 3fede839e8142533
            Name           : todo-generate-default-span-names
            Kind           : Client
            Start time     : 2025-02-13 14:06:32.552426 +0000 UTC
            End time       : 2025-02-13 14:06:32.773154 +0000 UTC
            Status code    : Unset
            Status message :
        Attributes:
             -> process.command: Str(ls)
             -> process.command_args: Slice(["ls"])
             -> process.owner: Str(milang)
             -> process.pid: Int(6275)
             -> process.parent_pid: Int(6284)
                {"kind": "exporter", "data_type": "traces", "name": "debug"}
        ```

## create a logs with otel

### running on MacOS 

* use the logger script included as MacOS is not equiped with rsyslog

    ```
    ./logger -p user.info "Testing otel logging" 
    ``` 

        ```
        2025-02-13T14:16:41.183Z        info    Logs    {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
        2025-02-13T14:16:41.184Z        info    ResourceLog #0
        Resource SchemaURL:
        ScopeLogs #0
        ScopeLogs SchemaURL:
        InstrumentationScope
        LogRecord #0
        ObservedTimestamp: 2025-02-13 14:16:41.077621169 +0000 UTC
        Timestamp: 2025-02-13 14:16:41.039646 +0000 UTC
        SeverityText: info
        SeverityNumber: Info(9)
        Body: Str(Testing otel logging )
        Attributes:
             -> application: Str(syslog)
             -> trace_id: Str(bcc240ae671572d0625810db5a8e0dda)
             -> span_id: Str(fcf926aa13a16bee)
             -> trace_flags: Str(01)
             -> version: Int(1)
             -> proc_id: Str(8390)
             -> facility: Int(1)
             -> hostname: Str(Michaelas-MacBook-Pro)
             -> priority: Int(14)
             -> loki.attribute.labels: Str(service_name, service_namespace, application, hostname, host, level, facility, connection_hostname, trace_id, span_id, trace_flags)
             -> loki.format: Str(raw)
        Trace ID: bcc240ae671572d0625810db5a8e0dda
        Span ID: fcf926aa13a16bee
        Flags: 1
                {"kind": "exporter", "data_type": "logs", "name": "debug"}
        ``` 

### running on Linux 

* if using the logger script included

    ```
    ./logger -p user.info "Testing otel logging"
    ```

        ```
        2025-02-13T14:17:48.073Z        info    Logs    {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
        2025-02-13T14:17:48.074Z        info    ResourceLog #0
        Resource SchemaURL:
        ScopeLogs #0
        ScopeLogs SchemaURL:
        InstrumentationScope
        LogRecord #0
        ObservedTimestamp: 2025-02-13 14:17:47.895452598 +0000 UTC
        Timestamp: 2025-02-13 14:17:47.838932 +0000 UTC
        SeverityText: info
        SeverityNumber: Info(9)
        Body: Str(Testing otel logging )
        Attributes:
             -> trace_id: Str(bcc240ae671572d0625810db5a8e0dda)
             -> span_id: Str(fcf926aa13a16bee)
             -> hostname: Str(rhel9-node)
             -> application: Str(rsyslog)
             -> facility: Int(1)
             -> proc_id: Str(877)
             -> version: Int(1)
             -> priority: Int(14)
             -> trace_flags: Str(01)
             -> loki.attribute.labels: Str(service_name, service_namespace, application, hostname, host, level, facility, connection_hostname, trace_id, span_id, trace_flags)
             -> loki.format: Str(raw)
        Trace ID: bcc240ae671572d0625810db5a8e0dda
        Span ID: fcf926aa13a16bee
        Flags: 1
                {"kind": "exporter", "data_type": "logs", "name": "debug"}
        ``` 

* if using the system logger you need to quote and add `#${TRACEPARENT}` to correlate logs to traces

    ```
    logger -p user.info "Testing otel logging#${TRACEPARENT}"
    ```

        ```
        2025-02-13T14:20:00.097Z        info    Logs    {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
        2025-02-13T14:20:00.097Z        info    ResourceLog #0
        Resource SchemaURL:
        ScopeLogs #0
        ScopeLogs SchemaURL:
        InstrumentationScope
        LogRecord #0
        ObservedTimestamp: 2025-02-13 14:19:59.965594056 +0000 UTC
        Timestamp: 2025-02-13 14:19:59.909214 +0000 UTC
        SeverityText: info
        SeverityNumber: Info(9)
        Body: Str(Testing otel logging )
        Attributes:
             -> proc_id: Str(877)
             -> version: Int(1)
             -> hostname: Str(rsyslog)
             -> span_id: Str(fcf926aa13a16bee)
             -> trace_flags: Str(01)
             -> priority: Int(14)
             -> application: Str(rsyslog)
             -> trace_id: Str(bcc240ae671572d0625810db5a8e0dda)
             -> facility: Int(1)
             -> loki.attribute.labels: Str(service_name, service_namespace, application, hostname, host, level, facility, connection_hostname, trace_id, span_id, trace_flags)
             -> loki.format: Str(raw)
        Trace ID: bcc240ae671572d0625810db5a8e0dda
        Span ID: fcf926aa13a16bee
        Flags: 1
                {"kind": "exporter", "data_type": "logs", "name": "debug"}
        ``` 
