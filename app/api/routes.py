from fastapi import APIRouter, HTTPException
from app.schemas.submission import SubmissionRequest
from app.core.validators import (
    validate_crop,
    validate_behavior,
    validate_qa,
)
from app.services.s3_service import append_jsonl
from app.services.logging_service import log_submission

import os
import boto3

router = APIRouter()

@router.get("/behaviors")
def get_behaviors():
    return [
        "theoretical",
        "practical",
        "calculation",
        "diagnostic",
        "preventive",
        "safety",
    ]


@router.get("/crops")
def list_crops():
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ.get("AWS_REGION"),
        )

        response = s3.list_objects_v2(
            Bucket=os.environ["S3_BUCKET_NAME"],
            Delimiter="/"
        )

        crops = [
            obj["Prefix"].rstrip("/")
            for obj in response.get("CommonPrefixes", [])
            if obj["Prefix"] != "metadata/"
        ]

        return {"crops": crops}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit")
def submit_data(payload: SubmissionRequest):
    try:
        validate_crop(payload.crop)
        validate_behavior(payload.behavior)

        entries = []
        for qa in payload.qa_pairs:
            validate_qa(qa.question, qa.answer)
            entries.append({
                "user": qa.question,
                "assistant": qa.answer,
            })

        key = f"{payload.crop}/{payload.crop}_{payload.behavior}.jsonl"
        append_jsonl(key, entries)

        log_submission({
            "crop": payload.crop,
            "behavior": payload.behavior,
            "count": len(entries),
            "submitted_by": payload.submitted_by,
        })

        return {"status": "success", "inserted": len(entries)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
