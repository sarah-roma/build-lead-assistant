`podman build . -t test-1-backend   `
`podman run -p 8001:8001 test-1-backend`

- getting more memory on podman
- using python:3.11-slim
- package changes

```
    File "/backend/utils/milvus_setup.py", line 60, in connect_to_milvus
    raise Exception(f"Failed to connect to Milvus server: {e}")
    Exception: Failed to connect to Milvus server: <MilvusException: (code=2, message=Fail connecting to server on 127.0.0.1:19530, illegal connection params or server unavailable)>
```