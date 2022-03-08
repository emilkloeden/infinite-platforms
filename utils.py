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


def load_high_score():
    try:
        with open(os.path.join("data", "high_score.txt"), "r") as f:
            return int(f.readline().strip())
    except FileNotFoundError:
        with open(os.path.join("data", "high_score.txt"), "w") as f:
            f.write(0)
        return 0
    except ValueError:
        return 0

def save_high_score(high_score):
    with open(os.path.join("data", "high_score.txt"), "w") as f:
        f.write(f"{int(high_score)}")

def load_background_images():
    return [
        pygame.image.load(os.path.join("assets", "backgrounds", png)).convert_alpha() 
        for png in os.listdir(os.path.join("assets", "backgrounds"))
        if png.lower().endswith(".png")
        ]