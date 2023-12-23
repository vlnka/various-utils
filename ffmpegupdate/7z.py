import requests, os, subprocess, shutil, time, glob

version_url, file_url = "https://www.gyan.dev/ffmpeg/builds/git-version", "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
new_version = requests.get(version_url).text.strip()
current_version = open("ver.txt", "r").read().strip() if os.path.exists("ver.txt") else ""

if new_version != current_version:
    open("ver.txt", "w").write(new_version)
    filename = f"ffmpeg-git-full-{new_version}.7z"
    open(filename, "wb").write(requests.get(file_url).content)
    subprocess.run(["7z", "x", filename])
    top_folder = next(name for name in os.listdir('.') if name.startswith('ffmpeg') and name.endswith('full_build'))
    for file in ['ffplay.exe', 'ffprobe.exe', 'ffmpeg.exe']:
        shutil.move(os.path.join(top_folder, 'bin', file), f'D:/Path/{file}')
    shutil.rmtree(top_folder)

for f in glob.glob("*.7z"):
    if (time.time() - os.path.getctime(f)) // (24 * 3600) >= 14:
        os.unlink(f)
