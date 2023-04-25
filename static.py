import pygame

def flatten(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

# Проблема поворота в том что нужно повернуть обертку (прямоугольник) не изменяя его позиций, а так же поворот должен быть вокруг его центра, для этого создается новый прямоугольник
def blit_rorate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center = image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font, text):
    render = font.render(text, 1, (255, 255, 0))
    win.blit(render, (win.get_width() / 2 - render.get_width() / 2 , ((win.get_height() / 2 - render.get_height() / 2) - 40) ))

