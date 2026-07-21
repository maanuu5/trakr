import logging
from opentelemetry import metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

def init_otel():
    resource = Resource.create({"service.name": "trakr"})
    
    # -----------------------------
    # Metrics Setup
    # -----------------------------
    metric_exporter = OTLPMetricExporter(
        endpoint="localhost:4317",
        insecure=True,
    )
    metric_reader = PeriodicExportingMetricReader(
        metric_exporter,
        export_interval_millis=5000,
    )
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
    metrics.set_meter_provider(meter_provider)
    meter = metrics.get_meter("trakr")

    # -----------------------------
    # Logs Setup
    # -----------------------------
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    
    log_exporter = OTLPLogExporter(
        endpoint="localhost:4317",
        insecure=True,
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    
    # Connect standard python logging to OpenTelemetry
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    
    # Create our specific logger
    logger = logging.getLogger("trakr")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return meter, logger
