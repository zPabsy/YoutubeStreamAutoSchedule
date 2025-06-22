from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Load your saved credentials from token.json (after OAuth)
def authenticate():
    creds = Credentials.from_authorized_user_file('token.json', [
        'https://www.googleapis.com/auth/youtube.force-ssl'
    ])
    return creds

def list_live_streams(youtube):
    request = youtube.liveStreams().list(
        part="id,snippet",
        mine=True,
        maxResults=10
    )
    response = request.execute()

    print("Your live streams:")
    for stream in response.get("items", []):
        stream_id = stream['id']
        title = stream['snippet']['title']
        print(f"Stream ID: {stream_id}  | Title: {title}")

if __name__ == "__main__":
    creds = authenticate()
    youtube = build("youtube", "v3", credentials=creds)
    list_live_streams(youtube)
