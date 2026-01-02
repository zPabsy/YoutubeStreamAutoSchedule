#!/usr/bin/env python3

import os
import json
import pytz
import datetime
import argparse
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRET_FILE = "/root/live/client_secret.json"
TOKEN_FILE = "/root/live/token.json"
CONFIG_FILE = "/root/live/config.json"

def authenticate():
    if not os.path.exists(TOKEN_FILE):
        raise Exception("âŒ token.json not found.")
    return Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

def get_utc_time(hour, minute):
    jakarta = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(jakarta)
    scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if scheduled < now:
        scheduled += datetime.timedelta(days=1)
    return scheduled.astimezone(pytz.utc).isoformat("T").replace("+00:00", "Z")

def schedule_stream(youtube, stream):
    scheduled_time = get_utc_time(stream["hour"], stream["minute"])

    # Step 1: Create broadcast
    broadcast = youtube.liveBroadcasts().insert(
        part="snippet,contentDetails,status",
        body={
            "snippet": {
                "title": stream["title"],
                "scheduledStartTime": scheduled_time
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            },
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": True
            }
        }
    ).execute()

    video_id = broadcast["id"]

    # Step 2: Bind to stream key
    youtube.liveBroadcasts().bind(
        part="id,contentDetails",
        id=video_id,
        streamId=stream["stream_id"]
    ).execute()

    # Step 3: Upload thumbnail
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(stream["thumbnail"])
        ).execute()
    except googleapiclient.errors.HttpError as e:
        if e.resp.status == 429:
            print("âš ï¸ Thumbnail limit! Skipping~")
        else:
            raise

    # Step 4: Get existing snippet and update with tags/category
    video = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    snippet = video["items"][0]["snippet"]
    snippet["tags"] = stream.get("tags", ["rain", "rain asmr", "rain ambience", "sloela", "tag sched"])
    snippet["categoryId"] = "22"  # People & Blogs

    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": snippet
        }
    ).execute()
    print(f"âœ… Video: {stream['video']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=int, help="Index of stream (0â€“9)")
    args = parser.parse_args()

    with open(CONFIG_FILE, "r") as f:
        streams = json.load(f)

    if args.index < 0 or args.index >= len(streams):
        raise ValueError("âŒ Invalid stream index (must be 0â€“9)")

    creds = authenticate()
    youtube = build("youtube", "v3", credentials=creds)

    schedule_stream(youtube, streams[args.index])

if __name__ == "__main__":
    main()
