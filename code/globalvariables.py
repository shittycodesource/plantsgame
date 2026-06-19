import json

global_plants_data = None
global_zombie_data = None
dt = 0

def load_global_json():
    global global_plants_data
    global global_zombie_data

    if global_plants_data == None or global_zombie_data == None:    
        with open(f'../json/Plants.json', 'r', encoding='utf-8') as file:
            global_plants_data = json.load(file)

        with open(f'../json/Zombies.json', 'r', encoding='utf-8') as file:
            global_zombie_data = json.load(file)
    
load_global_json()