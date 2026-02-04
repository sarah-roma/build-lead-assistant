# etcd image guidance

This service uses an upstream etcd image. Scanners often report OS/package CVEs for pinned images. Recommended actions:

- Prefer a patched upstream tag. Build/push using the build arg to override the image:

```bash
docker build --build-arg ETCD_IMAGE=quay.io/coreos/etcd:<patched-tag> -t <registry>/etcd:<patched-tag> -f app/backend/etcd/Dockerfile .
docker push <registry>/etcd:<patched-tag>
```

- Scan images locally before pushing (example with Trivy):

```bash
trivy image quay.io/coreos/etcd:v3.5.18
trivy image quay.io/coreos/etcd:latest
```

- If you need zero/near-zero distro CVEs, consider building a minimal image (multi-stage) that copies only the `etcd` and `etcdctl` binaries into a distroless/scratch image. That reduces the attack surface but requires a build step and CI to produce images.

Quick mitigation summary:
- Try `quay.io/coreos/etcd:latest` or a later 3.5.x patch release.
- Scan (Trivy/docker scan) and pick the smallest-C/H image.
- For strict policies, implement a multi-stage build that produces a minimal runtime image.
