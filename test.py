#run with pythonw
#add a readme for github (and a simple reason video why u made this)
#figure GUI
import tkinter as tk
import keyboard
import os
import json
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item
from datetime import datetime, timedelta

reminder_file = "reminder.json"
root = None  # Global variable to store the root window

def save_time_data(data):
    with open(reminder_file, 'w') as file:
        json.dump(data, file)

def load_timer_data():
    if os.path.exists(reminder_file):
        with open(reminder_file, 'r') as file:
            try:
                return json.load(file)
            except (ValueError, json.JSONDecodeError):
                return {}
    return {}

json_info = load_timer_data()

def parseTime(time):
    hours = 0
    minutes = 0
    for i, x in enumerate(time):
        if x in ['.', ':']:
            hours = int(time[:i])
        if x.lower() in ['a', 'p']:
            if '.' in time or ':' in time:
                minutes = int(time[i-2:i])
            else:
                minutes = 0
            if x.lower() == 'p' and hours != 12:
                hours += 12
            if x.lower() == 'a' and hours == 12:
                hours = 0
            break

    if hours > 23 or minutes > 59:
        raise ValueError("Invalid time format")

    return hours, minutes

def calculateTime(day, time):
    now = datetime.now()
    future_date = now + timedelta(days=int(day))  

    try:
        timeToSet = parseTime(time)
    except ValueError as e:
        print(f"Error parsing time: {e}")
        timeToSet = None

    if timeToSet:
        final_dateTime = future_date.replace(hour = timeToSet[0], minute = timeToSet[1])
        return final_dateTime
    else:
        return None

def setDateTime(event=None):  # Add event parameter for Enter key binding
    day = entry.get()
    time = timeEntry.get()

    dateTime = calculateTime(day, time)

    if not(dateTime):
        label.config(text = "Enter a correct day from now (non negative)")
        label2.config(text = "Enter time of format 2.54pm/am")
    else:
        json_info[user_input] = dateTime.strftime('%Y-%m-%d %H:%M:%S')
        save_time_data(json_info)
        root.destroy()  # Close the window after setting the date and time

def toggle():
    global entry, timeEntry, label2
    label.config(text="When do u wanna set it to (how many days from today)")
    entry.delete(0, tk.END)

    label2 = tk.Label(root, text="what time on said day (format 3pm 4pm 3.30am etc)")
    label2.pack()

    timeEntry = tk.Entry(root)
    timeEntry.pack()

    button.config(command=setDateTime)
    root.bind('<Return>', setDateTime)  # Bind Enter key to setDateTime function
    timeEntry.focus_set()  # Set focus to timeEntry

def on_click(event=None):  # Add event parameter for Enter key binding
    global user_input
    user_input = entry.get()
    toggle()

def showGUI():
    global label, entry, root, button
    root = tk.Tk()
    root.title("Simple GUI")

    label = tk.Label(root, text="enter a reminder")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text="Submit", command=on_click)
    button.pack()

    entry.focus_set()
    root.bind('<Return>', on_click)  # Bind Enter key to on_click function

    root.mainloop()

def on_quit(icon, item):
    icon.stop()

def create_image():
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 32, 64, 64), fill=(0, 0, 0))
    return image

keyboard.add_hotkey('ctrl+r', showGUI)

menu = (item('Quit', on_quit),)

icon = pystray.Icon("test_icon", create_image(), "Reminders App", menu)
icon.run()



