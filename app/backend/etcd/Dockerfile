# FROM quay.io/coreos/etcd:v3.5.18
# Use a configurable upstream etcd image so deploys can pick a patched tag.
# Set the build arg `ETCD_IMAGE` to a scanned/patched tag when building/pushing.
ARG ETCD_IMAGE=quay.io/coreos/etcd:latest
FROM ${ETCD_IMAGE}

# Default etcd runtime settings (override at deploy time)
ENV ETCD_AUTO_COMPACTION_MODE=revision
ENV ETCD_AUTO_COMPACTION_RETENTION=1000
ENV ETCD_QUOTA_BACKEND_BYTES=4294967296
ENV ETCD_SNAPSHOT_COUNT=50000
ENV ETCD_DATA_DIR=/etcd

VOLUME ["/etcd"]

EXPOSE 2379

# Healthcheck mirrors the docker-compose healthcheck
HEALTHCHECK --interval=30s --timeout=20s --retries=3 \
  CMD ETCDCTL_API=3 etcdctl endpoint health || exit 1

# Start etcd with the same flags used in docker-compose
CMD ["etcd", "-advertise-client-urls=http://127.0.0.1:2379", "-listen-client-urls", "http://0.0.0.0:2379", "--data-dir", "/etcd"]
