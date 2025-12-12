import boto3
from datetime import datetime, timedelta, timezone
import os

s3 = boto3.client("s3")
sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
BUCKET = os.environ.get("BUCKET")
PREFIX = os.environ.get("PREFIX", "")

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))


def lambda_handler(event, context):

    # ---- Calculate today's date in IST ----
    now_ist = datetime.now(IST)
    today_ist = datetime(now_ist.year, now_ist.month, now_ist.day, tzinfo=IST)

    # Add both date and time strings
    date_str = today_ist.strftime("%Y-%m-%d")
    time_str = now_ist.strftime("%H:%M:%S")     # use actual time, not midnight time

    # Convert into UTC because S3 uses UTC timestamps
    start_utc = today_ist.astimezone(timezone.utc)
    end_utc = (today_ist + timedelta(days=1)).astimezone(timezone.utc)

    count = 0

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET, Prefix=PREFIX)

    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                ts = obj["LastModified"]  # UTC timestamp
                if start_utc <= ts < end_utc:
                    count += 1

    # Email message
    message = (
        f"Visitors Count (Today)\n\n"
     #   f"Bucket: {BUCKET}\n"
     #   f"Prefix: {PREFIX}\n"
        f"Date (IST): {date_str}\n"
        f"Time (IST): {time_str}\n"
        f"Logs Created in Today's date: {count}\n"
    )

    # Publish email
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"Visitors Count: {count} | {date_str} | {time_str} ",
        Message=message
    )

    return {
        "date": date_str,
        "time": time_str,
        "objects_created_today": count,
        "email_sent": True
    }
