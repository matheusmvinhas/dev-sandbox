FROM minio/mc:latest

COPY minIo/minio-init/buckets.txt /buckets.txt
COPY minIo/minio-init/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]