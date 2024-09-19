def get_frostBuildUp(mm):
    if mm < 2:
        return "Thin"
    elif 2 <= mm <= 5:
        return "Medium"
    else:
        return "Thick"

def fet_tempInside(temp):
    if temp < -10:
        return "Very Cold"
    elif -10 <= temp <= 0:
        return "Cold"
    else:
        return "Moderate"

def get_doorOpeningFreq(freq):
    if freq < 5:
        return "Rarely"
    elif 5 <= freq <= 8:
        return "Occasionally"
    else:
        return "Frequently"

def get_tempOutside(temp):
    if temp < 20:
        return "Cold"
    elif 20 <= temp <= 30:
        return "Moderate"
    else:
        return "Warm"


def fuzzy_rules(frost_buildup, temp_inside, door_opening_freq, temp_outside):

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



if __name__ == '__main__':
    frozen_buildup_mm = float(input("Enter frost buildup in mm: "))
    temperature_inside_c = float(input("Enter inside temperature in °C: "))
    door_opening_frequency = int(input("Enter door opening frequency (times/day): "))
    temperature_outside_c = float(input("Enter outside temperature in °C: ")) 

    frost_buildup = get_frostBuildUp(frozen_buildup_mm)
    temp_inside = fet_tempInside(temperature_inside_c)
    door_frequency = get_doorOpeningFreq(door_opening_frequency)
    temp_outside = get_tempOutside(temperature_outside_c)

    defrost_cycle_output = fuzzy_rules(frost_buildup, temp_inside, door_frequency, temp_outside)

    print(f"\nDefroster Cycle Output: {defrost_cycle_output}")