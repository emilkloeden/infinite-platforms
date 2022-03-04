import os
import pygame

from settings import TILE_SIZE

def import_folder(path):
    surface_list = []

    for _,__,img_files in os.walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (TILE_SIZE, TILE_SIZE))        
            surface_list.append(image_surf)

    return surface_list

def render_multi_colour_text(font, text, odd_colour, even_colour):
    odd_text = " ".join([c for c in text[::2]])
    even_text = " " + " ".join([c for c in text[1::2]])
    odd_image = font.render(odd_text, True, pygame.Color(odd_colour))
    even_image = font.render(even_text, True, pygame.Color(even_colour))
    return [odd_image, even_image]