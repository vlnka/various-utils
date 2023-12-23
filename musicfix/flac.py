import os
import subprocess
import shutil
import pathlib
import re
import glob
from mutagen.flac import FLAC
from collections import Counter
from PIL import Image
import io

directory = '//?/D:/Music'
pre_directory = directory + '/pre'

def artistfix(tag):
    replacements = {
        " feat.":";",
        " featuring":";",
        " ft.":";",
        " &":";",
        ",":";",
        "La4":"LA4",
        "JAY‐Z":"Jay‐Z",
        "Sophie Meiers":"sophie meiers",
        "Charli Xcx":"Charli XCX",
        "Easy Life":"easy life",
        "Raye":"RAYE",
        "Fletcher":"FLETCHER",
        "HYD":"Hyd",
        "Enny":"ENNY",
        "Bia":"BIA",
        "-":"‐",
        "Baynk":"BAYNK",
	"IceColdBishop":"ICECOLDBISHOP",
	"Elucid":"E L U C I D",
	"Devon Hendryx":"JPEGMAFIA"
    }
    for key in replacements:
        tag = tag.replace(key, replacements[key])
    return tag

def numfix(num):
    return num.split('/',1)[0].zfill(2)

def sanitize(filename):
    dash = re.sub(r'[\\/:*?"<>|]', '-', filename)
    return re.sub(r'/^[.\s]+|[.\s]+$/g', '', dash)

def cutyear(yeartag):
	if len(yeartag) > 14:
		return yeartag[:-14]
	else:
		return yeartag

def separt(file_path):
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

def getext(data):
    if data.startswith(b"\xFF\xD8\xFF"):
        return "jpg"
    elif data.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
        return "png"
    elif data.startswith(b"\x47\x49\x46\x38\x39\x61") or data.startswith(b"\x47\x49\x46\x38\x37\x61"):
        return "gif"
    elif data.startswith(b"\x42\x4D"):
        return "bmp"
    elif data.startswith(b"\x49\x49\x2A\x00") or data.startswith(b"\x4D\x4D\x00\x2A"):
        return "tiff"
    elif data.startswith(b"\x00\x00\x01\x00") or data.startswith(b"\x00\x00\x02\x00"):
        return "ico"
    elif data.startswith(b"\x66\x74\x79\x70\x4D\x53\x4E"):
        return "avif"
    elif data.startswith(b"\x00\x00\x00\x0C\x4A\x58\x4C\x20"):
        return "jxl"
    elif data.startswith(b"\x52\x49\x46\x46....\x57\x45\x42\x50"):
        return "webp"
    else:
        return None

for file in glob.glob(os.path.join(directory + '/pre/', '**/*.flac'), recursive=True):
    f = FLAC(file)

    album = f.tags['album']
    albumartist = f.tags['albumartist']
    artist = f.tags['artist']
    discnumber = f.tags['discnumber']
    genre = f.tags['genre']
    title = f.tags['title']
    tracknumber = f.tags['tracknumber']
    date = f.tags['date']

    albumartist[0] = artistfix(albumartist[0])
    artist[0] = artistfix(artist[0])
    discnumber[0] = numfix(discnumber[0])
    tracknumber[0] = numfix(tracknumber[0])


    for index, pic in enumerate(f.pictures):
        if index == 0:
            picpath = os.path.dirname(file) +"/folder." + getext(pic.data)
        else:
            picpath = os.path.dirname(file) +"/folder(" + str(index) + ")." + getext(pic.data)
        if not os.path.exists(picpath):
            with open(picpath, "wb") as pictw:
                pictw.write(f.pictures[index].data)

    outfolder = directory + '/fl/' + sanitize(albumartist[0]).rstrip('.').rstrip('?').rstrip('*') + '/' + sanitize(cutyear(date[0])) + ' - ' + sanitize(album[0]).rstrip('.').rstrip('?').rstrip('*') + '/'
    pathlib.Path(outfolder).mkdir(parents=True, exist_ok=True)
    out = (outfolder + sanitize(discnumber[0]) + '-' + sanitize(tracknumber[0]) + '. ' + sanitize(artist[0]) + ' - ' +  sanitize(title[0])).rstrip('.').rstrip('?').rstrip('*') + '.flac'
    subprocess.check_call(['C:\Program Files\CUETools_2.2.4\CUETools.FLACCL.cmd.exe','-11','--lax','--cpu-threads','16','-o',out,file])

    f1 = FLAC(out)
    f1.tags['album'] = album[0]
    f1.tags['albumartist'] = albumartist[0]
    f1.tags['artist'] = artist[0]
    f1.tags['discnumber'] = discnumber[0]
    f1.tags['genre'] = genre[0]
    f1.tags['title'] = title[0]
    f1.tags['tracknumber'] = tracknumber[0]
    f1.tags['date'] = cutyear(date[0])
    f1.save()
    separt(out)

    os.remove(file)

    imgext = ["jpg", "png", "gif", "bmp", "tiff", "ico", "avif", "jxl", "webp"]
    images = []
    for ext in imgext:
        images.extend(glob.glob(os.path.join(os.path.dirname(file), f'**/*.{ext}'), recursive=True))
    for img in images:
        imgout = directory + '/fl/' + sanitize(albumartist[0]) + '/' + sanitize(cutyear(date[0])) + ' - ' + sanitize(album[0]) + '/' + os.path.basename(img)
        if not os.path.isfile(imgout):
            shutil.copy(img.replace('\\', '/'), imgout)

