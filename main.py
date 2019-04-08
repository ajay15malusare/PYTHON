import os
import time
import threading
from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import ttk

root = Tk()  # create window

playlist = []


def about_us():
    tkinter.messagebox.showinfo('Our Title', 'This is info tha we want to display')


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    lb1.insert(index, filename)
    playlist.insert(index, filename_path)
    lb1.pack()
    index += 1


p = FALSE


def pause_music():
    global p
    p = TRUE
    mixer.music.pause()
    status['text'] = "Music Paused"


def show_details(pp):
    file_data = os.path.splitext(pp)
    # print(file_data)
    if file_data[1] == '.mp3':
        audio = MP3(pp)
        total_length = audio.info.length
    else:
        a = mixer.Sound(pp)
        total_length = a.get_length()

    mins, sec = divmod(total_length, 60)
    mins = round(mins)
    sec = round(sec)
    timeformat = '{:02d}:{:02d}'.format(mins, sec)
    label1['text'] = "Total Length:" + '-' + timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global p
    x = 0
    while x <= t and mixer.music.get_busy():
        if p:
            continue
        else:
            mins, sec = divmod(x, 60)
            mins = round(mins)
            sec = round(sec)
            timeformat = '{:02d}:{:02d}'.format(mins, sec)
            label2['text'] = "Current Length:" + '-' + timeformat
            time.sleep(1)
            x += 1


def play_music():
    global p
    if p:
        mixer.music.unpause()
        status['text'] = "Plying Music"
        p = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            select = lb1.curselection()
            select = int(select[0])
            play_it = playlist[select]
            mixer.music.load(play_it)
            mixer.music.play()
            status['text'] = "Plying Music" + '-' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("Error", "please select the song")


def next_music():
    global p
    if p:
        mixer.music.unpause()
        status['text'] = "Plying Music"
        p = FALSE
    else:
        try:
            next_selection = 0
            stop_music()
            time.sleep(1)
            select = lb1.curselection()
            if len(select) > 0:
                last_select = int(select[-1])

                lb1.selection_clear(select)

            # Make sure we're not at the last item
            if last_select < lb1.size() - 1:
                next_selection = last_select + 1

            lb1.activate(next_selection)
            lb1.selection_set(next_selection)

            play_it = playlist[next_selection]
            mixer.music.load(play_it)
            mixer.music.play()
            status['text'] = "Plying Music" + '-' + os.path.basename(play_it)
            show_details(play_it)

        except:
            tkinter.messagebox.showerror("Error", "please select the song")


def prev_music():
    global p
    if p:
        mixer.music.unpause()
        status['text'] = "Plying Music"
        p = FALSE
    else:
        try:
            next_selection = 0
            stop_music()
            time.sleep(1)
            select = lb1.curselection()
            if len(select) > 0:
                last_select = int(select[-1])

                lb1.selection_clear(select)

            # Make sure we're not at the last item
            if last_select >= lb1.size() - 1:
                next_selection = last_select - 1

            lb1.activate(next_selection)
            lb1.selection_set(next_selection)

            play_it = playlist[next_selection]
            mixer.music.load(play_it)
            mixer.music.play()
            status['text'] = "Plying Music" + '-' + os.path.basename(play_it)
            show_details(play_it)

        except:
            tkinter.messagebox.showerror("Error", "please select the song")


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)  # set_volume mixer takes value from 0 to 1


def stop_music():
    mixer.music.stop()
    status['text'] = "Music Stopped"


def re_music():
    play_music()
    status['text'] = "Music Rewinded"


muted = FALSE


def mu_music():
    global muted
    if muted:
        scale.set(70)
        mixer.music.set_volume(0.7)
        mu_Btn.configure(image=mu_photo1)
        muted = FALSE
    else:
        scale.set(0)
        mixer.music.set_volume(0)
        mu_Btn.configure(image=mu_photo2)
        muted = TRUE


def delete_file():
    select = lb1.curselection()
    select = int(select[0])
    lb1.delete(select)
    playlist.pop(select)


status = ttk.Label(root, text="Welcome to PyBeat", relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# create menu bar
menubar = Menu(root)
root.config(menu=menubar)

# create sub menu bar
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Close", command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About us", command=about_us)

mixer.init()  # initializing the mixer

root.title("PyBeat")
root.iconbitmap(r'image/pybeat.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)

l = ttk.Label(leftframe, text='Create play list')
l.pack(pady=10)
lb1 = Listbox(leftframe)
lb1.pack()

btn1 = ttk.Button(leftframe, text='+ADD', command=browse_file)
btn1.pack(side=LEFT)
btn2 = ttk.Button(leftframe, text='+DEL', command=delete_file)
btn2.pack()

rightframe = Frame()
rightframe.pack()

label1 = ttk.Label(rightframe, text='Total length:--:--')
label1.pack(pady=10)

label2 = ttk.Label(rightframe, text='Current length:--:--')
label2.pack(pady=10)

middleframe = Frame(rightframe)
middleframe.pack(padx=10, pady=10)



bottomframe = Frame(rightframe)
bottomframe.pack(padx=10, pady=10)

play_photo = PhotoImage(file='image/play.gif')
play_Btn = ttk.Button(bottomframe, image=play_photo, command=play_music)
play_Btn.grid(row=0, column=3);

# play_photo1 = PhotoImage(file='image/stop.png')
# stop_Btn = ttk.Button(middleframe, image=play_photo1, command=stop_music)
# stop_Btn.pack(side=LEFT, padx=10)

pause_photo1 = PhotoImage(file='image/pause.gif')
pause_Btn = ttk.Button(bottomframe, image=pause_photo1, command=pause_music)
pause_Btn.grid(row=0, column=1)

next_photo1 = PhotoImage(file='image/next.gif')
next_Btn = ttk.Button(bottomframe, image=next_photo1, command=next_music)
next_Btn.grid(row=0, column=4)

prev_photo1 = PhotoImage(file='image/prev.gif')
prev_Btn = ttk.Button(bottomframe, image=prev_photo1, command=prev_music)
prev_Btn.grid(row=0, column=2)

re_photo1 = PhotoImage(file='image/loop.gif')
re_Btn = ttk.Button(bottomframe, image=re_photo1, command=re_music)
re_Btn.grid(row=0, column=0)

mu_photo1 = PhotoImage(file='image/volume.gif')
mu_photo2 = PhotoImage(file='image/mute.gif')
mu_Btn = ttk.Button(bottomframe, image=mu_photo1, command=mu_music)
mu_Btn.grid(row=0, column=5)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=6, padx=10)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
