import json
from datetime import datetime
from app.core.s3_client import get_s3_client
from app.core.config import S3_BUCKET_NAME

s3 = get_s3_client()
LOG_KEY = "metadata/logs/submissions.jsonl"

def log_submission(data: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        **data,
    }

    try:
        obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=LOG_KEY)
        existing = obj["Body"].read().decode("utf-8")
    except s3.exceptions.NoSuchKey:
        existing = ""

    updated = existing + json.dumps(entry, ensure_ascii=False) + "\n"

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=LOG_KEY,
        Body=updated.encode("utf-8"),
    )
