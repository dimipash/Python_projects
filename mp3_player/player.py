import os
from tkinter import Tk, PhotoImage, Label, Button, Frame, Listbox, Scrollbar, filedialog
from pygame import mixer

root = Tk()
root.title("Simple Music Player")
root.geometry("485x700+290+10")
root.configure(background="#333333")
root.resizable(False, False)
mixer.init()


def add_music():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert("end", song)


def play_music():
    music_name = playlist.get("active")
    print(music_name[:-4])
    mixer.music.load(playlist.get("active"))
    mixer.music.play()


# Icon
lower_frame = Frame(root, bg="#FFFFFF", width=485, height=180)
lower_frame.place(x=0, y=400)

icon_image = PhotoImage(file="logo png.png")
root.iconphoto(False, icon_image)

frame_count = 30
frames = [
    PhotoImage(file="aa1.gif", format="gif -index %i" % i) for i in range(frame_count)
]


def update_animation(index):
    frame = frames[index]
    index += 1
    if index == frame_count:
        index = 0
    animation_label.configure(image=frame)
    root.after(40, update_animation, index)


animation_label = Label(root)
animation_label.place(x=0, y=0)
root.after(0, update_animation, 0)

play_button_image = PhotoImage(file="play1.png")
Button(
    root,
    image=play_button_image,
    bg="#FFFFFF",
    bd=0,
    height=60,
    width=60,
    command=play_music,
).place(x=215, y=487)

stop_button_image = PhotoImage(file="stop1.png")
Button(
    root,
    image=stop_button_image,
    bg="#FFFFFF",
    bd=0,
    height=60,
    width=60,
    command=mixer.music.stop,
).place(x=130, y=487)

volume_button_image = PhotoImage(file="volume.png")
Button(
    root,
    image=volume_button_image,
    bg="#FFFFFF",
    bd=0,
    height=60,
    width=60,
    command=mixer.music.unpause,
).place(x=20, y=487)

pause_button_image = PhotoImage(file="pause1.png")
Button(
    root,
    image=pause_button_image,
    bg="#FFFFFF",
    bd=0,
    height=60,
    width=60,
    command=mixer.music.pause,
).place(x=300, y=487)

menu_image = PhotoImage(file="menu.png")
Label(root, image=menu_image).place(x=0, y=580, width=485, height=120)

music_frame = Frame(root, bd=2, relief="ridge")
music_frame.place(x=0, y=585, width=485, height=100)

Button(
    root,
    text="Browse Music",
    width=59,
    height=1,
    font=("calibri", 12, "bold"),
    fg="Black",
    bg="#FFFFFF",
    command=add_music,
).place(x=0, y=550)

scrollbar = Scrollbar(music_frame)
playlist = Listbox(
    music_frame,
    width=100,
    font=("Times new roman", 10),
    bg="#333333",
    fg="grey",
    selectbackground="lightblue",
    cursor="hand2",
    bd=0,
    yscrollcommand=scrollbar.set,
)
scrollbar.config(command=playlist.yview)
scrollbar.pack(side="right", fill="y")
playlist.pack(side="right", fill="both")

root.mainloop()
