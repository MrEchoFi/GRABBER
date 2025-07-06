# GRABBER: Forensic IP & Username Tracer
# Author: Mr.EchoFi
# Version: 1.0 (Red Team Edition)

import json
import requests
import time
import os
import sys
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from phonenumbers import carrier, geocoder, timezone
from sys import stderr


SOCIAL_MEDIA_FILE = "social_media_sites.json"
LOG_FILE = "GRABBER.log"
MAX_THREADS = 20


Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)


DISCLAIMER = f"""{Re}
[!] WARNING: This tool is for authorized forensic and red team use only.
Unauthorized use against systems or accounts you do not own or have explicit permission to test is illegal.
The author is not responsible for misuse or damage.
{Wh}
"""



def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def validate_ip(ip):
    import re
   
    ipv4 = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    ipv6 = r"^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}$"
    return re.match(ipv4, ip) or re.match(ipv6, ip)

def validate_username(username):
    return username and username.isalnum() and 2 <= len(username) <= 32

def load_social_media_sites():
   
    default_sites = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
         {"url": "https://www.google.com/{}", "name": "Google"},
         {"url": "https://mail.google.com/{}", "name": "Mail"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/{}", "name": "Youtube"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
        {"url": "https://www.ello.co/{}", "name": "Ello"},
        {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        {"url": "https://www.weheartit.com/{}", "name": "We Heart It"},
        {"url": "https://www.bybit.com/{}", "name": "Bybit"},
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit"},
        {"url": "https://www.deviantart.com/{}", "name": "DeviantArt"},
        {"url": "https://www.vk.com/{}", "name": "VK"},
        {"url": "https://www.ok.ru/{}", "name": "Odnoklassniki"},
        {"url": "https://www.goodreads.com/{}", "name": "Goodreads"},
        {"url": "https://www.patreon.com/{}", "name": "Patreon"},
        {"url": "https://www.badoo.com/en/{}", "name": "Badoo"},
        {"url": "https://www.mixcloud.com/{}", "name": "Mixcloud"},
        {"url": "https://www.discogs.com/user/{}", "name": "Discogs"},
        {"url": "https://www.last.fm/user/{}", "name": "Last.fm"},
        {"url": "https://www.strava.com/athletes/{}", "name": "Strava"},
        {"url": "https://www.roblox.com/users/{}/profile", "name": "Roblox"},
        {"url": "https://www.wattpad.com/user/{}", "name": "Wattpad"},
        {"url": "https://www.couchsurfing.com/people/{}", "name": "Couchsurfing"},
        {"url": "https://www.tripit.com/people/{}", "name": "TripIt"},
        {"url": "https://www.foursquare.com/{}", "name": "Foursquare"},
        {"url": "https://www.about.me/{}", "name": "About.me"},
        {"url": "https://www.blip.fm/{}", "name": "Blip.fm"},
        {"url": "https://www.coderwall.com/{}", "name": "Coderwall"},
        {"url": "https://www.kongregate.com/accounts/{}", "name": "Kongregate"},
        {"url": "https://www.hackerone.com/{}", "name": "HackerOne"},
        {"url": "https://www.keybase.io/{}", "name": "Keybase"},
        {"url": 'https://pastebin.com/u/{}', 'name': 'Pastebin'},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/{}", "name": "Youtube"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
        {"url": "https://www.ello.co/{}", "name": "Ello"},
        {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        {"url": "https://www.weheartit.com/{}", "name": "We Heart It"},
       
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit"},
        {"url": "https://www.deviantart.com/{}", "name": "DeviantArt"},
        {"url": "https://www.vk.com/{}", "name": "VK"},
        {"url": "https://www.ok.ru/{}", "name": "Odnoklassniki"},
        {"url": "https://www.goodreads.com/{}", "name": "Goodreads"},
        {"url": "https://www.patreon.com/{}", "name": "Patreon"},
        {"url": "https://www.badoo.com/en/{}", "name": "Badoo"},
        {"url": "https://www.mixcloud.com/{}", "name": "Mixcloud"},
        {"url": "https://www.discogs.com/user/{}", "name": "Discogs"},
        {"url": "https://www.last.fm/user/{}", "name": "Last.fm"},
        {"url": "https://www.strava.com/athletes/{}", "name": "Strava"},
        {"url": "https://www.roblox.com/users/{}/profile", "name": "Roblox"},
        {"url": "https://www.wattpad.com/user/{}", "name": "Wattpad"},
        {"url": "https://www.couchsurfing.com/people/{}", "name": "Couchsurfing"},
        {"url": "https://www.tripit.com/people/{}", "name": "TripIt"},
        {"url": "https://www.foursquare.com/{}", "name": "Foursquare"},
        {"url": "https://www.about.me/{}", "name": "About.me"},
        {"url": "https://www.blip.fm/{}", "name": "Blip.fm"},
        {"url": "https://www.coderwall.com/{}", "name": "Coderwall"},
        {"url": "https://www.kongregate.com/accounts/{}", "name": "Kongregate"},
        {"url": "https://www.hackerone.com/{}", "name": "HackerOne"},
        {"url": "https://www.keybase.io/{}", "name": "Keybase"},
        {"url": "https://www.pastebin.com/u/{}", "name": "Pastebin"},
        {"url": "https://www.reverbnation.com/{}", "name": "ReverbNation"},
        {"url": "https://www.slideshare.net/{}", "name": "SlideShare"},
        {"url": "https://www.scribd.com/{}", "name": "Scribd"},
        {"url": "https://www.trello.com/{}", "name": "Trello"},
        {"url": "https://www.upwork.com/freelancers/~{}", "name": "Upwork"},
        {"url": "https://www.freelancer.com/u/{}", "name": "Freelancer"},
        {"url": "https://www.fiverr.com/{}", "name": "Fiverr"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
    ]
    if os.path.exists(SOCIAL_MEDIA_FILE):
        try:
            with open(SOCIAL_MEDIA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load {SOCIAL_MEDIA_FILE}: {e}")
    return default_sites

def export_results(data, filename, fmt="json"):
    try:
        if fmt == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        elif fmt == "csv":
            import csv
            with open(filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Field", "Value"])
                for k, v in data.items():
                    writer.writerow([k, v])
        logging.info(f"Results exported to {filename}")
    except Exception as e:
        logging.error(f"Export failed: {e}")

def use_proxy():
   
    if os.environ.get("USE_TOR", "0") == "1":
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }
        return proxies
    return None

def print_banner():
    clear()
    print(f"""{Cy}
  ______  ______ _______ ______  ______  _______  ______
 |  ____ |_____/ |_____| |_____] |_____] |______ |_____/
 |_____| |    \_ |     | |_____] |_____] |______ |    \_
                                                        
                          {Ye}BY: Mr.EchoFi {Blu}Version 1.0
                          {Cy}Copyright 2025_Mr.EchoFi_Tanjib{Cy}
    """)
    print(DISCLAIMER)



def iptrack(ip, export=None, fmt="json"):
    print_banner()
    if not validate_ip(ip):
        print(f"{Re}Invalid IP address Format.{Wh}")
        return
    proxies = use_proxy()
    try:
        resp = requests.get(f"http://ipwho.is/{ip}", proxies=proxies, timeout=10)
        ip_data = resp.json()
        if not ip_data.get("success", True):
            print(f"{Re}IP lookup failed: {ip_data.get('message', 'Unknown error')}{Wh}")
            logging.error(f"IP lookup failed for {ip}: {ip_data}")
            return
        print(f' {Cy}------------- {Blu} INFORMATION OF IP ADDRESS {Cy}-------------')
        for field in [
            ("IP target", ip),
            ("Type IP", ip_data.get("type")),
            ("Country", ip_data.get("country")),
            ("Country Code", ip_data.get("country_code")),
            ("City", ip_data.get("city")),
            ("Continent", ip_data.get("continent")),
            ("Continent Code", ip_data.get("continent_code")),
            ("Region", ip_data.get("region")),
            ("Region Code", ip_data.get("region_code")),
            ("Latitude", ip_data.get("latitude")),
            ("Longitude", ip_data.get("longitude")),
            ("Maps", f"https://www.google.com/maps/@{ip_data.get('latitude')},{ip_data.get('longitude')},8z"),
            ("EU", ip_data.get("is_eu")),
            ("Postal", ip_data.get("postal")),
            ("Calling Code", ip_data.get("calling_code")),
            ("Capital", ip_data.get("capital")),
            ("Borders", ip_data.get("borders")),
            ("Country Flag", ip_data.get("flag", {}).get("emoji")),
            ("Country Flag PNG", ip_data.get("flag", {}).get("img")),
            ("Currency", ip_data.get("currency", {}).get("name")),
            ("Currency Code", ip_data.get("currency", {}).get("code")),
            ("Currency Symbol", ip_data.get("currency", {}).get("symbol")),
            ("ASN", ip_data.get("connection", {}).get("asn")),
            ("ORG", ip_data.get("connection", {}).get("org")),
            ("ISP", ip_data.get("connection", {}).get("isp")),
            ("Domain", ip_data.get("connection", {}).get("domain")),
            ("Timezone ID", ip_data.get("timezone", {}).get("id")),
            ("Timezone ABBR", ip_data.get("timezone", {}).get("abbr")),
            ("DST", ip_data.get("timezone", {}).get("is_dst")),
            ("Offset", ip_data.get("timezone", {}).get("offset")),
            ("UTC", ip_data.get("timezone", {}).get("utc")),
            ("Current Time", ip_data.get("timezone", {}).get("current_time")),
            ("Languages", ip_data.get("languages")),
            ("Region Native", ip_data.get("region_native")),
            ("Country Native", ip_data.get("country_native")),
            ("Country Emoji Unicode", ip_data.get("flag", {}).get("unicode")),
            ("Threat Level", ip_data.get("security", {}).get("threat_level")),
            ("Threat Types", ip_data.get("security", {}).get("threat_types")),
            ("Is Proxy", ip_data.get("security", {}).get("is_proxy")),
            ("Is VPN", ip_data.get("security", {}).get("is_vpn")),
            ("Is Tor", ip_data.get("security", {}).get("is_tor")),
            ("Is Hosting", ip_data.get("security", {}).get("is_hosting")),
        ]:
            print(f"{Blu}{field[0]:<22}:{Cy} {field[1]}")
        logging.info(f"IP tracked: {ip}")
        if export:
            export_results(ip_data, export, fmt)
    except Exception as e:
        print(f"{Re}Error: {e}{Wh}")
        logging.error(f"IP tracking error: {e}")

def showip(export=None, fmt="json"):
    print_banner()
    proxies = use_proxy()
    try:
        resp = requests.get('https://api.ipify.org/', proxies=proxies, timeout=10)
        show_ip = resp.text
        print(f"\n {Cy}<<<<<<< {Cy}YOUR IP INFORMATION {Cy}>>>>>>>")
        print(f"\n {Cy}[{Blu} ~ {Cy}] Your IP Address : {Blu}{show_ip}")
        print(f"\n {Ye}********************************************")
        logging.info(f"Your IP: {show_ip}")
        if export:
            export_results({"ip": show_ip}, export, fmt)
    except Exception as e:
        print(f"{Re}Error: {e}{Wh}")
        logging.error(f"Show IP error: {e}")

def check_username_site(site, username, proxies=None):
    url = site['url'].format(username)
    try:
        resp = requests.get(url, proxies=proxies, timeout=8)
        if resp.status_code == 200:
            return (site['name'], url)
        else:
            return (site['name'], None)
    except Exception:
        return (site['name'], None)

def trackU(username, export=None, fmt="json"):
    print_banner()
    if not validate_username(username):
        print(f"{Re}Invalid username format. Use 2-32 alphanumeric characters.{Wh}")
        return
    proxies = use_proxy()
    sites = load_social_media_sites()
    results = {}
    print(f"\n {Cy}<<<< {Blu}SHOW INFORMATION USERNAME {Cy}>>>>\n")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_site = {executor.submit(check_username_site, site, username, proxies): site for site in sites}
        for future in as_completed(future_to_site):
            site = future_to_site[future]
            name, url = future.result()
            if url:
                print(f" {Blu}[ {Cy}~ {Blu}] {name} : {Gr}{url}")
                results[name] = url
            else:
                print(f" {Blu}[ {Cy}~ {Blu}] {name} : {Re}Username not found!")
                results[name] = None
    logging.info(f"Username tracked: {username}")
    if export:
        export_results(results, export, fmt)



def main_menu():
    while True:
        print_banner()
        print(f"{Cy}1/~ {Blu}IP GRABBER")
        print(f"{Cy}2/~ {Blu}Show Your IP")
        print(f"{Cy}3/~ {Blu}Username GRABBER")
        print(f"{Cy}0|- {Blu}Exit")
        try:
            opt = input(f"{Cy}\n<> {Blu}Select Option--> {Wh}")
            if opt == "1":
                ip = input(f"{Blu}\n Enter Target IP : {Cy}")
                iptrack(ip)
            elif opt == "2":
                showip()
            elif opt == "3":
                username = input(f"\n {Ye}Enter Username : {Blu}")
                trackU(username)
            elif opt == "0":
                print(f"{Gr}Goodbye! & Happy HackNight!!{Wh}")
                break
            else:
                print(f"{Re}Invalid Option!{Wh}")
            input(f'\n{Cy}[ {Cy}~ {Cy}] {Ye}Back To Menu {Cy}Press Enter')
        except KeyboardInterrupt:
            print(f'\n{Cy}[ {Re}! {Cy}] {Re}EXIT')
            break

def parse_args():
    parser = argparse.ArgumentParser(
        description="GRABBER: Forensic IP & Username Tracer (Red Team Edition)"
    )
    parser.add_argument("--ip", help="Track information for an IP address")
    parser.add_argument("--username", help="Track username across social media")
    parser.add_argument("--showip", action="store_true", help="Show your public IP")
    parser.add_argument("--export", help="Export results to file (json/csv)")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format")
    parser.add_argument("--no-banner", action="store_true", help="Do not show banner/disclaimer")
    return parser.parse_args()

def main():
    args = parse_args()
    if not args.no_banner:
        print_banner()
    if args.ip:
        iptrack(args.ip, args.export, args.format)
    elif args.username:
        trackU(args.username, args.export, args.format)
    elif args.showip:
        showip(args.export, args.format)
    else:
        main_menu()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Cy}[ {Re}! {Cy}] {Re}EXIT')
        time.sleep(1)
        sys.exit(0)
