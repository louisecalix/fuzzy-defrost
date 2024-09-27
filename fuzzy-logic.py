import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class IceMeltAnimation:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.animation_running = False
        self.current_image_id = None 
        self.cooling = True
        
        self.images = [
            self.resize_image(os.path.join("D:", "fuzzy-logic", "ice_stage_1.png")),
            self.resize_image(os.path.join("D:", "fuzzy-logic", "ice_stage_2.png")),
            self.resize_image(os.path.join("D:", "fuzzy-logic", "ice_stage_3.png")),
            self.resize_image(os.path.join("D:", "fuzzy-logic", "ice_stage_4.png"))
        ]
        self.image_index = 0
        self.image_item = None
        
    


    def get_frostBuildUp(self, x):
        if x < 2:
            return (1, 0, 0)  # Thin, Medium, Thick
        elif 2 <= x <= 5:
            return (0, (5 - x) / 3, (x - 2) / 3)  # Thin, Medium, Thick
        else:
            return (0, 0, 1)  # Thin, Medium, Thick

    def get_tempInside(self, x):
        if x < -18:
            return (1, 0, 0)  # Very Cold, Cold, Moderate
        elif -18 <= x <= -10:
            return (0, (-10 - x) / 8, (x + 18) / 8)  # Very Cold, Cold, Moderate
        elif -10 < x <= -1:
            return (0, 0, 1)  # Very Cold, Cold, Moderate
        else:
            return (0, 0, 1)  # Very Cold, Cold, Moderate

    def get_doorOpeningFreq(self, x):
        if x < 5:
            return (1, 0, 0)  # Rarely, Occasionally, Frequently
        elif 5 <= x <= 7:
            return (0, (7 - x) / 2, (x - 5) / 2)  # Rarely, Occasionally, Frequently
        else:
            return (0, 0, 1)  # Rarely, Occasionally, Frequently

    def get_tempOutside(self, x):
        if x < 20:
            return (1, 0, 0)  # Cold, Moderate, Warm
        elif 20 <= x <= 30:
            return (0, (30 - x) / 10, (x - 20) / 10)  # Cold, Moderate, Warm
        else:
            return (0, 0, 1)  # Cold, Moderate, Warm

    def defrost_cycle_weighted(self, frost_buildup, temp_inside, door_open_freq, temp_outside):
        frost_values = self.get_frostBuildUp(frost_buildup)
        temp_inside_values = self.get_tempInside(temp_inside)
        door_open_freq_values = self.get_doorOpeningFreq(door_open_freq)
        temp_outside_values = self.get_tempOutside(temp_outside)

        defrost_score = 0
        
        if frost_values[2] > 0:  # Thick frost
            defrost_score += 2
        elif frost_values[1] > 0:  # Medium frost
            defrost_score += 1

        if temp_inside_values[0] > 0:  # Very Cold
            defrost_score += 1
        elif temp_inside_values[1] > 0:  # Cold
            defrost_score += 0.5

        if door_open_freq_values[2] > 0:  # Frequently
            defrost_score -= 0.5
        elif door_open_freq_values[1] > 0:  # Occasionally
            defrost_score -= 0.25

        if temp_outside_values[0] > 0:  # Cold outside
            defrost_score += 0.5
        elif temp_outside_values[2] > 0:  # Warm outside
            defrost_score -= 0.5

        

        if defrost_score >= 2:
            return "Long" # 30 minutes to 1 hour
        elif defrost_score >= 1:
            return "Medium" # 15-30 minutes
        else:
            return "Short" # 5-15 minutes

    def resize_image(self, image_path):
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image.resize((250, 150))) 

    def setup_gui(self):
        self.window_width = 1100  
        self.window_height = 700  
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack(fill="both", expand=True)

        
        background_image_path = os.path.join("D:", "fuzzy-logic", "background.png")
        self.original_background_img = Image.open(background_image_path)
        self.resized_background_img = self.original_background_img.resize((self.window_width, self.window_height))
        self.background_img = ImageTk.PhotoImage(self.resized_background_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        
        self.control_frame = tk.Frame(self.root, bg='white', bd=5)
        self.control_frame.place(relx=0.3, rely=0.5, anchor='center')

        
        self.create_controls()


        self.cooling_system_label = tk.Label(self.root, text="Cooling System Status: \nON", bg='white', font=("Arial", 12))
        self.cooling_system_label.place(relx=0.65, rely=0.25, anchor='center')

        self.cooling_circle = self.canvas.create_oval(0, 0, 20, 20, fill='green', outline='')  # Circle for cooling status
        self.update_cooling_circle_position()

    def create_controls(self):
        
        frost_label = tk.Label(self.control_frame, text="Frost buildup (mm):", bg='white')
        frost_label.pack()
        self.frost_slider = tk.Scale(self.control_frame, from_=0, to=10, orient="horizontal")
        self.frost_slider.pack()

        temp_inside_label = tk.Label(self.control_frame, text="Temperature inside (°C):", bg='white')
        temp_inside_label.pack()
        self.temp_inside_slider = tk.Scale(self.control_frame, from_=-25, to=5, orient="horizontal")
        self.temp_inside_slider.pack()

        door_freq_label = tk.Label(self.control_frame, text="Door opening frequency (times per day):", bg='white')
        door_freq_label.pack()
        self.door_freq_slider = tk.Scale(self.control_frame, from_=0, to=10, orient="horizontal")
        self.door_freq_slider.pack()

        temp_outside_label = tk.Label(self.control_frame, text="Temperature outside (°C):", bg='white')
        temp_outside_label.pack()
        self.temp_outside_slider = tk.Scale(self.control_frame, from_=0, to=40, orient="horizontal")
        self.temp_outside_slider.pack()

        start_button = tk.Button(self.control_frame, text="Start Defrost Simulation", command=self.simulate_defrost)
        start_button.pack()

        self.result_label = tk.Label(self.control_frame, text="Defrost cycle: ", font=("Arial", 14), bg='white')
        self.result_label.pack()


 
    def update_cooling_status(self):
        if self.cooling:
            print('COOLING ON')
            self.canvas.itemconfig(self.cooling_circle, fill='green')
            self.cooling_system_label.config(text="Cooling System Status: \nON")
        else:
            print('COOLING OFF')
            self.canvas.itemconfig(self.cooling_circle, fill='red')
            self.cooling_system_label.config(text="Cooling System Status: \nOFF")

    def update_cooling_circle_position(self):
        self.canvas.coords(self.cooling_circle, 600, 190, 580, 170)

    def simulate_defrost(self):
        frost_buildup = self.frost_slider.get()
        temp_inside = self.temp_inside_slider.get()
        door_open_freq = self.door_freq_slider.get()
        temp_outside = self.temp_outside_slider.get()

        cycle_time = self.defrost_cycle_weighted(frost_buildup, temp_inside, door_open_freq, temp_outside)
        self.result_label.config(text=f"Defrost cycle: {cycle_time}")

        self.cooling = False
        self.cooling_system_label.config(text="Cooling System Status: \nOFF")
        self.update_cooling_status()
        self.start_animation(cycle_time)

class IceMeltAnimation:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.animation_running = False
        self.current_image_id = None 
        self.cooling = True
        
        self.images = [
            self.resize_image(os.path.join("D:", "ice_stage_1.png")),
            self.resize_image(os.path.join("D:", "ice_stage_2.png")),
            self.resize_image(os.path.join("D:", "ice_stage_3.png")),
            self.resize_image(os.path.join("D:", "ice_stage_4.png"))
        ]
        self.image_index = 0
        self.image_item = None
        
    


    def get_frostBuildUp(self, x):
        if x < 2:
            return (1, 0, 0)  # Thin, Medium, Thick
        elif 2 <= x <= 5:
            return (0, (5 - x) / 3, (x - 2) / 3)  # Thin, Medium, Thick
        else:
            return (0, 0, 1)  # Thin, Medium, Thick

    def get_tempInside(self, x):
        if x < -18:
            return (1, 0, 0)  # Very Cold, Cold, Moderate
        elif -18 <= x <= -10:
            return (0, (-10 - x) / 8, (x + 18) / 8)  # Very Cold, Cold, Moderate
        elif -10 < x <= -1:
            return (0, 0, 1)  # Very Cold, Cold, Moderate
        else:
            return (0, 0, 1)  # Very Cold, Cold, Moderate

    def get_doorOpeningFreq(self, x):
        if x < 5:
            return (1, 0, 0)  # Rarely, Occasionally, Frequently
        elif 5 <= x <= 7:
            return (0, (7 - x) / 2, (x - 5) / 2)  # Rarely, Occasionally, Frequently
        else:
            return (0, 0, 1)  # Rarely, Occasionally, Frequently

    def get_tempOutside(self, x):
        if x < 20:
            return (1, 0, 0)  # Cold, Moderate, Warm
        elif 20 <= x <= 30:
            return (0, (30 - x) / 10, (x - 20) / 10)  # Cold, Moderate, Warm
        else:
            return (0, 0, 1)  # Cold, Moderate, Warm

    def defrost_cycle_weighted(self, frost_buildup, temp_inside, door_open_freq, temp_outside):
        frost_values = self.get_frostBuildUp(frost_buildup)
        temp_inside_values = self.get_tempInside(temp_inside)
        door_open_freq_values = self.get_doorOpeningFreq(door_open_freq)
        temp_outside_values = self.get_tempOutside(temp_outside)

        defrost_score = 0
        
        if frost_values[2] > 0:  # Thick frost
            defrost_score += 2
        elif frost_values[1] > 0:  # Medium frost
            defrost_score += 1

        if temp_inside_values[0] > 0:  # Very Cold
            defrost_score += 1
        elif temp_inside_values[1] > 0:  # Cold
            defrost_score += 0.5

        if door_open_freq_values[2] > 0:  # Frequently
            defrost_score -= 0.5
        elif door_open_freq_values[1] > 0:  # Occasionally
            defrost_score -= 0.25

        if temp_outside_values[0] > 0:  # Cold outside
            defrost_score += 0.5
        elif temp_outside_values[2] > 0:  # Warm outside
            defrost_score -= 0.5

        

        if defrost_score >= 2:
            return "Long" # 30 minutes to 1 hour
        elif defrost_score >= 1:
            return "Medium" # 15-30 minutes
        else:
            return "Short" # 5-15 minutes

    def resize_image(self, image_path):
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image.resize((250, 150))) 

    def setup_gui(self):
        self.window_width = 1100  
        self.window_height = 700  
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack(fill="both", expand=True)

        
        background_image_path = os.path.join("D:", "background.png")
        self.original_background_img = Image.open(background_image_path)
        self.resized_background_img = self.original_background_img.resize((self.window_width, self.window_height))
        self.background_img = ImageTk.PhotoImage(self.resized_background_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        
        self.control_frame = tk.Frame(self.root, bg='white', bd=5)
        self.control_frame.place(relx=0.3, rely=0.5, anchor='center')

        
        self.create_controls()


        self.cooling_system_label = tk.Label(self.root, text="Cooling System Status: \nON", bg='white', font=("Arial", 12))
        self.cooling_system_label.place(relx=0.65, rely=0.25, anchor='center')

        self.cooling_circle = self.canvas.create_oval(0, 0, 20, 20, fill='green', outline='')  # Circle for cooling status
        self.update_cooling_circle_position()

    def create_controls(self):
        
        frost_label = tk.Label(self.control_frame, text="Frost buildup (mm):", bg='white')
        frost_label.pack()
        self.frost_slider = tk.Scale(self.control_frame, from_=0, to=10, orient="horizontal")
        self.frost_slider.pack()

        temp_inside_label = tk.Label(self.control_frame, text="Temperature inside (°C):", bg='white')
        temp_inside_label.pack()
        self.temp_inside_slider = tk.Scale(self.control_frame, from_=-25, to=5, orient="horizontal")
        self.temp_inside_slider.pack()

        door_freq_label = tk.Label(self.control_frame, text="Door opening frequency (times per day):", bg='white')
        door_freq_label.pack()
        self.door_freq_slider = tk.Scale(self.control_frame, from_=0, to=10, orient="horizontal")
        self.door_freq_slider.pack()

        temp_outside_label = tk.Label(self.control_frame, text="Temperature outside (°C):", bg='white')
        temp_outside_label.pack()
        self.temp_outside_slider = tk.Scale(self.control_frame, from_=0, to=40, orient="horizontal")
        self.temp_outside_slider.pack()

        start_button = tk.Button(self.control_frame, text="Start Defrost Simulation", command=self.simulate_defrost)
        start_button.pack()

        self.result_label = tk.Label(self.control_frame, text="Defrost cycle: ", font=("Arial", 14), bg='white')
        self.result_label.pack()


 
    def update_cooling_status(self):
        if self.cooling:
            print('COOLING ON')
            self.canvas.itemconfig(self.cooling_circle, fill='green')
            self.cooling_system_label.config(text="Cooling System Status: \nON")
        else:
            print('COOLING OFF')
            self.canvas.itemconfig(self.cooling_circle, fill='red')
            self.cooling_system_label.config(text="Cooling System Status: \nOFF")

    def update_cooling_circle_position(self):
        self.canvas.coords(self.cooling_circle, 600, 190, 580, 170)

    def simulate_defrost(self):
        frost_buildup = self.frost_slider.get()
        temp_inside = self.temp_inside_slider.get()
        door_open_freq = self.door_freq_slider.get()
        temp_outside = self.temp_outside_slider.get()

        cycle_time = self.defrost_cycle_weighted(frost_buildup, temp_inside, door_open_freq, temp_outside)
        self.result_label.config(text=f"Defrost cycle: {cycle_time}")

        self.cooling = False
        self.cooling_system_label.config(text="Cooling System Status: \nOFF")
        self.update_cooling_status()
        self.start_animation(cycle_time)


    def start_animation(self, cycle_time):
        if self.current_image_id is not None:
            self.canvas.delete(self.current_image_id)

        if cycle_time == "Long":
            self.animation_duration = 7000  # 30 minutes 
        elif cycle_time == "Medium":
            self.animation_duration = 5000  # 15-30 minutes
        elif cycle_time == "Short":
            self.animation_duration = 3000  # 5-15 minutes

        self.animation_interval = self.animation_duration // (len(self.images) - 1)
        self.current_image_id = self.canvas.create_image(715, 275, anchor="center", image=self.images[0])
        self.animation_running = True
        self.image_index = 0

        self.animate()

    def animate(self):
        if self.animation_running:
            if self.image_index < len(self.images):
                self.canvas.itemconfig(self.current_image_id, image=self.images[self.image_index])
                self.image_index += 1
                self.root.after(self.animation_interval, self.animate)
            else:
                self.animation_running = False
                self.cooling = True
                self.update_cooling_status()

                self.canvas.delete(self.current_image_id)

    


    
root = tk.Tk()
root.title("Refrigerator Defrost and Ice Melting Simulation")
app = IceMeltAnimation(root)
root.mainloop()
