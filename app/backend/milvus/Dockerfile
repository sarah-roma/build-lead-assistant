# Milvus standalone image for IBM Code Engine
# Uses the official Milvus base image and runs standalone mode.
FROM milvusdb/milvus:latest

# Runtime environment values passed at deploy time

# Ensure data directories exist
USER root
RUN mkdir -p ${MILVUS_WAL_DIR} ${MILVUS_DATA_DIR} \
    && chown -R milvus:milvus /var/lib/milvus || true

EXPOSE ${MILVUS_PORT} ${MILVUS_HTTP_PORT}

USER milvus

# Start Milvus in standalone mode. Environment variables can be
# supplied by the Code Engine deployment to override defaults.
CMD ["milvus", "run", "standalone"]