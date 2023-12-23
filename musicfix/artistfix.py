import os
from mutagen.flac import FLAC

def update_flac_tags(file_path):
    audio = FLAC(file_path)
    updated = False
    
    if 'ARTIST' in audio and isinstance(audio['ARTIST'], list) and any('; ' in artist for artist in audio['ARTIST']):
        updated_artists = []
        for artist in audio['ARTIST']:
            updated_artists.extend(artist.split('; '))
        audio['ARTIST'] = updated_artists
        updated = True
    
    if 'ALBUMARTIST' in audio and isinstance(audio['ALBUMARTIST'], list) and any('; ' in artist for artist in audio['ALBUMARTIST']):
        updated_album_artists = []
        for album_artist in audio['ALBUMARTIST']:
            updated_album_artists.extend(album_artist.split('; '))
        audio['ALBUMARTIST'] = updated_album_artists
        updated = True
    
    if updated:
        audio.save()

# Specify the directory containing FLAC files
current_directory = "//?/D:/Music/fl"

# Recursively search for FLAC files
flac_files = []
for root, dirs, files in os.walk(current_directory):
    for file in files:
        if file.lower().endswith(".flac"):
            flac_files.append(os.path.join(root, file))

if not flac_files:
    print("No FLAC files found in the current directory and its subfolders.")
else:
    updated_files = 0
    for flac_file_path in flac_files:
        before_tags = FLAC(flac_file_path).tags
        update_flac_tags(flac_file_path)
        after_tags = FLAC(flac_file_path).tags
        
        if before_tags != after_tags:
            updated_files += 1
    
    if updated_files == 0:
        print("No FLAC files with semicolons in tags were found.")
    else:
        print(f"Updated tags for {updated_files} FLAC files.")
