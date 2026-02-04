# Milvus standalone image for IBM Code Engine
# Uses the official Milvus base image and runs standalone mode.
FROM milvusdb/milvus:latest

# Ensure data directories exist with hardcoded paths
USER root
RUN mkdir -p /var/lib/milvus/wal /var/lib/milvus/data \
    && chown -R milvus:milvus /var/lib/milvus || true

EXPOSE 19530 19121

USER milvus

# Start Milvus in standalone mode. Environment variables can be
# supplied by the Code Engine deployment to override defaults.
CMD ["milvus", "run", "standalone"]