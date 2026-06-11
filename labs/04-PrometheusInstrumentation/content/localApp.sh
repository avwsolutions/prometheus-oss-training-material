#!/bin/bash

# Output file for Node Exporter Textfile Collector
OUTPUT_FILE="/var/lib/node_exporter/textfile_collector/localApp.prom"

# Example values (replace with your application's values)
PROCESSING_TIME=125
PROCESSING_CODE=200
CUSTOMER="foobar"

# Create metrics atomically
TMP_FILE=$(mktemp)

cat > "$TMP_FILE" << EOF
# HELP crm_processing_time_milliseconds Processing time in milliseconds
# TYPE crm_processing_time_milliseconds gauge
crm_processing_time_milliseconds{role="processing-host",customer="${CUSTOMER}"} ${PROCESSING_TIME}

# HELP crm_processing_status_code Processing status code
# TYPE crm_processing_status_code gauge
crm_processing_status_code{role="processing-host",customer="${CUSTOMER}"} ${PROCESSING_CODE}

# HELP crm_processing_customer_info Customer information metric
# TYPE crm_processing_customer_info gauge
crm_processing_customer_info{role="processing-host",customer="${CUSTOMER}"} 1
EOF

mv "$TMP_FILE" "$OUTPUT_FILE"