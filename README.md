1. Configure the Social Media File (social_media_sites.json)
This file should be in the same directory as GhostTR.py.
It must be a valid JSON array of objects, each with "url" and "name" keys.
Example: [
  {"url": "https://www.facebook.com/{}", "name": "Facebook"},
  {"url": "https://www.instagram.com/{}", "name": "Instagram"},
  {"url": "https://www.github.com/{}", "name": "GitHub"}
]
You can add, remove, or edit entries as needed.

2. Configure the Log File (GRABBER.log)
By default, logs are written to GRABBER.log in the same directory.
You can change the filename by editing the LOG_FILE variable at the top of grabber.py:

LOG_FILE = "my_custom_log.log"

3.Set Tor as Proxy (USE_TOR=1)

Install Tor on your system and start the Tor service (it must listen on 127.0.0.1:9050).
Set the environment variable USE_TOR=1 before running the script.

Windows Command Prompt:

set USE_TOR=1
python [grabber.py](http://_vscodecontentref_/5)

Windows PowerShell:

$env:USE_TOR=1
python [grabber.py](http://_vscodecontentref_/6)

Linux/macOS Terminal:

export USE_TOR=1
python [grabber.py](http://_vscodecontentref_/7)

