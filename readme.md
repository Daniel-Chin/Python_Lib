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
## 24solver.py
Do you know the 24 card game?  

## Archive/
Meaningless Archive of random Python Scripts I wrote.

### Archive/'Response Generator'/
A prank.  
It was freshman year. I was introduced to Python by NYUSH.  
I made this for Zane.  
Try figuring out what it does.

### Archive/archive_rrrr.py
To archive http://rrrrthats5rs.com

### Archive/LAN_scan/
Scans LAN

### Archive/legacy_archive/
This was before I started to use Github, and I didn't do documentation.  
Consider this the pre-historical era.

### Archive/LenovoShipping/
Tried to implement SSH when I was young.

#### Archive/mim/mim.py
To test the security of getpass.  

### Archive/OneFileFly/
Transmit one file.  
Deprecated. Replaced by ../oneship

#### Archive/OneFileFly/OneFileFly.py
by Daniel

### Archive/robust_persistent_data_solution.py
There are two copies of the database.    
We use a "which_file" to point to the valid one of the two.    
Read operation:    
    Read the valid database.    
Write operation:    
    Write to the invalid database. Close it.    
    Change which_file to point to the database we wrote to.    
This ensures:    
* Whenever the user unplug their machine, the which_file always points to a non-corrupted database.    
* Every write operation is atomic. Either we revert back to the state before the write, or the write is 100% complete. There is no middle state.    
However, concurrent writing leads to undefined behavior.    
  
I don't know what this strategy is called. If you know what it's called, please open an issue and tell me.  

### Archive/SleepProber/
Keeps beeping, until the computer sleeps.  
Purpose: so you can tell if your computer is asleep.  
Useful in rare occasions.

### Archive/WireVoice/
Simple experiment of dealing with sound data in real time.

## ascii_table.py
A beautiful script to print the ascii table. 

## babble.py
Repeatedly prints 'wobo wabble' indefinitely. 

## Beer on the Wall/
Bamboozling lyric-rolling music-playing windows-only python script

## book.py
A file system.    
Encrypts the file system with Fernet.  

## cache_no_hash.py
Inefficiently cache and lookup function returns. 

## chdir_context.py
A context to temporarily cd to another directory.    
Frequently useful: Chdir2(__file__)  

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
I later realized that this can be done with arguments to exec and eval.  

### console/__init__.py
Windows only. If not windows, `console()` calls `IPython.embed()`.   
Usage: `console(globals())` or `console({**locals(), **globals()})`  
Advantages over IPython:    
    1. Lighter    
    2. Other threads can still print things when user is inputting commands    
    3. Tab auto-completes your phrase, even under Windows! (I'm proud.)    
    4. Tired of having to `import` to test your module everytime you make an edit? `restart()` is what you need here. Ctrl+R does the same!    
Issues:    
    1. Reassigning module global variables will not be visible to module native codes. Sorry.    
    2. For unknown reasons, you cannot declare any name present in kernal.py that is invisible to the env.    
    3. Sometimes inline generator cannot access namespace. I can't stably replicate this issue, and I don't know what this is about.    
Fixed Issues:    
    1. If you wanna scroll up, you don't need to input() anymore!    
    2. Multi-line code continuation is implemented!    
    3. If input command is longer than terminal width, camera rolls.    
Future:    
    1. Consider adding a dynamic `return` feature.    
    2. Study passing namespace into `exec` and `evel` and use them.  

## count.py
For counting votes and ranking the counts.    
Oh! I guess `from collections import Counter` does the same for you!    
Although my thing is still more console friendly.  

## dependencies.txt
Dependencies of this repo.  

## dict_shape.py
Compare the shape of two dicts.   
i.e. is the structure the same? are the keys the same? 

## echo.py
print(sys.argv)

### Find Vera/Find_Vera V2.py
A game by Daniel

## flashplayer/
Play swf files.

## folder_go.py
To transmit a folder over the internet.    
Can continue on half-done job. Auto retry on connection failure. Skip files whose hash is the same.    
Does not include subfolders.  

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
`clearLine`: fill the current line with ' ' (whitespace)    
`eastAsianStrLen`: length of str as displayed on terminal (so chinese characters and other fullwidth chars count as 2 or more spaces)    
`displayAllColors`: display all colors that your terminal supports.  

## httpmim.py
HTTP man in middle. Prints all traffic. Useful for investigating how http works. Although Chrome Dev Tools prolly have something like this already.  

## hub.py
Hub: forward all socket messages.   
Connect, sendall(b'OK'), forward...

## indentprinter.py
Indent log output in a logical way.    
Try this:    
```python  
from indentprinter import *  
bois = ['Collie', 'Husky', 'Shoob', 'Shibe']  
print('All bois:')  
with indentPrinter:  
    [print(x) for x in bois]  
```

### interactive/console_explorer.py
An android-friendly console file explorer. 

### interactive/kbhit.py
A Python class implementing KBHIT, the standard keyboard-interrupt poller.  
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work  
with IDLE.  
  
This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU Lesser General Public License as   
published by the Free Software Foundation, either version 3 of the   
License, or (at your option) any later version.  
  
This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU General Public License for more details.

### interactive/__init__.py
Terminal interactivity utils.    
Issues:    
    * On Linux, Stopping the job and bringing it back to foreground   
        messes the terminal setting up (?)    
Future work:    
    Stop telling lies in `help(getFullCh)` on Linux.    
    https://stackoverflow.com/questions/48039759/how-to-distinguish-between-escape-and-escape-sequence  

## ipynb_to_py.py
Converts ipynb to py.   
Works even when Jupyter is not installed. 

## jdt.py
Progress bar. 

## lab.py
This is for me only.   
You won't get why this code is here.   
Give up. 

## linked_file_list.py
A double linked file list.    
A simple database solution, but highly scalable.    
Each entry has a timestamp, and the list is sorted by time.    
Features:    
* Dynamic filename length, grows as the database grows.  

## local_ip.py
Find out local IP addr on Windows

## macro/
Record, play, save, and load macros.  
Windows only.  
PROTECTION: global hooked button to stop macro = Windows Key

### md2html/__main__.py
Translate markdown .md file to html file.    
Note: to work on WordPress, avoid level one header (# Title).  

## minecraft_afk.py
AFK tool for Minecraft.  

## moretk.py
More tkinter gadgets

### multi_term/__init__.py
Provides multiple terminal windows for output.    
Supports Windows OS.    
Uses sockets to inter-process communication.    
Future work:    
* Support more OSes.    
* Allow input from other terminals.    
* Replace lock for semaphore to launch terminals in parallel.    
* Remote terminal?  

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

## myqr.py
Prints QR code to terminal. Ascii only: black whitespace and white whitespace

## mysocket.py
My socket utils. Provides `recvall`, `recvFile`, `sendFileJdt`, and `findAPort`.  

## mythread.py
My threading utils

## myxml.py
XML parser

## netid2profile.py
For an NYU person, convert their netID to profile.  

## Notes.txt
My personal notebook for learning Python. 

## nothing.py


## nyu_ip/
Just to see how often NYU LAN re-allocates IP.

## oneship.py
?????????  
Transmit files over the internet / LAN  
No encryption! Consider everything you transmit broadcast to the entire network. 

## os_stimulate.py
My laptop is weird. Running this script makes opening and terminating processes faster.   
Speculation: Taking CPU time away from Windows Defender? 

## pdf_litouzhibei.py
LiTouZhiBei(Chinese: '\xe5\x8a\x9b\xe9\x80\x8f\xe7\xba\xb8\xe8\x83\x8c').    
Converts pdf from [p1, p2...] to [p1, p1, p2, p2...]  

## pdf_unspread.py
Original author: pmaupin  
https://github.com/pmaupin/pdfrw  
with minor modification by Daniel Chin for friendlier command-line calling  
  
usage: py -m pdf_unspread my.pdf  
  
Creates unspread.my.pdf  
  
Chops each page in half, e.g. if a source were  
created in booklet form, you could extract individual  
pages.

### pickle_preview/__main__.py
Preview a pickle file

## pickle_socket.py
A socket that supports object transmission. 

## pimport.py
pip install, and imports

## playwav.py
Light-weight wav player. 

## Ports.txt
Port specification for my applications.  

## port_forward.py
Provides fake p2p, port forwarding.   
  
Ignored the thread-danger of sockets.   
Expect unexpected behaviors. 

## prime.py
Get prime numbers

## Push_Git.py
Interactive git commit and push.  

### qrchat/__main__.py
Sets up a server, displays a QR code. Scan it to go to a web page. Exchange raw texts!    
Useful for sending a URL from the phone to the laptop.    
Warning: No authentication or encryption. Don't type in secrets. Don't assume who the remote is.  

## qr_now.py
Make a QR code instantly

## questions.txt
Questions I have about Python.  

## reactNew.py
Creates a react component file containing boilerplate code.  

## safeserver/
A simple file server.  
Serves file in a folder.  
Has a simple html page interface.  
Built upon safe_http.py. Please see its documentation.  
Problems:  
* Does not sanitize html. But Don't panic! This is a file server and the threat only originates from local file names. Plus, "<>" is not allowed in filename.

## safe_http.py
An HTTP backend server.    
Really tries to be safe against injection attacks.    
Intentionally uses single thread only.    
Only answers GET. Does not abide by request http header fields.    
Does not defend against DoS.    
Problems:    
* socket.send without timeout. Could block the entire scheduling.  

## serve_now.py
Immediately open a port, accept connection  
and does nothing. 

## stats.py
What I learned from Statistics for Business and Finance. 

## summarize_dependencies.py
Examines a directory of .py files and find all imports.  

## terminalsize.py
Contributors of this code: Alexander Belchenko, Harco Kuppens, Justin Riley.   
http://code.activestate.com/recipes/440694-determine-size-of-console-window-on-windows/  
https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python  
https://gist.github.com/jtriley/1108174   
I changed python2 to python3, and added crediting printing. 

## terraria.py
Terraria bot.  Automated fishing.    
Vision: bait catching, and defending invasions.    
Result: Failed! This macro does not work on Terraria!  

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

## typofix/
My personal tool to fix typos.  
Assume you only do horizontal typos. No vertical typos. You may mistype E as R, but never as D.  
Also you may hit "=" instead of Backspace.  
Word data is from https://norvig.com/big.txt

## voice_scroll.py
Scroll whatever you are reading with voice.  

## wget.py
Downloads a web resource.   
Provide no argument to enter interactive mode. 

