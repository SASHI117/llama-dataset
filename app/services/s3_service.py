import json
from app.core.s3_client import get_s3_client
from app.core.config import S3_BUCKET_NAME

s3 = get_s3_client()

def append_jsonl(key: str, entries: list[dict]):
    try:
        obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=key)
        existing = obj["Body"].read().decode("utf-8")
    except s3.exceptions.NoSuchKey:
        existing = ""

    new_lines = ""
    for entry in entries:
        new_lines += json.dumps(entry, ensure_ascii=False) + "\n"

    updated = existing + new_lines

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=updated.encode("utf-8"),
    )
