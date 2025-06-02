<div align="center">
 <img src="https://github.com/MrEchoFi/MrEchoFi/raw/4274f537dec313ac7dde4403fe0fae24259beade/Mr.EchoFi-New-Logo-with-ASCII.jpg" alt="logo" width="200" height="auto" />
  <h1>~ GRABBER ~</h1>
   
  <p>
  An IP Tracer, Username Tracer based tool.
  </p>


  📫 How to reach me **tanjibisham777@gmail.com & tanjibisham888@gmail.com**

# Video for better understanding :
  


https://github.com/user-attachments/assets/8c208975-32b5-4d1a-ab94-a5236de1c091


   
</div>


# Usage:

         #######USAGE######
         grabber.py [-h] [--ip IP] [--username USERNAME] [--showip] [--export EXPORT] [--format {json,csv}] [--no-banner]

         // GRABBER: Forensic IP & Username Tracer (Red Team Edition)

         options:
            -h, --help           show this help message and exit
            --ip IP              Track information for an IP address
            --username USERNAME  Track username across social media
            --showip             Show your public IP
            --export EXPORT      Export results to file (json/csv)
            --format {json,csv}  Export format
            --no-banner          Do not show banner/disclaimer
            
Other usage: 

1. Configure the Social Media File (social_media_sites.json)
   This file should be in the same directory as GhostTR.py.
   It must be a valid JSON array of objects, each with "url" and "name" keys.

Example:
 [
  {"url": "https://www.facebook.com/{}", "name": "Facebook"},
  {"url": "https://www.instagram.com/{}", "name": "Instagram"},
  {"url": "https://www.github.com/{}", "name": "GitHub"}
]
   You can add, remove, or edit entries as needed.

3. Configure the Log File (GRABBER.log)
   
      By default, logs are written to GRABBER.log in the same directory.
      You can change the filename by editing the LOG_FILE variable at the top of grabber.py:

      LOG_FILE = "my_custom_log.log"

4.Set Tor as Proxy (USE_TOR=1)

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


Happy HackNight !!!
