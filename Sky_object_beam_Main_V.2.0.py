import pygame
import sys
from skyfield import api as skyapi
from skyfield import named_stars
from skyfield.api import Star, load
from skyfield.data import hipparcos
import numpy as np
from datetime import datetime,timezone
import time
#from main_hardware_function_by_Puripat import *
# # # # # # # # # # # # En,step,dir Encode1,Encode2,maxstep(encode)
#Az_motor = stepper_motor(25,24,23,   27,22,1200)
#Al_motor = stepper_motor(1,7,8,      4,17,1200)

############################# pos setup #########################################
la = 13.70305556
long = 100.5265

deep_sky_objects = {
    'M112':{
        'RA': [12,41,22.6],
        'Dec': [-34,29,56.42],
        'Name': ['Unknown']
    },
    'M31': {
        'RA': [0, 44, 2.7],
        'Dec': [41, 16, 54.0],
        'Name': ['Andromeda Galaxy']
    },
    'M42': {
        'RA': [5, 35, 17.5],
        'Dec': [-5, 23, 28.6],
        'Name': ['Orion Nebula']
    },
    'M13': {
        'RA': [16, 41, 41.2],
        'Dec': [36, 27, 36.1],
        'Name': ['Hercules Cluster']
    },
    'M51': {
        'RA': [13, 29, 52.8],
        'Dec': [47, 11, 43.2],
        'Name': ['Whirlpool Galaxy']
    },
    'M57': {
        'RA': [18, 53, 35.1],
        'Dec': [32, 56, 54.3],
        'Name': ['Ring Nebula']
    },
    'NGC 869': {
        'RA': [2, 20, 14.0],
        'Dec': [57, 8, 23.0],
        'Name': ['Double Cluster']
    },
    'NGC 884': {
        'RA': [2, 20, 14.0],
        'Dec': [57, 8, 23.0],
        'Name': ['Double Cluster']
    },
    'NGC 7000': {
        'RA': [20, 58, 47.2],
        'Dec': [44, 20, 48.0],
        'Name': ['North America Nebula']
    },
    'NGC 4565': {
        'RA': [12, 36, 20.7],
        'Dec': [25, 59, 16.0],
        'Name': ['Needle Galaxy']
    },
    'NGC 6960': {
        'RA': [20, 45, 38.5],
        'Dec': [30, 43, 4.0],
        'Name': ['Veil Nebula']
    },
    'NGC 7293': {
        'RA': [22, 29, 38.9],
        'Dec': [-20, 50, 13.0],
        'Name': ['Helix Nebula']
    },
    'M45': {
        'RA': [3, 47, 24.6],
        'Dec': [24, 7, 0.0],
        'Name': ['The Pleiades']
    },
    'M44': {
        'RA': [8, 40, 24.3],
        'Dec': [19, 40, 48.0],
        'Name': ['The Beehive Cluster']
    },
    'M92': {
        'RA': [17, 17, 7.8],
        'Dec': [43, 8, 10.0],
        'Name': ['The Great Globular Cluster in Hercules']
    },
    'M8': {
        'RA': [18, 3, 37.2],
        'Dec': [-24, 23, 12.0],
        'Name': ['The Lagoon Nebula']
    },
}

############ get hour angle ###########
def arc_to_decimal(list_x):
    return list_x[0] + (list_x[1] / 60) + (list_x[2] / 3600)
def decimal_to_arc(x):
    x = x/24
    xhr = (x - int(x)) * 24
    xmin = (xhr - int(xhr)) * 60
    xsec = (xmin - int(xmin)) * 60
    return [int(xhr), int(xmin), xsec]

def getazal(rasp, decsp, la, long, sidlist):
    declist = [(int(decsp[0].split("deg")[0])), (int(decsp[1].split("'")[0])),(float(decsp[2].split('"')[0]))]
    if declist[0] >= 0 and (decsp[0].split("deg")[0]) != "-0":
        DEC = declist[0] + declist[1] / 60 + declist[2] / 3600
    else:
        DEC = declist[0] - declist[1] / 60 - declist[2] / 3600
    ralist = [(int(rasp[0].split("h")[0])), (int(rasp[1].split("m")[0])),(float(rasp[2].split("s")[0]))]
    if ralist[0] >= 0 and (rasp[0].split("h")[0]) != "-0":
        RA = arc_to_decimal(ralist)
    else:
        RA = ralist[0] - ralist[1] / 60 - ralist[2] / 3600
    HA = arc_to_decimal(sidlist) - arc_to_decimal(ralist)
    if HA < 0: HA = 24 + HA
    HA_in_deg = (HA / 24) * 360
    print(HA_in_deg)
    s = lambda x: np.sin(np.deg2rad(x))
    c = lambda x: np.cos(np.deg2rad(x))
    t = lambda x: np.tan(np.deg2rad(x))
    al = np.rad2deg( np.asin((s(DEC) * s(la)) + (c(DEC) * c(la) * c(HA_in_deg))))
    az = np.rad2deg( np.acos((s(la) * s(al) - s(DEC)) / (-c(la) * c(al))))
    if HA <= 12:  #East
        az = 360 - az
    print("HA :",decimal_to_arc(HA))
    print("SID :",sidlist)
    print(az,al)
    return az, al

############################## skyfield setup ###################

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)
planets = load('de421.bsp')
earth = planets['earth']
sun = planets['sun']
ra, dec, distance, ha, az, al = 0, 0, 0, 0, 0, 0
start_time = time.time()
current_deg_az = 0
current_deg_al = 0

def input(inp):
    global planets
    global earth
    global ra, dec, distance
    stardict = named_stars.named_star_dict
    ts = load.timescale()
    t = ts.now()
    inp = inp.capitalize()
    app_sun_ra , app_sun_dec, app_sun_distance  = earth.at(t).observe(sun).apparent().radec()
    print(app_sun_ra)
    ############# star #############
    if inp in stardict:
        barnards_star = Star.from_dataframe(df.loc[stardict[inp]])
        astrometric = earth.at(t).observe(barnards_star)
        ra, dec, distance = astrometric.radec()
        run()
    ############# planet #############
    elif inp + ' barycenter' in planets:
        planet = planets[inp + ' barycenter']
        astrometric = earth.at(t).observe(planet)
        ra, dec, distance = astrometric.radec()
        run()
    elif inp.upper() in deep_sky_objects.keys():
        pos = deep_sky_objects[inp.upper()]
        rightas = pos['RA']
        decli = pos['Dec']
        name = pos['Name'][0]
        print(name)
        ra = str(rightas[0]) + "h " + str(rightas[1]) + "m " + str(rightas[2]) + "s"
        dec = str(decli[0]) + "deg " + str(decli[1]) + "' " + str(decli[2]) + '"'
        run()

def run():
    global ra, dec, distance
    global ha, az, al
    global current_deg_az, current_deg_al
    ############################ Get day ###############################
    current_time = datetime.now(timezone.utc)
    print(current_time)
    datelist = str(current_time).split(" ")[0].split("-")
    timelist = str(current_time).split(" ")[1].split("+")[0].split(":")
    day_since_vernal = [344, 10, 40, 71, 101, 132, 163, 193, 224, 254, 285, 316]
    day = 0.5 #sidereal year is start at 12:00 which is 0.5day slower than tropical year
    day += day_since_vernal[int(datelist[1]) - 3] + float(datelist[2])
    if int(datelist[0]) % 4 == 0 and int(datelist[0]) % 100 != 0:
        if day > 344 and day < 365:
            day += 1
    if day >= 365:
        day = day - 365
    ################## get sidereal time ###############
    sec_since_vernal = (day * 24 * 60 * 60) + (float(timelist[0]) * 3600) + (float(timelist[1]) * 60) + float(timelist[2])
    local_sec_since_vernal = sec_since_vernal + (long * 60 * 60 / 15)
    sidsec = local_sec_since_vernal * (366.24219 / 365.24219)
    sidlist = decimal_to_arc(sidsec / (60*60))
    ralist = str(ra).split(" ")
    decsplist = str(dec).split(" ")
    az, al = getazal(ralist, decsplist, la, long, sidlist)
    need_az = az - current_deg_az
    need_al = al - current_deg_al
    azhr = int(az)
    azmin = (az - int(az)) * 60
    azsec = (azmin - int(azmin)) * 60
    alhr = int(al)
    almin = (al - int(al)) * 60
    alsec = (almin - int(almin)) * 60
    az = f"{azhr}° {int(azmin)}' {round(azsec, 1)}''"
    al = f"{alhr}° {abs(int(almin))}' {abs(round(alsec, 3))}''"
    if need_az > 180:
       need_az -= 360
    if need_al > 180:
       need_al -= 360
    #Az_motor.drive_angle(need_az, 3)
    #Al_motor.drive_angle(need_al, 3)
    current_deg_az = need_az
    current_deg_al = need_al

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 255)
RED = (200, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((1000, 500))# , pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Celestial Starlight Enigma Proxima Nebula Beam")
FONT_SIZE = round(screen_width * 0.05)
font = pygame.font.Font(None, FONT_SIZE)

KEYBOARD_LAYOUT = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ENT', 'DEL'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D'],
    ['F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

def draw_keyboard(keys, start_x, start_y, button_width, button_height, spacing, pressed_key):
    buttons = []
    for row_index, row in enumerate(keys):
        for col_index, key in enumerate(row):
            y = start_y + row_index * (button_height + spacing)
            if key == 'ENT':
                x = start_x + col_index * (button_width + spacing)
                rect = pygame.Rect(x, y, button_width * 2, button_height)
            elif key == 'DEL':
                x = start_x + col_index * (button_width + spacing * 2.65)
                rect = pygame.Rect(x, y, button_width * 2, button_height)
            else:
                x = start_x + col_index * (button_width + spacing)
                rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((key, rect))
            color = DARK_BLUE if key == pressed_key else BLACK
            pygame.draw.rect(screen, color, rect, 2)
            txt_surface = font.render(key, True, color)
            screen.blit(txt_surface,
                        (x + (rect.width - txt_surface.get_width()) // 2,
                         y + (button_height - txt_surface.get_height()) // 2))
    return buttons

def draw_buttons(button_texts, start_x, start_y, button_width, button_height, pressed):
    rect = pygame.Rect(start_x, start_y, button_width, button_height)
    color = DARK_BLUE if pressed else BLACK
    pygame.draw.rect(screen, color, rect, 2)
    txt_surface = font.render(button_texts, True, color)
    screen.blit(txt_surface,
                (start_x + (rect.width - txt_surface.get_width()) // 2,
                 start_y + (button_height - txt_surface.get_height()) // 2))
    return rect

def main():
    global az, al, current_deg_az, current_deg_al
    input_box = pygame.Rect(screen_width * 0.05, screen_height * 0.03, 140, FONT_SIZE)
    reset_button = draw_buttons("Reset position", screen_width * 0.3, screen_height * 0.54, screen_width * 0.4, screen_height * 0.1, False)
    night_mode_button = draw_buttons("Night", screen_width * 0.95, screen_height * 0.1, screen_width * 0.3, screen_height * 0.1, False)
    color = pygame.Color('lightskyblue3')
    text = ''
    done = False
    button_width = screen_width // 20
    button_height = screen_height // 12
    spacing = screen_width // 300
    start_x = screen_width * 0.05
    start_y = screen_height * 0.65
    keyboard_buttons = []
    pressed_key = None
    pressed_reset = False
    pressed_night_mode = False
    night_mode = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, rect in keyboard_buttons:
                    if rect.collidepoint(event.pos):
                        pressed_key = key
                        if key == 'ENT':
                            input(text)
                            text = ''
                        elif key == 'DEL':
                            text = text[:-1]
                        else:
                            text += key
                        break
                if reset_button.collidepoint(event.pos):
                    pressed_reset = True
                    if current_deg_az > 180:
                       current_deg_az -= 360
                    if current_deg_al > 180:
                       current_deg_al -= 360
                    #Az_motor.drive_angle(-current_deg_az, 3)
                    #Al_motor.drive_angle(-current_deg_al, 3)
                    current_deg_az = 0
                    current_deg_al = 0
                    break
                if night_mode_button.collidepoint(event.pos):
                    pressed_night_mode = True
                    night_mode = not night_mode
                    break
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed_key = None
                pressed_reset = False
                pressed_night_mode = False

        screen.fill(WHITE)
        txt_surface = font.render(text, True, BLACK)
        width = max(screen_width // 5, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        additional_texts = [
            f"RA : {ra}", f"Azi cal : {az}", "Azi read",
            f"Lat : {round(la, round(screen_width * 0.005))}"
        ]
        for i, line in enumerate(additional_texts):
            additional_surface = font.render(line, True, BLACK)
            screen.blit(additional_surface,
                        (screen_width * 0.02, screen_height * 0.15 + i * (FONT_SIZE - 5)))

        additional_texts = [
            f'DEC : {str(dec).replace("deg","°")}', f"Alt cal : {al}",
            "Alt read", f"Long : {round(long, round(screen_width * 0.005))}"
        ]
        for i, line in enumerate(additional_texts):
            additional_surface = font.render(line, True, BLACK)
            screen.blit(additional_surface,
                        (screen_width * 0.52, screen_height * 0.15 + i * (FONT_SIZE - 5)))

        keyboard_buttons = draw_keyboard(KEYBOARD_LAYOUT, start_x, start_y, button_width, button_height, spacing, pressed_key)
        reset_button = draw_buttons("Reset position", screen_width * 0.3, screen_height * 0.54, screen_width * 0.4, screen_height * 0.1, pressed_reset)
        night_mode_button = draw_buttons("Night", screen_width * 0.8, screen_height * 0.05, screen_width * 0.15, screen_height * 0.1, pressed_night_mode)
        
        if night_mode:
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))
            
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()