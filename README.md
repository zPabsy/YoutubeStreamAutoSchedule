# YouTube Livestream Automation

This repository contains Python scripts for managing and automating YouTube livestreams using the YouTube Data API in Linux OS. It supports token refresh, stream scheduling, starting/stopping streams, and configuration via JSON files.
What you need :

1. Windows OS for one-time token activation.
2. Linux (Ubuntu preferably) with ffmpeg, python and Google API Library installed.
3. A bit of patience since it's very frustating and confusing.

---

## ⚙️ Setup

**1. Clone the repository:**

```bash
git clone https://github.com/zPabsy/YoutubeStreamAutoSchedule.git
cd YoutubeStreamAutoSchedule
```

---

**2. Get client_secret.json and token.json:**
   
Install the Google API Library
```bash
pip install --upgrade google-auth google-auth-oauthlib google-api-python-client --break-system-packages
```
Full tutorial for getting the token on progress

---

**3. Get StreamID and StreamKey:**
   
Create your StreamKey on your Youtube Studio Livestream section and use the streamid.py to get the streamID, it's different with the StreamKey

![image](https://github.com/user-attachments/assets/bb43cd90-f7de-4b00-a952-65247c7403ed)

---

**4. Configure config.json for Livestream Metadata**
   
Here the format of the config.json for the livestream metadata, you can duplicate the format if you want to have more than 2 streams.

```bash
[
  {
    "title": "YOUR_STREAM_TITLE",
    "video": "YOUR_VIDEO_LOCATION",
    "thumbnail": "YOUR_THUMBNAIL_LOCATION",
    "stream_id": "STREAM_ID", #NOT STREAM KEY
    "hour": 6,
    "minute": 0,
    "tags": ["TAG1","TAG2","TAG3"]
  },
  {
    "title": "YOUR_STREAM_TITLE",
    "video": "YOUR_VIDEO_LOCATION",
    "thumbnail": "YOUR_THUMBNAIL_LOCATION",
    "stream_id": "STREAM_ID", #NOT STREAM KEY
    "hour": 7,
    "minute": 0,
    "tags": ["TAG1","TAG2","TAG3"]
  }
]
```

---

**5. Start the Schedule With schedule.py**
   
You can directly run the schedule.py script or you can use the crontab for the automation, for example we only have 2 index of config in config.json, so in the schedule.py, it start with index number 0. 

```bash
44 16 * * * /usr/bin/python3 /root/live/testing/schedule.py 0
49 16 * * * /usr/bin/python3 /root/live/testing/schedule.py 1
```

---

**6. Refresh Token Daily Using refresh.py**
   
We need to refresh the token.json daily to avoid re-activate. Better to use the crontab to automate refresh token daily.

![image](https://github.com/user-attachments/assets/0a620693-025d-4187-9ca0-35da9dbfd20b)

---

**7. Start and Stop Stream Using Crontab**


You can start the stream and stop the stream based on the streamkey and the PPID of the ffmpeg

---

**8. Automate using crontab**
    
You can combine all the refresh token, start schedule, start stream and stop stream in crontab.

![image](https://github.com/user-attachments/assets/e80b2046-7c38-4112-b9ce-9fd1d80976ed)
