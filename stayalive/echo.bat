@echo off
:loop
ffplay -f lavfi -i "sine=frequency=50400:duration=2" -loglevel quiet -nostats -hide_banner -autoexit -nodisp
timeout /t 277 /nobreak
goto loop
