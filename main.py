import tkinter as tk
from tkinter import ttk

def get_frostBuildUp(x):
    if x < 2:
        return (1, 0, 0)  # Thin, Medium, Thick
    elif 2 <= x <= 5:
        return (0, (5 - x) / 3, (x - 2) / 3)  # Thin, Medium, Thick
    else:
        return (0, 0, 1)  # Thin, Medium, Thick

def get_tempInside(x):
    if x < -18:
        return (1, 0, 0)  # Very Cold, Cold, Moderate
    elif -18 <= x <= -10:
        return (0, (-10 - x) / 8, (x + 18) / 8)  # Very Cold, Cold, Moderate
    elif -10 <= x <= -1:
        return (0, 1, 0)  # Very Cold, Cold, Moderate
    else:
        return (0, 0, 1)  # Very Cold, Cold, Moderate

def get_doorOpeningFreq(x):
    if x < 5:
        return (1, 0, 0)  # Rarely, Occasionally, Frequently
    elif 5 <= x <= 7:
        return (0, (7 - x) / 2, (x - 5) / 2)  # Rarely, Occasionally, Frequently
    else:
        return (0, 0, 1)  # Rarely, Occasionally, Frequently

def get_tempOutside(x):
    if x < 20:
        return (1, 0, 0)  # Cold, Moderate, Warm
    elif 20 <= x <= 30:
        return (0, (30 - x) / 10, (x - 20) / 10)  # Cold, Moderate, Warm
    else:
        return (0, 0, 1)  # Cold, Moderate, Warm

def defrost_cycle_weighted(frost_buildup, temp_inside, door_open_freq, temp_outside):
    # Get fuzzy values
    frost_values = get_frostBuildUp(frost_buildup)
    temp_inside_values = get_tempInside(temp_inside)
    door_open_freq_values = get_doorOpeningFreq(door_open_freq)
    temp_outside_values = get_tempOutside(temp_outside)

    # Evaluate rules
    defrost_cycle = "Short"  # Default to Short cycle

    # Apply rules
    if frost_values[2] > 0:  # Thick frost
        if temp_inside_values[1] > 0:  # Moderate
            defrost_cycle = "Medium"
        if temp_inside_values[0] > 0:  # Cold
            defrost_cycle = "Long"
    
    if frost_values[1] > 0:  # Medium frost
        if temp_inside_values[1] > 0:  # Moderate
            defrost_cycle = "Short"
        elif temp_inside_values[0] > 0:  # Cold
            defrost_cycle = "Medium"

    if frost_values[0] > 0:  # Thin frost
        if door_open_freq_values[2] > 0:  # Frequently
            defrost_cycle = "Short"
        elif door_open_freq_values[1] > 0:  # Occasionally
            defrost_cycle = "Short"
    
    if temp_outside_values[0] > 0:  # Cold outside
        if defrost_cycle == "Medium":
            defrost_cycle = "Long"  # Increase time if it's cold outside
    elif temp_outside_values[2] > 0:  # Warm outside
        if defrost_cycle == "Long":
            defrost_cycle = "Medium"  # Decrease time if it's warm outside


    return defrost_cycle


def simulate_defrost():
    frost_buildup = frost_slider.get()
    temp_inside = temp_inside_slider.get()
    door_open_freq = door_freq_slider.get()
    temp_outside = temp_outside_slider.get()

    cycle_time = defrost_cycle_weighted(frost_buildup, temp_inside, door_open_freq, temp_outside)
    result_label.config(text=f"Defrost cycle: {cycle_time}")




root = tk.Tk()
root.title("Refrigerator Defrost Simulator")

frost_label = tk.Label(root, text="Frost buildup (mm):")
frost_label.pack()
frost_slider = tk.Scale(root, from_=0, to_=10, orient="horizontal")
frost_slider.pack()

temp_inside_label = tk.Label(root, text="Temperature inside (°C):")
temp_inside_label.pack()
temp_inside_slider = tk.Scale(root, from_=-25, to_=5, orient="horizontal")
temp_inside_slider.pack()

door_freq_label = tk.Label(root, text="Door opening frequency (times per day):")
door_freq_label.pack()
door_freq_slider = tk.Scale(root, from_=0, to_=10, orient="horizontal")
door_freq_slider.pack()

temp_outside_label = tk.Label(root, text="Temperature outside (°C):")
temp_outside_label.pack()
temp_outside_slider = tk.Scale(root, from_=0, to_=40, orient="horizontal")
temp_outside_slider.pack()

start_button = tk.Button(root, text="Start Defrost Simulation", command=simulate_defrost)
start_button.pack()

result_label = tk.Label(root, text="Defrost cycle: ", font=("Arial", 14))
result_label.pack()

root.mainloop()
