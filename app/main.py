import tkinter as tk
from PIL import Image



# Step 1: Get monitor info

# get monitor info from Windows API


# Step 2: Set up GUI
root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=400)
canvas.pack(side=tk.TOP)

# frame for monitor list and settings

settings_frame = tk.Frame(root)
settings_frame.pack(side=tk.BOTTOM)

# add monitor list to settings frame
monitor_list = tk.Listbox(settings_frame)
monitor_list.grid(row=0, column=0, rowspan=2, padx=10, pady=5)




def on_canvas_click(event):
    # find the monitor rectangle that was clicked on
    clicked_monitor = None
    for monitor_rect in monitors:
        if canvas.coords(monitor_rect)[0] <= event.x <= canvas.coords(monitor_rect)[2] \
            and canvas.coords(monitor_rect)[1] <= event.y <= canvas.coords(monitor_rect)[3]:
            clicked_monitor = monitor_rect
            break

    # if a monitor rectangle was clicked, remember it and its initial position
    if clicked_monitor is not None:
        clicked_monitor.initial_pos = (event.x, event.y)

def on_canvas_drag(event):
    # if a monitor rectangle is currently being dragged, move it
    for monitor_rect in monitors:
        if hasattr(monitor_rect, 'initial_pos'):
            dx = event.x - monitor_rect.initial_pos[0]
            dy = event.y - monitor_rect.initial_pos[1]
            canvas.move(monitor_rect, dx, dy)
            monitor_rect.initial_pos = (event.x, event.y)


# Step 3: Draw monitor setup on canvas
monitors = []  # list of monitor rectangles on canvas

def draw_monitor(monitor_info):
    monitor_rect = canvas.create_rectangle(
        monitor_info['x'], monitor_info['y'],
        monitor_info['x'] + monitor_info['width'],
        monitor_info['y'] + monitor_info['height']
    )
    monitors.append(monitor_rect)

def move_monitor(monitor_id, dx, dy):
    canvas.move(monitor_id, dx, dy)

canvas.bind('<Button-1>', on_canvas_click)
canvas.bind('<B1-Motion>', on_canvas_drag)

# Step 4: Set up monitor settings grid
monitor_settings = []  # list of settings dictionaries for each monitor

def add_monitor():
    name = name_entry.get()
    resolution = resolution_entry.get()
    width, height = map(int, resolution.split('x'))
    x, y = map(int, position_entry.get().split(','))
    monitor_info = {'name': name, 'width': width, 'height': height, 'x': x, 'y': y}
    monitor_settings.append(monitor_info)

    # create row in settings grid for new monitor
    row = len(monitor_settings) - 1
    name_label = tk.Label(settings_frame, text=name)
    name_label.grid(row=row, column=0)
    resolution_label = tk.Label(settings_frame, text=resolution)
    resolution_label.grid(row=row, column=1)
    position_label = tk.Label(settings_frame, text='({}, {})'.format(x, y))
    position_label.grid(row=row, column=2)
    move_button = tk.Button(settings_frame, text='Move', command=lambda monitor=monitor_info: move_monitor_on_canvas(monitor))
    move_button.grid(row=row, column=3)
    delete_button = tk.Button(settings_frame, text='Delete', command=lambda monitor=monitor_info: delete_monitor(monitor))
    delete_button.grid(row=row, column=4)

name_label = tk.Label(settings_frame, text='Name')
name_label.grid(row=0, column=0)
resolution_label = tk.Label(settings_frame, text='Resolution')
resolution_label.grid(row=0, column=1)
position_label = tk.Label(settings_frame, text='Position')
position_label.grid(row=0, column=2)
add_button = tk.Button(settings_frame, text='Add Monitor', command=add_monitor)
add_button.grid(row=0, column=3, padx=10, pady=5)

name_entry = tk.Entry(settings_frame)
name_entry.grid(row=1, column=0)
resolution_entry = tk.Entry(settings_frame)
resolution_entry.grid(row=1, column=1)
position_entry = tk.Entry(settings_frame)
position_entry.grid(row=1, column=2)


def move_monitor_on_canvas(monitor):
    # find monitor rectangle on canvas and move it
    for monitor_rect in monitors:
        if canvas.coords(monitor_rect)[0] == monitor['x'] and canvas.coords(monitor_rect)[1] == monitor['y']:
            dx, dy = 10, 10  # hardcoded for example purposes, you'll need to implement a way for the user to move the monitor on the canvas
            canvas.move(monitor_rect, dx, dy)
            monitor['x'] += dx
            monitor['y'] += dy
            # update corresponding label in settings grid
            for row, setting in enumerate(monitor_settings):
                if setting == monitor:
                    position_label = settings_frame.grid_slaves(row+1, 2)[0]
                    position_label.config(text='({}, {})'.format(monitor['x'], monitor['y']))
                    break

def delete_monitor(monitor):
    # remove monitor from settings grid and monitor_settings list
    for row, setting in enumerate(monitor_settings):
        if setting == monitor:
            monitor_settings.pop(row)
            settings_frame.grid_slaves(row+1, 0)[0].grid_forget()  # remove name label
            settings_frame.grid_slaves(row+1, 1)[0].grid_forget()  # remove resolution label
            settings_frame.grid_slaves(row+1, 2)[0].grid_forget()  # remove position label
            settings_frame.grid_slaves(row+1, 3)[0].grid_forget()  # remove move button
            settings_frame.grid_slaves(row+1, 4)[0].grid_forget()  # remove delete button
            break


# # Step 5: Cut image into wallpapers
# image = Image.open('large_image.jpg')
# for monitor_info in monitors:
#     wallpaper = image.crop((
#         monitor_info['x'], monitor_info['y'],
#         monitor_info['x'] + monitor_info['width'],
#         monitor_info['y'] + monitor_info['height']
#     ))
#     wallpaper.save('wallpaper_{}.jpg'.format(monitor_info['name']))


# Step 6: Set desktop wallpaper
# platform-dependent code here

root.mainloop()

