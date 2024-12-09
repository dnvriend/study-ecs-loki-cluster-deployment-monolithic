FROM grafana/loki:3.3.1

RUN mkdir -p /loki && \
    mkdir -p /loki/boltdb-shipper-active && \
    mkdir -p /loki/boltdb-shipper-cache && \
    mkdir -p /loki/compactor

COPY ./config/monolith-config.yaml /etc/loki/config.yaml

RUN /usr/bin/loki -verify-config -config.file=/etc/loki/config.yaml -config.expand-env=true

ENTRYPOINT ["/usr/bin/loki", "-config.file=/etc/loki/config.yaml", "-config.expand-env=true"]
