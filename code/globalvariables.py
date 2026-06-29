import json, time

global_plants_data = None
global_zombie_data = None
global_projectiles_data = None
dt = 0

score = 0
game_start_time = 0
pause_time_start = 0
pause_time_end = 0
pause_time_delta = 0

def load_global_json():
    global global_plants_data
    global global_zombie_data
    global global_projectiles_data

    if global_plants_data == None or global_zombie_data == None or global_projectiles_data == None:    
        with open(f'../json/Plants.json', 'r', encoding='utf-8') as file:
            global_plants_data = json.load(file)

        with open(f'../json/Zombies.json', 'r', encoding='utf-8') as file:
            global_zombie_data = json.load(file)

        with open(f'../json/Projectiles.json', 'r', encoding='utf-8') as file:
            global_projectiles_data = json.load(file)
    
load_global_json()

# def get_correct_update_time(update_time):
#     return update_time - ( pause_time_end - pause_time_start )

def get_correct_start_time(start_time):
    return time.time() - ( pause_time_end - pause_time_start )
