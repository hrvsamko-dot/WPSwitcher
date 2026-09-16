#Hi there reader!!!
#This is my first project ever, so dont judge me too much. Tbh i didnt like my ruff wallpaper switcher and the only language i know is python.
#Most stuff here is done purely by my hand, but since i didnt know anything about customtkinter, pathlib, pillow and generaly app development, i had some help form AI.
#The stuff from customtkinter and pathlib is mostly just me reading documentation and experimenting.  When i used AI i just asked how does something work and used the examples to figure it out.
#Other times my code straight up failed, so i asked AI whats wrong (terminal said smth was wrong on line 1690 but my code was under 100). And thats the only times i straight up copied the snippet.
#Since the info was totaly new to me i kept some coments that show the was and explain stuff.
# I plan to upgrade it and implement classes and objects and maybe make it look better. Depends. And yeah this is for linux only, mainly arch.
# Enjoy!!!

import subprocess
import sys
import time
from pathlib import Path

import customtkinter as ctk
from PIL import Image, ImageFilter

#if no folder_path was given pop up window to set info
#Ask for path of your folder or use default folder
#use .exists() and is_dir() to verify
#if not fall to backup folder inside repo with a few wallappers
#then display all files with suffix .jpg .jpeg .png with .suffix()
#basics  ctk.CTk"package"(where, what, other_criteria)
#be able to use arrows to navigate and esc to leave and enter to "accept"
#blurred effects and slideshow
#when u choose a picture with enter, it sends a comand to your terminal and changes wallpaper using swww or awww
#be able to change path of the pictures if needed

#ctk.set_appearance_mode("dark")
CONFIG_FILE = Path("config.txt")
folder_path = ""
frame = None
def get_saved_path():
        if CONFIG_FILE.exists():
            path_txt = CONFIG_FILE.read_text().strip()
            return path_txt
        return ""

def save_path(folder_path):
    CONFIG_FILE.write_text(folder_path)





#subprocess.run(["hyprctl", "keyword", "windowrule2", "float, minsize 730 450, maxsize 730 450, title:^(switcher.app.py)$"], check=True)



CLASS = "Switcher.app.py"
Top = "TopLevel"
W, H = 730, 450
width_p, height_p= 350, 300

def hypr_eval(lua):
    r = subprocess.run(["hyprctl", "eval", lua], capture_output=True, text=True, check=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

rule_lua = f'''hl.window_rule({{
    name = "switcher-app-fixed-size",
    match = {{ initial_class = "{CLASS}" }},
    float = true,
    size = "{W} {H}",
    center = true,
}})'''


out, err, rc = hypr_eval(rule_lua)
print("rule:", out or err, "rc:", rc)

"""
rule_lua_2 = f'''hl.window_rule({{
    name = "top-level-fixed-size",
    match = {{ initial_class = "{Top}" }},
    float = true,
    size = "{width_p} {height_p}",
    center = true,
    }})'''

out2, err2, rc2 = hypr_eval(rule_lua_2)
print("rule:", out2 or err2, "rc:", rc2)
"""

###     Main window    ###
#app = ctk.CTk()     #Define the app window
app = ctk.CTk(className="switcher.app.py")
width = 730
height = 450
app.update_idletasks()
ctk.set_appearance_mode("dark")


screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = int((screen_width - width)/2)
y = int((screen_height - height)/2)
app.geometry(f"{width}x{height}+{x}+{y}")
app.update()

#app.count = 0       #keep count
app.overrideredirect(True)   #delete top bar
#app.wm_attributes("-type", "utility")  # Tell Hyprland this window is a panel/utility/splash widget     Options: "utility", "splash", "dock"
#app.pack_propagate(False)
#app.grid_propagate(False)
app.minsize(width, height)
app.maxsize(width, height)
app.resizable(False, False)

app.title("wpaper switcher")
app.grid_columnconfigure((0), weight=1)

if sys.platform.startswith("win"): # set transparency in windows
    transparent_color = '#000001' 
    app.attributes("-transparentcolor",  transparent_color) 
    app.config(bg=transparent_color)

elif sys.platform.startswith("darwin"): # set transparency in mac os
    transparent_color = 'systemTransparent' 
    app.attributes("-transparent", True) 
    app.config(bg=transparent_color)

else: 
    app.attributes('-alpha', 0.8) # no full transparency method in linux


#from some post i found for app transparency




### actual scrollfarem with wallpapers
def show_wpapers(folder_path):
    global frame, current_index, main_frame
    MAIN_SIZE = (320, 320)
    SIDE_SIZE = (200, 200)
    BLUR = 5
    
    main_frame = ctk.CTkFrame(app, width=730, height=450, corner_radius=20, fg_color="#1e1e2e", border_color="#3e233f", border_width=4)
    main_frame.pack(padx=0, pady=0, fill="both", expand=True)
    #main_frame.pack_propagate(False)

    #if main_frame is not None and main_frame.winfo_exists():
        #main_frame.destroy()

    if frame is not None and frame.winfo_exists():
        frame.destroy()
    #if 'frame' in globals() and frame.winfo_exists():
    #    frame.destroy()

    frame = ctk.CTkFrame(main_frame, width=710, height=360, fg_color="transparent")
    frame.pack(padx=10, pady=(10, 10), anchor="center")

    img_paths = []
    for file in Path(folder_path).rglob("*"):   #searches for files in the folder with the correct suffix
        if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            img_paths.append(file)

    current_index = 0
    def right_arrow(event):
        global current_index
        current_index = (current_index + 1) % len(img_paths) 
        display_update()
        
    def left_arrow(event):
        global current_index
        current_index = (current_index - 1) % len(img_paths)  
        display_update()
        
    left_label = ctk.CTkLabel(frame, text="", image=None, corner_radius=25, fg_color="transparent")
    #left_label.grid(row=0, column=0, padx=5)
    left_label.place(x=115, y=180, anchor="center")
    #left_label.pack(padx=20, pady=20,  expand=True)


    right_label = ctk.CTkLabel(frame, text="", image=None, corner_radius=25, fg_color="transparent")
    #right_label.grid(row=0, column=2, padx=5)
    right_label.place(x=595, y=180, anchor="center")
    #right_label.pack()
    
    img_label = ctk.CTkLabel(frame,text="", image=None, compound="top", corner_radius=25, fg_color="transparent")     #create 1 empty label where the image will be showm
    #img_label.grid(row=0, column=1, padx=8, pady=8)
    img_label.place(x=350, y=180, anchor="center")
    img_label.lift()
    #img_label.pack()

    img_cache = {}

    def blur_and_resize(path, size, blur):
        pil_img = Image.open(path)   #basics of Pillow and implementing it in tkinter
        pil_img.thumbnail(size)
        if blur > 0:
            pil_img = pil_img.filter(ImageFilter.BoxBlur(blur))
        return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)

    def get_img(index, size, blur=0):     #This is the cacheor dictionary that holds rendered images for smoother expeerience
        #index is a burner variable, it is there to say expect a variable with a number --> current_index
        #creates a special key for each picture
        cache_key = (index, size, blur)
        #new_key = int(cache_key[0])     #takes the 0th value of the cache_key so it can be used as list index
        path = index 
        #chceks if a picture with the index is in cache
        if cache_key in img_cache:
            return img_cache[cache_key]
        #if its not, it renders and resizes the picture --> the hard part
        ctk_img = blur_and_resize(path, size, blur)
        #finaly it saves the rendered picture to the cache for future use
        img_cache[cache_key] = (ctk_img)
        return img_cache[cache_key]
    
    def display_update():       #updates to image based on current index
        if not img_paths:
            return
        path = img_paths[current_index]
        name = path.relative_to(folder_path)     #relative_to() is used to delete "motherfolder" path to file
        left_idx = (current_index - 1) #% len(img_paths)
        right_index = (current_index + 1) % len(img_paths)

        #main images
        ctk_img = get_img(img_paths[current_index], MAIN_SIZE)
        img_label.configure(text=str(name), image=ctk_img)       #configure() changes the image in the label so it doesnt create images on top

        #left image
        img_left = get_img(img_paths[left_idx],  SIDE_SIZE, BLUR)
        left_label.configure(image=img_left)

        #Right image
        img_right = get_img(img_paths[right_index], SIDE_SIZE, BLUR)
        right_label.configure(image=img_right)



    def chosen_wpaper():
        command = f"awww img {img_paths[current_index]} --transition-fps 60 --transition-step 255 --transition-type wipe"
        subprocess.run(command, shell=True, check=True)

    ### some keybinds ###
    app.bind("<Right>", right_arrow)
    app.bind("<Left>", left_arrow)
    def comand():
        chosen_wpaper()
        app.destroy()
    app.bind("<Return>", lambda e: comand())
    display_update()

        ###  pop up window   ###

def show_popup():
    width_p = 350
    height_p = 300
    popup_win = ctk.CTkToplevel()
    popup_win.title("switcher-settings")   

    def fix_window(title, w, h):
        """Make the window with this title float, sized, and centered."""
        target = f'"title:{title}"'
        for _ in range(20):  # retry for up to 2 seconds while the window maps
            result = subprocess.run(
                ["hyprctl", "eval", f'hl.dispatch(hl.dsp.window.float({{ action = "set", window = {target} }}))'],
                capture_output=True, text=True, check=True
            )
            if result.stdout.strip() == "ok":
                break
            time.sleep(0.1)
        else:
            return  # never found it, give up quietly

        subprocess.run(["hyprctl", "eval", f'hl.dispatch(hl.dsp.window.resize({{ x = {w}, y = {h}, window = {target} }}))'], check=True)
        subprocess.run(["hyprctl", "eval", f'hl.dispatch(hl.dsp.window.center({{ window = {target} }}))'], check=True)

    popup_win.update_idletasks()
    popup_win.minsize(width_p, height_p)
    popup_win.maxsize(width_p, height_p)
    popup_win.resizable(False, False)
    xp = int((screen_width - width_p)/2)
    yp = int((screen_height - height_p)/2)
    popup_win.geometry(f"{width_p}x{height_p}+{xp}+{yp}")
    popup_win.attributes("-topmost", True)     #keeps on top
    popup_win.overrideredirect(True)
    #popup_win.wm_attributes("-type", "utility")  # Tell Hyprland this window is a panel/utility/splash widget   Options: "utility", "splash", "dock"
    app.pack_propagate(False)
    app.grid_propagate(False)
    popup_win.configure(fg_color="#1e1e2e", border_color="#3e233f",)
    popup_win.deiconify()
    fix_window("switcher-settings", width_p, height_p)
    
    
    entry = ctk.CTkEntry(popup_win, width=300, fg_color="#8b778d", placeholder_text="your folder path: ", placeholder_text_color="white")        #here u write the path to your folder
    entry.grid(row=2, column=0, padx=20, pady=(10, 10))
    username = ctk.CTkEntry(popup_win, width=300, fg_color="#8b778d", placeholder_text="your system username: ", placeholder_text_color="white")        #here u write the path to your folder
    username.grid(row=5, column=0, padx=20, pady=(10, 10))


    def button_callback():
        global folder_path
        val = var.get()
        user = username.get()
        if val == 2:
            folder_path = f"/home/{user}/.config/WPSwitcher/default_wallpaper/"
        elif val == 1:
            folder_path = entry.get()
        if Path(folder_path).exists() and Path(folder_path).is_dir():       #checks if it exists and is a dir
            save_path(folder_path)      #saves it to a notepad file
            show_wpapers(folder_path)       #shows wallpapers
            change_button()
            popup_win.destroy()         #closes popup window
        else:
            ctk.CTkLabel(popup_win, text="wrong path", text_color="red").grid(row=6, column=0, padx=20, pady=20, sticky="w")

    var = ctk.IntVar(value=2)       #InrVar() creates 1 variable for the button system with a base value that changes based on button action
    rbtn1 = ctk.CTkRadioButton(popup_win, text="own wpaper folder",fg_color="#3e233f",hover_color="#321b33",  variable=var, value=1)
    rbtn1.grid(row=0, column=0, padx=20, pady=20, sticky="w")
    rbtn2 = ctk.CTkRadioButton(popup_win, text="default wpaper folder",fg_color="#3e233f",hover_color="#321b33",  variable=var, value=2)
    rbtn2.grid(row=4, column=0, padx=20, pady=20, sticky="w")
    ctk.CTkButton(popup_win, text="Accept", fg_color="#3e233f",hover_color="#321b33", command=button_callback).grid(row=6, column=0, padx=20, pady=20, sticky="e")
    
    
    popup_win.bind("<Escape>", lambda event: popup_win.destroy())    #it seems like lambda e: or event: is used to set comands in binding
    popup_win.bind("<Return>", lambda e: button_callback())


def ch_button_callback():
    global folder_path, frame, main_frame  # noqa: PLW0602
    CONFIG_FILE.write_text("")
    CONFIG_FILE.unlink(missing_ok=True)
    folder_path = ""
    if frame is not None and frame.winfo_exists():
        frame.destroy()
    if main_frame is not None and main_frame.winfo_exists():
        main_frame.destroy()
    
    #if 'frame' in globals() and frame.winfo_exists():
    #        frame.destroy() 
    if "ch_btn" in globals() and ch_btn.winfo_exists():
        ch_btn.destroy()
    pop_condition()

def change_button():
    global ch_btn
    ch_btn = ctk.CTkButton(main_frame, width=300, height=50, text="change path to folder", fg_color="#3e233f",hover_color="#321b33", command=ch_button_callback)
    ch_btn.pack(padx=15, pady=15, side="bottom")
    #ch_btn.place(x=325, rely=350, anchor="center")
    #ch_btn.lift()

def pop_condition():            #the conditiom that checks if a folder exists, if yes it skips the popup
    global folder_path
    folder_path = get_saved_path()
    if folder_path == "" or not Path(folder_path).exists():
        show_popup()
    else:
        show_wpapers(folder_path)
        change_button()

app.bind("<Escape>", lambda e: app.destroy())
pop_condition()
app.mainloop()


