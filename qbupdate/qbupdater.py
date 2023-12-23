import feedparser
import requests
import os
import re
import subprocess
import datetime
import shutil

feed_url = "https://sourceforge.net/p/qbittorrent/activity/feed"
keyword = "lt20_qt6_x64_setup.exe"
qb_directory = "D:\\Programs\\qBittorrent"
dl_directory = "D:\\Scripts\\qbupdate"

# Parse the RSS feed
feed = feedparser.parse(feed_url)

# Find the latest item with the specified keyword in the title
latest_item = None
for item in feed.entries:
    if item.title.endswith(keyword):
        if latest_item is None or item.published_parsed > latest_item.published_parsed:
            latest_item = item

latest_link = "https://kumisystems.dl.sourceforge.net/project/qbittorrent/qbittorrent-win32/" + '/'.join(latest_item.guid.split('/')[-3:-1])
archive_name = latest_item.guid.split('/')[-2]
archive_path = dl_directory + "\\" + archive_name
print(latest_link)

def download_file(url, target_directory):
    response = requests.get(url)
    if response.status_code == 200:

        # Create the full path for the target file
        target_path = os.path.join(target_directory, archive_name)

        # Check if the target directory exists, create if not
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Write the content to the file
        with open(target_path, "wb") as f:
            f.write(response.content)
        
        print(f"File downloaded to: {target_path}")
    else:
        print("Failed to download the file.")
        
def extract_7z_with_overwrite(archive_path):
    subprocess.run(['7z', 'x', '-o' + qb_directory, '-aoa', archive_name])
        
def scan_and_launch(target_directory, url):
    if not os.path.exists(os.path.join(dl_directory, archive_name)):
        download_file(latest_link, dl_directory)
        print('dl')
        extract_7z_with_overwrite(archive_path)

scan_and_launch(dl_directory, latest_link)

def remove_old_7z_files():
    now = datetime.datetime.now()
    for filename in os.listdir(dl_directory):
        if filename.endswith("setup.exe"):
            file_path = os.path.join(dl_directory, filename)
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            age = now - modification_time
            if age.days > 30:
                os.unlink(file_path)  # Use os.unlink to remove the file
                print(f"Removed: {filename}")
                
remove_old_7z_files()

delfolder = qb_directory + "\\$PLUGINSDIR"
if os.path.exists(delfolder) and os.path.isdir(delfolder):
    try:
        shutil.rmtree(delfolder)
    except OSError:
        pass

trackers_url = "https://cf.trackerslist.com/all.txt"
response = requests.get(trackers_url)
if response.status_code == 200:
    additional_trackers = response.text.replace('\n', '\\n')
else:
    print(f"Failed to fetch the trackers txt. Status code: {response.status_code}")

ini_file_path = r'D:\Programs\qBittorrent\profile\qBittorrent\config\qBittorrent.ini'
with open(ini_file_path, 'r') as file:
    lines = file.readlines()
for i, line in enumerate(lines):
    if line.startswith("Session\AdditionalTrackers="):
        lines[i] = "Session\AdditionalTrackers=" + additional_trackers
with open(ini_file_path, 'w') as file:
    file.writelines(lines)