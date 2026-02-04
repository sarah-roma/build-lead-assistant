FROM quay.io/coreos/etcd:v3.5.18
# Use a configurable upstream etcd image so deploys can pick a patched tag.
# Set the build arg `ETCD_IMAGE` to a scanned/patched tag when building/pushing.
# ARG ETCD_IMAGE=quay.io/coreos/etcd:latest
# FROM ${ETCD_IMAGE}

# Runtime settings passed via environment variables at deploy time

VOLUME ["/etcd"]

EXPOSE 2379

# Healthcheck mirrors the docker-compose healthcheck
HEALTHCHECK --interval=30s --timeout=20s --retries=3 \
  CMD ETCDCTL_API=3 etcdctl endpoint health || exit 1

# Start etcd with the same flags used in docker-compose
CMD ["etcd", "-advertise-client-urls=http://127.0.0.1:2379", "-listen-client-urls", "http://0.0.0.0:2379", "--data-dir", "/etcd"]