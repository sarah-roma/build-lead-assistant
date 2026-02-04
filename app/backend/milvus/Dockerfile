# Milvus standalone image for IBM Code Engine
# Uses the official Milvus base image and runs standalone mode.
FROM milvusdb/milvus:latest

# Default environment values (override at deploy time)
ENV MILVUS_TOKEN="root:Milvus"
ENV MILVUS_PORT=19530
ENV MILVUS_HTTP_PORT=19121
ENV MILVUS_WAL_DIR=/var/lib/milvus/wal
ENV MILVUS_DATA_DIR=/var/lib/milvus/data

# Ensure data directories exist
USER root
RUN mkdir -p ${MILVUS_WAL_DIR} ${MILVUS_DATA_DIR} \
    && chown -R milvus:milvus /var/lib/milvus || true

EXPOSE ${MILVUS_PORT} ${MILVUS_HTTP_PORT}

USER milvus

# Start Milvus in standalone mode. Environment variables can be
# supplied by the Code Engine deployment to override defaults.
CMD ["milvus", "run", "standalone"]
