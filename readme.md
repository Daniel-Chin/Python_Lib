# How to run
**To run anything here, you need to add this repo to your `%PYTHONPATH%`!**  
*Otherwise nothing will work!*

A lot of the scripts include tests and demos.  
You can find them after `if __name__ == '__main__':` or in file `__main__.py`.  

# This repo is...
All the wheels I re-invented. 

# Wait, what?
This repo has various useful python tools and utils...  
and some projects that don't deserve a full repo.  

If you have questions or suggestions, please open an issue.  
(My repo doesn't have an issue yet... I figure it would be cool to have one...)

# Documentation
## 24solver.py
Do you know the 24 card game?  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/24solver.py)

## alarm.py
An alarm clock because the Win10 Alarm App HCI is trash.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/alarm.py)

## Archive/
Meaningless Archive of random Python Scripts I wrote.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/)

## Archive/'Response Generator'/
A prank.  
It was freshman year. I was introduced to Python by NYUSH.  
I made this for Zane.  
Try figuring out what it does.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/%27Response%20Generator%27/)

## Archive/archive_rrrr.py
To archive http://rrrrthats5rs.com

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/archive_rrrr.py)

## Archive/beta.py
experiment regarding covariance, coefficient, regression  
  
F: future price / market portfolio price  
S: spot price / stock price  
h: hedge ratio / beta  
  
Both F and S refers to per period return.

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/beta.py)

## Archive/bianQue.py
?????????????????????????????????????????????????????????

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/bianQue.py)

## Archive/chineseGamble.py
Liwei's gamble with ???????????????  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/chineseGamble.py)

## Archive/databass/
Oh damn! I read about `dbm` and will now dump this project.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/databass/)

## Archive/fileComplexity/
Tests the time complexity of small binary updates to large files.  

Conclusion: On my Windows, it's O(1).

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/fileComplexity/)

## Archive/LAN_scan/
Scans LAN

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/LAN_scan/)

## Archive/legacy_archive/
This was before I started to use Github, and I didn't do documentation.  
Consider this the pre-historical era.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/legacy_archive/)

## Archive/LenovoShipping/
Tried to implement SSH when I was young.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/LenovoShipping/)

## Archive/mim/mim.py
To test the security of getpass.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/mim/mim.py)

## Archive/mindustryKeyRemap.py
Too bad. It does not work. Mindustry 6.0 is anti-python?  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/mindustryKeyRemap.py)

## Archive/octave_up.py
Transpose an audio up one octave, by removing odd partials.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/octave_up.py)

## Archive/OneFileFly/
Transmit one file.  
Deprecated. Replaced by ../oneship

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/OneFileFly/)

## Archive/requests_futures_graceful.py
Does requests_futures interrupt the sockets on exit?    
Conclusion: even socket is graceful!

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/requests_futures_graceful.py)

## Archive/robust_persistent_data_solution.py
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

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/robust_persistent_data_solution.py)

## Archive/serial_self_latency.py
Measures the serial self-playback round trip time.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/serial_self_latency.py)

## Archive/SleepProber/
Keeps beeping, until the computer sleeps.  
Purpose: so you can tell if your computer is asleep.  
Useful in rare occasions.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/SleepProber/)

## Archive/WireVoice/
Simple experiment of dealing with sound data in real time.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Archive/WireVoice/)

## ascii_table.py
A beautiful script to print the ascii table. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/ascii_table.py)

## asyncException.py
Send exceptions to other threads.    
Based on Philippe F's https://stackoverflow.com/a/325528/8622053    
If the thread is busy in a system call (socket.accept(), ...),   
the exception is simply ignored.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/asyncException.py)

## async_std.py
Read from a PIPE async.    
See https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/async_std.py)

## audioCues.py
Play audio cues. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/audioCues.py)

## auto_bin.py
Auto bin number.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/auto_bin.py)

## babble.py
Repeatedly prints 'wobo wabble' indefinitely. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/babble.py)

## Beer on the Wall/
Bamboozling lyric-rolling music-playing windows-only python script

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Beer%20on%20the%20Wall/)

## blindDescend.py
Find local minima of a 1D function without gradient.    
Minimizes the number of calls to the function.    
Run this script to test it.    
Implementation:    
* A 3-point recursion of shifting and zooming    
* Cacheing with input as Fractions  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/blindDescend.py)

## bloonTools.py
automaitcally press 222222

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/bloonTools.py)

## book.py
A file system.    
Encrypts the file system with Fernet.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/book.py)

## cacheWithFile.py
````python  
@cacheWithFile('expanded_matrix')  
def expandMatrix(m):  
    # some heavy computation  
    result = ...  
    return result  
````

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/cacheWithFile.py)

## cache_no_hash.py
Inefficiently cache and lookup function returns. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/cache_no_hash.py)

## chdir_context.py
A context to temporarily cd to another directory.    
Frequently useful: ChdirAlongside(__file__)  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/chdir_context.py)

## cleanWordHtml.py
Input: MS Word generated html file.    
What it does: change encoding to utf-8, remove style info specific to Microsoft Outlook, replace curly double quotes (???) with straights (").  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/cleanWordHtml.py)

## clicker/__main__.py
Windows only.   
Use your phone to send UP and DOWN to your computer!   
Useful for reading in Kindle.   
  
WARNING: Running this may open vulnerabilities for your computer.   
Don't run this if you don't know what you are doing.   
Only run this if you are in a safe network, or inside a firewall.   
I am not responsible if someone attacks your computer through this server. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/clicker/__main__.py)

## Color_Tiles/
A game

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/Color_Tiles/)

## compile_readme.py
Iterate through all files in this repo  
build a readme.md for Github. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/compile_readme.py)

## console/
Runtime embedded interactive python shell, just like IPython.  

Windows only. If not windows, `console()` calls `IPython.embed()`.  
Usage: `console(globals())` or `console({**locals(), **globals()})`  

Advantages over IPython:  
* Lighter. Launches very quickly.  
* Other threads can still print things when user is inputting commands  
* Tab auto-completes your phrase, even under Windows! (I'm proud.)  
* Tired of having to `import` to test your module everytime you make an edit? `restart()` is what you need here. Ctrl+R does the same!  

Issues:  
* Reassigning module global variables will not be visible to module native codes. Sorry.  
* For unknown reasons, you cannot declare any name present in kernal.py that is invisible to the env.  
* Sometimes inline generator cannot access namespace. I can't stably replicate this issue, and I don't know what this is about.  

Fixed Issues:  
* If you wanna scroll up, you don't need to input() anymore!  
* Multi-line code continuation is implemented!  
* If input command is longer than terminal width, camera rolls.  

Future:  
* Consider adding a dynamic `return` feature.  
* Study passing namespace into `exec` and `evel` and use them.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/console/)

## console/kernal.py
For a clean namespace.    
I later realized that this can be done with arguments to exec and eval.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/console/kernal.py)

## count.py
For counting votes and ranking the counts.    
Oh! I guess `from collections import Counter` does the same for you!    
Although my thing is still more console friendly.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/count.py)

## dchin_log/__init__.py
Log script parameters as well as terminal output to files.    
Useful for simulation runs / deep learning experiments.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/dchin_log/__init__.py)

## dependencies.txt
Dependencies of this repo.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/dependencies.txt)

## dict_shape.py
Compare the shape of two dicts.   
i.e. is the structure the same? are the keys the same? 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/dict_shape.py)

## echo.py
print(sys.argv)

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/echo.py)

## editDistance.py
Uses dynamic programming (DP) to calculate the minimum editing distance.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/editDistance.py)

## exclusive.py
Use a file to denote whether a program is running.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/exclusive.py)

## Find Vera/Find_Vera V2.py
A game by Daniel

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Find%20Vera/Find_Vera%20V2.py)

## flashplayer/
Play swf files.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/flashplayer/)

## folder_go.py
To transmit a folder over the internet.    
Can continue on half-done job. Auto retry on connection failure. Skip files whose hash is the same.    
Does not include subfolders.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/folder_go.py)

## forcemap.py
Like dummy.Pool.map, but no limit of number of threads.   
Useful when IO-bound. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/forcemap.py)

## formula.py
Evaluate beautiful formulas like ???(2??3??4)  
(Those non-ascii math symbols)

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/formula.py)

## fractionToResistor.py
Given a fraction, find the resistor connection to achieve it.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/fractionToResistor.py)

## friendly_time.py
Formatting time data in a friendly manner. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/friendly_time.py)

## graphic_terminal.py
Tools to do graphics in the terminal.    
`clearLine`: fill the current line with ' ' (whitespace)    
`eastAsianStrLen`: length of str as displayed on terminal (so chinese characters and other fullwidth chars count as 2 or more spaces)    
`displayAllColors`: display all colors that your terminal supports.    
`printTable`: print a table in the terminal.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/graphic_terminal.py)

## harmonicSynth.py
Synthesize sound with harmonics.    
Interpolate between frames smartly.    
  
commit 490dd5810f39fc322a61cd444c581374323d8803 removed   
accelerated approach to correct mag. So now it only works   
if harmonic list input is stable in sequence. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/harmonicSynth.py)

## holdKeyContext.py
Uses the `keyboard` package to hold down a key.    
1. `with ...` clause avoids forgetting to release a key.    
2. Blocks the held key, and redirect it to your hook.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/holdKeyContext.py)

## httpmim.py
HTTP man in middle. Prints all traffic. Useful for investigating how http works. Although Chrome Dev Tools prolly have something like this already.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/httpmim.py)

## hub.py
Hub: forward all socket messages.   
Connect, sendall(b'OK'), forward...

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/hub.py)

## hybridSynth.py
Uses HarmonicSynth (precise) for the lower register   
and IfftSynth (fast) for the higher register.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/hybridSynth.py)

## icarusTools.py
1. automaitcally press FFFFFFFF    
2. Auto running with stamina management.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/icarusTools.py)

## ifftSynth.py
Synthesizes an audio page from a spectrum.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/ifftSynth.py)

## indentprinter.py
Indent log output in a logical way.    
Try this:    
```python  
from indentprinter import indentPrinter  
bois = ['Collie', 'Husky', 'Shoob', 'Shibe']  
print('All bois:')  
with indentPrinter as print:  
    [print(x) for x in bois]  
```

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/indentprinter.py)

## interactive/console_explorer.py
An android-friendly console file explorer. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/interactive/console_explorer.py)

## interactive/kbhit.py
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

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/interactive/kbhit.py)

## interactive/__init__.py
Terminal interactivity utils.    
  
`listen`: waits for key press.    
`inputChin`: It does everything. There are too many features to describe. Reading the source code is the only way.    
`Universe`: `x in Universe()` always returns `True` no matter what `x` is.    
`inputUntilValid`: re-asks if not valid.    
`multiLineInput`: user may input multi lines. Terminate with ^Z.    
  
Demo:    
Define in `__main__.py`. Run it, or run the module.    
  
Issues:    
* On Linux, Stopping the job and bringing it back to foreground messes up the terminal setting up (?)    
  
Future work:    
    Stop telling lies in `help(getFullCh)` on Linux.    
    https://stackoverflow.com/questions/48039759/how-to-distinguish-between-escape-and-escape-sequence  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/interactive/__init__.py)

## ipynb_to_py.py
Converts ipynb to py.   
Works even when Jupyter is not installed. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/ipynb_to_py.py)

## jdt.py
Progress bar.    
Did you know about `tqdm`?    
  
Usage:    
```python  
with Jdt(500, 'loading...') as j:  
    for i in range(500):  
        j.acc()  
        doJob(i)  
```  
  
Run this file to see demo.    
  
Set `override_terminal_width` when using Jupyter Notebook with jdt. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/jdt.py)

## joystick_cursor.py
Move cursor with Pro Controller.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/joystick_cursor.py)

## keepTop.py
Maintain a list of high scores.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/keepTop.py)

## lab.py
This is for me only.   
You won't get why this code is here.   
Give up. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/lab.py)

## linked_file_list.py
A double linked file list.    
A simple database solution, but highly scalable on systems that use hash map to store files.    
Each entry has a timestamp, and the list is sorted by time.    
Features:    
* Dynamic filename length, grows as the database grows.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/linked_file_list.py)

## local_ip.py
Find out local IP addr on Windows

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/local_ip.py)

## macro/
Record, play, save, and load macros.  
Windows only.  
PROTECTION: global hooked button to stop macro = Windows Key

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/macro/)

## manhattan/
Manhattan geometry, where Manhattan distance is the distance metric.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/manhattan/)

## md2html/__main__.py
Translate markdown .md file to html file.    
Note: to work on WordPress, avoid level one header (# Title).    
A lot of markdown features are not implemented!  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/md2html/__main__.py)

## md_headings.py
Print the headings of a markdown file.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/md_headings.py)

## MidiOverTCP.py
 -> LAN -> `Midi from TCP` as midi device ->  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/MidiOverTCP.py)

## minecraft_afk.py
AFK tool for Minecraft.    
Punch the air every 5 seconds so you don't get kicked for inactivity.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/minecraft_afk.py)

## mobileArrowKeys/
Simulate arrow keys with mobile web app.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/mobileArrowKeys/)

## mobileArrowKeys/__main__.py
WARNING: Running this may open vulnerabilities for your computer.   
Don't run this if you don't know what you are doing.   
Only run this if you are in a safe network, or inside a firewall.   
I am not responsible if someone attacks your computer through this server. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/mobileArrowKeys/__main__.py)

## mobileNumpad/
Your laptop has no numpad? Can't play Cataclysm:DDA? No worries. Use your phone as a numpad!  
This script hosts a webpage on your computer. Open the webpage on your phone.  
Issues: 
* "0" is not currently supported.  
* Digits may come out-of-order if the connection is poor.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/mobileNumpad/)

## mobileNumpad/__main__.py
WARNING: Running this may open vulnerabilities for your computer.   
Don't run this if you don't know what you are doing.   
Only run this if you are in a safe network, or inside a firewall.   
I am not responsible if someone attacks your computer through this server. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/mobileNumpad/__main__.py)

## moretk.py
tkinter gadgets and some util functions.    
`Msgbox`, `inputbox`, `screenCenter`, `StretchMessage`, `StretchPicture`, `ToughText`, `bilingualStringLen`.    
Run this file to see demo.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/moretk.py)

## multi_term/
Provides multiple terminal windows for output.  
Supports Windows OS.  

For demo, run file `__main__.py` or run this module via `py -m multi_term`.  
In the demo, there are multiple levels of output (info, debug, warning, error), redirected to each terminal.  

Uses sockets for inter-process communication.  
Future work:  
* Support more OSes.  
* Allow input from other terminals.  
* Replace lock for semaphore to launch terminals in parallel.  
* Remote terminal?

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/multi_term/)

## my.py
My misc little tools.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/my.py)

## myfile.py
Unreliable file utils

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/myfile.py)

## myhttp.py
Serves through a (super) simplified version of http protocol.   
Warning: Running this may expose your computer to attacks.   
Don't run this. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/myhttp.py)

## mymath.py
More math utils than just `import math`

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/mymath.py)

## myqr.py
Prints QR code to terminal. Ascii only: black whitespace and white whitespace

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/myqr.py)

## mysocket.py
My socket utils. Provides `recvall`, `recvFile`, `sendFileJdt`, and `findAPort`.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/mysocket.py)

## mythread.py
My threading utils

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/mythread.py)

## myxml.py
XML parser

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/myxml.py)

## netid2profile.py
For an NYU person, convert their netID to profile.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/netid2profile.py)

## newIgnore.py
Creates an empty `.gitignore` file.    
This is useful because Windows File Explorer forbids you from naming a file without base name, and `>` now creates files in UTF-16 with BOM encoding.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/newIgnore.py)

## Notes.txt
My personal notebook for learning Python. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Notes.txt)

## nothing.py


[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/nothing.py)

## nyu_ip/
Just to see how often NYU LAN re-allocates IP.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/nyu_ip/)

## oneship.py
?????????  
Transmit files over the internet / LAN  
No encryption! Consider everything you transmit broadcast to the entire network. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/oneship.py)

## os_stimulate.py
My laptop is weird. Running this script makes opening and terminating processes faster.   
Speculation: Taking CPU time away from Windows Defender? 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/os_stimulate.py)

## pdf_litouzhibei.py
LiTouZhiBei(Chinese: '\xe5\x8a\x9b\xe9\x80\x8f\xe7\xba\xb8\xe8\x83\x8c').    
Converts pdf from [p1, p2...] to [p1, p1, p2, p2...]  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/pdf_litouzhibei.py)

## pdf_unspread.py
Original author: pmaupin  
https://github.com/pmaupin/pdfrw  
with minor modification by Daniel Chin for friendlier command-line calling  
  
usage: py -m pdf_unspread my.pdf  
  
Creates my.unspread.pdf  
  
Chops each page in half, e.g. if a source were  
created in booklet form, you could extract individual  
pages.

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/pdf_unspread.py)

## pickle_preview/__main__.py
Preview a pickle file

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/pickle_preview/__main__.py)

## pickle_socket.py
A socket that supports object transmission. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/pickle_socket.py)

## pimport.py
pip install, and imports

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/pimport.py)

## playback.py
Playback audio in real-time.    
Useful if you want to hear your doorbell while watching videos   
with headphones.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/playback.py)

## playMidi.py
Uses mido to play a midi file.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/playMidi.py)

## playwav.py
Light-weight wav player. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/playwav.py)

## Ports.txt
Port specification for my applications.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Ports.txt)

## port_forward.py
Provides fake p2p, port forwarding.   
  
Ignored the thread-danger of sockets.   
Expect unexpected behaviors. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/port_forward.py)

## previewAudio.py
Plays an array of audio signal. Blocking.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/previewAudio.py)

## prime.py
Get prime numbers

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/prime.py)

## Push_Git.py
Interactive git commit and push.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/Push_Git.py)

## qrchat/__main__.py
Sets up a server, displays a QR code. Scan it to go to a web page. Exchange raw texts!    
Useful for sending a URL from the phone to the laptop.    
Warning: No authentication or encryption. Don't type in secrets. Don't assume who the remote is.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/qrchat/__main__.py)

## qr_now.py
Make a QR code instantly

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/qr_now.py)

## quad2quad.py
morph a quad into another quad. It's like 3D projection.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/quad2quad.py)

## questions.txt
Questions I have about Python.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/questions.txt)

## rand.py
I just wanna generate a random number very conveniently,    
e.g. Win+R py -m rand

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/rand.py)

## reactNew.py
Creates a react component file containing boilerplate code.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/reactNew.py)

## roundRobinSched.py
Time-based round robin scheduling.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/roundRobinSched.py)

## runamod.py
Run a python module but it waits at the end as if you called it in command line.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/runamod.py)

## safeserver/
A simple file server.  
Serves file in a folder.  
Has a simple html page interface.  
Built upon safe_http.py. Please see its documentation.  
Problems:  
* Does not sanitize html. But Don't panic! This is a file server and the threat only originates from local file names. Plus, "<>" is not allowed in filename.

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/safeserver/)

## safe_http.py
An HTTP backend server.    
Really tries to be safe against injection attacks.    
Intentionally uses single thread only.    
Only answers GET. Does not abide by request http header fields.    
Does not defend against DoS.    
Problems:    
* socket.send without timeout. Could block the entire scheduling.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/safe_http.py)

## scpsl/
Voice transformer for SCP:SL

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/scpsl/)

## screenCable/__main__.py
Playback a section of your screen.    
Useful for sharing PPT (with speaker notes on) over Tencent (VooV) Meeting.    
Hit `ESC` or `q` to quit.    
Hit `Spacebar` to refresh view.    
Click and drag to resize the window.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/screenCable/__main__.py)

## selectAudioDevice.py
A terminal interface that lets the user select   
the audio input/output device.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/selectAudioDevice.py)

## serial_monitor_colored.py
PySerial already has a CLI monitor, but when it receives   
color formatting codes, it tries to print unprintable   
characters. Let's fix that.    
Features:   
- Color formatting.    
- Attach a time stamp to each line.    
- Merge multiple ports into one terminal.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/serial_monitor_colored.py)

## serve_now.py
Immediately open a port, accept connection  
and does nothing. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/serve_now.py)

## smartBar.py
The bar chart provided by matplotlib is surprisingly manual.    
Let's fix that.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/smartBar.py)

## softmax.py
Softmax with temperature and probability weighting.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/softmax.py)

## stats.py
What I learned from Statistics for Business and Finance. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/stats.py)

## stellaris/__main__.py
Stellaris game assistant.    
Assignes hotkey to planet prev/next buttons and   
pop growth specification buttons.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/stellaris/__main__.py)

## streamProfiler.py
Profiles the computation time of a series of actions in a real-time stream-base application.    
Run the script to see a demo.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/streamProfiler.py)

## summarize_dependencies.py
Examines a directory of .py files and find all imports.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/summarize_dependencies.py)

## sys_path_context.py
A context to temporarily add paths to sys.path    
Useful for importing modules from a different directory. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/sys_path_context.py)

## terminalsize.py
Contributors of this code: Alexander Belchenko, Harco Kuppens, Justin Riley.   
http://code.activestate.com/recipes/440694-determine-size-of-console-window-on-windows/  
https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python  
https://gist.github.com/jtriley/1108174   
I changed python2 to python3, and added crediting printing. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/terminalsize.py)

## terraria.py
Terraria bot.  Automated fishing.    
Vision: bait catching, and defending invasions.    
Result: Failed! This macro does not work on Terraria!  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/terraria.py)

## To the Earth/To the Earth V8.py
A game by Daniel.   
  
My personal second / third python project. You can see a lot of bad coding styles.   
  
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

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/To%20the%20Earth/To%20the%20Earth%20V8.py)

## tree.py
Data type that stores file directory structure. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/tree.py)

## typofix/
My personal tool to fix typos.  
Assume you only do horizontal typos. No vertical typos. You may mistype E as R, but never as D.  
Also you may hit "=" instead of Backspace.  
Word data is from https://norvig.com/big.txt

[source code folder](https://github.com/Daniel-Chin/Python_Lib/blob/master/typofix/)

## udp_lab.py
Interactive shell to test UDP.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/udp_lab.py)

## voice_scroll.py
Scroll whatever you are reading with voice.    
low hum to scroll down. high hum to scroll up.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/voice_scroll.py)

## wget.py
Downloads a web resource.   
Provide no argument to enter interactive mode. 

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/wget.py)

## xls2csv.py
Convert xls or xlsx to csv.    
This loads the entire file content into RAM. Be careful with big files.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/xls2csv.py)

## yin.py
YIN pitch detection for a single page of audio.    
Modified from librosa's implementation of YIN.  

[source code](https://github.com/Daniel-Chin/Python_Lib/blob/master/yin.py)

