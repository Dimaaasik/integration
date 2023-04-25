import pygame

def flatten(img, factor:float):
    '''
    Changing size of image
    :param img: link on image
    :param factor: factor of image changing
    :return:
    '''
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rorate_center(win, image, top_left, angle:float):
    '''
    Rotate car rectangle around center.
    :param win: Surface of game area.
    :param image: Image which rotating.
    :param top_left: Position of top left corner.
    :param angle: Angle on which rotating image.
    '''
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center = image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font:str, text:str):
    '''
    Сalculates the center position for the text, given the size of the text itself.
    :param win: Surface of game area
    :param font: Game font.
    :param text: Text which will be print on the screen.
    '''
    render = font.render(text, 1, (255, 255, 0))
    win.blit(render, (win.get_width() / 2 - render.get_width() / 2 , ((win.get_height() / 2 - render.get_height() / 2) - 40) ))

