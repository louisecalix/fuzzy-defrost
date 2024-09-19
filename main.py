def fuzzify_frost_buildup(mm):
    if mm < 2:
        return "Thin"
    elif 2 <= mm <= 5:
        return "Medium"
    else:
        return "Thick"

def fuzzify_temperature_inside(temp):
    if temp < -10:
        return "Very Cold"
    elif -10 <= temp <= 0:
        return "Cold"
    else:
        return "Moderate"

def fuzzify_door_opening_frequency(freq):
    if freq < 5:
        return "Rarely"
    elif 5 <= freq <= 8:
        return "Occasionally"
    else:
        return "Frequently"

def fuzzify_temperature_outside(temp):
    if temp < 20:
        return "Cold"
    elif 20 <= temp <= 30:
        return "Moderate"
    else:
        return "Warm"

def determine_defrost_cycle(frost_buildup, temp_inside, door_opening_freq, temp_outside):
    # Define the rules based on the provided conditions
    if frost_buildup == "Thin" and temp_inside == "Very Cold" and door_opening_freq == "Rarely" and temp_outside == "Cold":
        return "No Defrost"
    
    elif frost_buildup == "Thin" and temp_inside == "Very Cold" and door_opening_freq == "Occasionally" and temp_outside == "Moderate":
        return "No Defrost"
    
    elif frost_buildup == "Medium" and temp_inside == "Cold" and door_opening_freq == "Occasionally" and temp_outside == "Moderate":
        return "Short Defrost Cycle"
    
    elif frost_buildup == "Medium" and temp_inside == "Cold" and door_opening_freq == "Frequently" and temp_outside == "Moderate":
        return "Long Defrost Cycle"
    
    elif frost_buildup == "Thick" and temp_inside == "Cold" and door_opening_freq == "Occasionally" and temp_outside == "Warm":
        return "Long Defrost Cycle"
    
    elif frost_buildup == "Thick" and temp_inside == "Moderate" and door_opening_freq == "Frequently" and temp_outside == "Warm":
        return "Long Defrost Cycle"
    
    elif frost_buildup == "Thick" and temp_inside == "Moderate" and door_opening_freq == "Frequently" and temp_outside == "Moderate":
        return "Long Defrost Cycle"
    
    elif frost_buildup == "Medium" and temp_inside == "Cold" and door_opening_freq == "Rarely" and temp_outside == "Cold":
        return "Short Defrost Cycle"
    
    elif frost_buildup == "Thin" and temp_inside == "Cold" and door_opening_freq == "Frequently" and temp_outside == "Moderate":
        return "Short Defrost Cycle"
    
    elif frost_buildup == "Thick" and temp_inside == "Very Cold" and door_opening_freq == "Rarely" and temp_outside == "Warm":
        return "Long Defrost Cycle"
    
    else:
        return "No applicable defrost cycle found."

# Example Inputs
frozen_buildup_mm = float(input("Enter frost buildup in mm: "))
temperature_inside_c = float(input("Enter inside temperature in °C: "))
door_opening_frequency = int(input("Enter door opening frequency (times/day): "))
temperature_outside_c = float(input("Enter outside temperature in °C: ")) 

# Fuzzification of inputs
frost_buildup = fuzzify_frost_buildup(frozen_buildup_mm)
temp_inside = fuzzify_temperature_inside(temperature_inside_c)
door_frequency = fuzzify_door_opening_frequency(door_opening_frequency)
temp_outside = fuzzify_temperature_outside(temperature_outside_c)

# Determine the defrost cycle based on fuzzy logic rules
defrost_cycle_output = determine_defrost_cycle(frost_buildup, temp_inside, door_frequency, temp_outside)

# Display Results
print(f"\nDefroster Cycle Output: {defrost_cycle_output}")