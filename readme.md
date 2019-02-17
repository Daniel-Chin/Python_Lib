# This repo is...
All the wheels I re-invented. 

# Wait, what?
This repo has various useful python tools and utils. 

I kinda documented them. 

If you have questions or suggestions, please send an email to daniel_chin@yahoo.com  
or open an issue.  
(My repo doesn't have an issue yet... I figure it would be cool to have one...)

The following folders are not python utils, but some demos dependant on the other utils. 
Mostly games. 

Color_Tiles/  
To the Earth/  
Find Vera/  
Beer on the Wall/  

# Documentation
## Archive/
Meaningless Archive of random Python Scripts I wrote.

## ascii_table.py
A beautiful script to print the ascii table. 

## babble.py
Repeatedly prints 'wobo wabble' indefinitely. 

## Beer on the Wall/
Bamboozling lyric-rolling music-playing windows-only python script

## book.py
A file system. 

## cache_no_hash.py
Inefficiently cache and lookup function returns. 

### clicker/__main__.py
Windows only.   
Use your phone to send UP and DOWN to your computer!   
Useful for reading in Kindle.   
  
WARNING: Running this may open vulnerabilities for your computer.   
Don't run this if you don't know what you are doing.   
Only run this if you are in a safe network, or inside a firewall.   
I am not responsible if someone attacks your computer through this server. 

## Color_Tiles/
A game

## compile_readme.py
Iterate through all files in this repo  
build a readme.md for Github. 

## console/
A lighter IPython that launches very quickly. Supports runtime embed.

### console/kernal.py
For a clean namespace.

### console/__init__.py
Windows only. If not windows, console() calls IPython.embed().   
Advantages over IPython:   
    1. Lighter  
    2. Other threads can still print things when user is inputting commands  
    3. Tab auto-completes your phrase, even under Windows! (I'm proud.)   
Issues:   
    1. If you wanna scroll up, you need to input().  
    2. Reassigning module global variables will not be visible to module native codes. Sorry.   
    3. No multi-line code continuation yet

## count.py
For counting votes and ranking the counts. 

## dict_shape.py
Compare the shape of two dicts.   
i.e. is the structure the same? are the keys the same? 

## echo.py
print(sys.argv)

### Find Vera/Find_Vera V2.py
A game by Daniel

## forcemap.py
Like dummy.Pool.map, but no limit of number of threads.   
Useful when IO-bound. 

## formula.py
Evaluate beautiful formulas like ???(2??3??4)  
(Those non-ascii math symbols)

## friendly_time.py
Formatting time data in a friendly manner. 

## graphic_terminal.py
Tools to do graphics in the terminal.

## hub.py
Hub: forward all socket messages.   
Connect, sendall(b'OK'), forward...

### interactive/console_explorer.py
An android-friendly console file explorer. 

### interactive/__init__.py
Terminal interactivity utils.   
  
One vulnerability in `listen`. Do help(listen) for details. 

## ipynb_to_py.py
Converts ipynb to py.   
Works even when Jupyter is not installed. 

## jdt.py
Progress bar. 

## lab.py
This is for me only.   
You won't get why this code is here.   
Give up. 

## local_ip.py
Find out local IP addr on Windows

### macro/__main__.py
Record, play, save, and load macros.   
Windows only.  
PROTECTION: global hooked button to stop macro = Windows Key 

## md2html/
Author = Aumit Leon  
Converts markdown to html.  
I changed __init__.py and renamed commandline.py to __main__.py

## moretk.py
More tkinter gadgets

## my.py
My misc little tools. 

## myfile.py
Unreliable file utils

## myhttp.py
Serves through a (super) simplified version of http protocol.   
Warning: Running this may expose your computer to attacks.   
Don't run this. 

## mymath.py
More math utils than just `import math`

## mythread.py
My threading utils

## myxml.py
XML parser

## Notes.txt
My personal notebook for learning Python. 

## nothing.py


## oneship.py
?????????  
Transmit files over the internet / LAN  
No encryption! Consider everything you transmit broadcast to the entire network. 

## os_stimulate.py
My laptop is weird. Running this script makes opening and terminating processes faster.   
Speculation: Taking CPU time away from Windows Defender? 

## pdf_unspread.py
Original author: pmaupin  
https://github.com/pmaupin/pdfrw  
with minor modification by Daniel Chin for friendlier command-line calling  
  
usage: py -m pdf_unspread my.pdf  
  
Creates unspread.my.pdf  
  
Chops each page in half, e.g. if a source were  
created in booklet form, you could extract individual  
pages.

## pickle_preview.py
Preview a pickle file

## pickle_socket.py
A socket that supports object transmission. 

## pimport.py
pip install, and imports

## playwav.py
Light-weight wav player. 

## port_forward.py
Provides fake p2p, port forwarding.   
  
Ignored the thread-danger of sockets.   
Expect unexpected behaviors. 

## prime.py
Get prime numbers

## qr_now.py
Make a QR code instantly

## recvall.py
Receive `size` bytes from `socket`. Blocks until gets all.   
Somehow doesn't handle socket closing.   
I will fix that when I have time. 

## recvfile.py
receive a file from a socket with known length. 

## serve_now.py
Immediately open a port, accept connection  
and does nothing. 

## stats.py
What I learned from Statistics for Business and Finance. 

## terminalsize.py
Contributors of this code: Alexander Belchenko, Harco Kuppens, Justin Riley.   
http://code.activestate.com/recipes/440694-determine-size-of-console-window-on-windows/  
https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python  
https://gist.github.com/jtriley/1108174   
I changed python2 to python3, and added crediting printing. 

### To the Earth/To the Earth V8.py
A game by Daniel.   
  
Updates description:  
    V3:  
        + Added: new weapon = Holy Sickle  
            Acquired through Annoying Cat  
            Ulti: ATK+1  
            20% Vamparic.  
        + Added: Personal high score.  
        + Improved: Game over prompt.  
    V4:  
        Fixed: Holy Sickle works properly now.  
    V5:  
        Fixed: Now the game actually restarts when you die.  
        + Added: Next Daily Hint  
        Edit: Intro screen now uses black background  
        Fixed: Daily Hint regarding the behavior of Annoying cat.  
        + Added: drop weapon msg  
        Fixed: DeltaHP now reflects the aggregate effect of healing and dmg  
        Fixed: Easter item drop rate was higher than normal weapons'...  
        Fixed: Critical Hit chance > 100%  
        + Added: Holy Sickle now increase GamePace.   
        + Added: When Holy Sickle ATK=100, Ulti becomes IronMan  
    V6:  
        very hihg speed -> incredible hihg speed  
    V7:  
        First play will show kidding death msg  
    V8:  
        Changed the abbr of Space Corgi to " Corgi"

## tree.py
Data type that stores file directory structure. 

