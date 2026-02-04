FROM docker.io/minio/minio:RELEASE.2023-03-20T20-16-18Z

# Default MinIO access credentials (override via Code Engine secrets/envs)
ENV MINIO_ACCESS_KEY=minioadmin
ENV MINIO_SECRET_KEY=minioadmin
ENV MINIO_DATA_DIR=/minio_data

VOLUME ["/minio_data"]

EXPOSE 9000 9001

# Healthcheck mirrors docker-compose
HEALTHCHECK --interval=30s --timeout=20s --retries=3 \
  CMD curl -f http://localhost:9000/minio/health/live || exit 1

# Start MinIO with console on 9001 and data directory as in docker-compose
CMD ["minio", "server", "/minio_data", "--console-address", ":9001"]
