import requests, os, time, glob
import urllib.request

txt = open('latest.txt', 'r')
txtlatest = txt.read()
readme = requests.get("https://raw.githubusercontent.com/RobRich999/Chromium_Clang/master/README.md")
open("gitreadme","wb").write(readme.content)
with open("gitreadme","rt") as readmefile:
	data = readmefile.readlines()
for line in data:
	if "-win64-avx2" in line:
		latestvern = line.replace("/tag/", "/download/") + "/mini_installer.exe"
		latestver = latestvern.replace('\r', '').replace('\n', '')

if latestver != txtlatest:
    #installer = requests.get(latestver)
    filename = latestver.replace("https://github.com/RobRich999/Chromium_Clang/releases/download/", "")[:22] + ".exe"
    #open(filename, "wb").write(installer.content)
    urllib.request.urlretrieve(latestver, filename)
    os.system(filename)
    txt.close()
    txtw = open('latest.txt', 'w')
    txtw.write(latestver)
    txtw.close()

current_time = time.time()
for f in glob.glob("*.exe"):
    creation_time = os.path.getctime(f)
    if (current_time - creation_time) // (24 * 3600) >= 7:
        os.unlink(f)

