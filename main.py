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



def defrost_cycle(frost_buildup, temp_inside, door_open_freq, temp_outside):
    frost_thin, frost_medium, frost_thick = get_frostBuildUp(frost_buildup)
    temp_very_cold, temp_cold, temp_moderate = get_tempInside(temp_inside)
    door_rare, door_occasional, door_frequent = get_doorOpeningFreq(door_open_freq)
    outside_cold, outside_moderate, outside_warm = get_tempOutside(temp_outside)

    short_cycle = max(
        min(frost_thin, temp_moderate, door_rare, outside_cold),
        min(frost_thin, temp_cold, door_occasional, outside_cold),
        min(frost_thin, temp_moderate, door_frequent, outside_moderate)
    )
    medium_cycle = max(
        min(frost_medium, temp_cold, door_occasional, outside_moderate),
        min(frost_thin, temp_moderate, door_frequent, outside_cold),
        min(frost_medium, temp_moderate, door_occasional, outside_moderate),
        min(frost_thin, temp_cold, door_occasional, outside_moderate)
    )
    long_cycle = max(
        min(frost_thick, temp_cold, door_frequent, outside_warm),
        min(frost_medium, temp_very_cold, door_frequent, outside_warm),
        min(frost_thick, temp_very_cold, door_frequent, outside_moderate)
    )

    # Use max-min defuzzification (maximum of minimums)
    max_cycle_value = max(short_cycle, medium_cycle, long_cycle)
    if max_cycle_value == short_cycle:
        return "Short cycle"
    elif max_cycle_value == medium_cycle:
        return "Medium cycle"
    else:
        return "Long cycle"



if __name__ == '__main__':
    frost_buildup = float(input('Frost buildup in mm: '))
    temp_inside = float(input('Temparature Inside in °C: '))
    door_open_freq = float(input('Door opening frequency (times per day): '))
    temp_outside = float(input('Temparature Outside in °C: '))

    cycle_time = defrost_cycle(frost_buildup, temp_inside, door_open_freq, temp_outside)
    print(f"Defrost cycle time: {cycle_time}") 
