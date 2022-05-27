import webcolors
from colorthief import ColorThief
from scipy.spatial import KDTree
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb, CSS21_HEX_TO_NAMES

from google_speech import Speech
from translator import translate
import os


def get_colour_name(rgb_triplet):
    min_colours = {}
    for key, name in webcolors.CSS21_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour():
    color_thief = ColorThief('/home/pi/Desktop/output-1.jpg')

    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    
    colour = get_colour_name(dominant_color)
    
    translation = translate(str(colour))
    
    language = "bg"
    text = "главният цвят е " + translation 
    speech = Speech(text, language)
    speech.save("color.mp3")
    os.system('mpg321 color.mp3 &')