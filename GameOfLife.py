import pygame
from Cells import Cells
from time import time


BLACK = (16, 16, 16)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
CELL_UPDATE_FREQUENCY = 10
FPS = 60
CAPTION = "Cellular Automata"

# Press 1 to place glider
# press 2 to place ship
# press 3 to place pulsar
# press one of arrows to choose direction of the glider/ship


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    playing = False
    mouse_button_pressed = False
    object_to_place = 'square'
    count = 0
    generation_time = CELL_UPDATE_FREQUENCY / FPS

    cells = Cells(window, WIDTH, HEIGHT, CELL_SIZE)

    direction = 'random'
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        if count >= CELL_UPDATE_FREQUENCY:
            count = 0
            start = time()
            cells.new_generation()
            print(f'Generation time: {time() - start:.4f} s, '
                  f'Generation refresh time: {generation_time:.4f} s, '
                  f'Number of cells: {cells.get_number_of_cells()}')

        pygame.display.set_caption(CAPTION + ' - Playing' if playing else CAPTION + ' - Paused')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_pressed = True
                if object_to_place != 'square':
                    object_position = pygame.mouse.get_pos()
                    if object_to_place == 'glider':
                        cells.place_glider(object_position, direction=direction)
                    elif object_to_place == 'ship':
                        cells.place_ship(object_position, direction=direction)
                    elif object_to_place == 'pulsar':
                        cells.place_pulsar(object_position)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_button_pressed = False

            if mouse_button_pressed and object_to_place == 'square':
                new_cell = pygame.mouse.get_pos()
                cells.add_cell(new_cell)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    playing = not playing
                elif event.key == pygame.K_c:
                    cells.clear_cells()
                elif event.key == pygame.K_g:
                    cells.generate_random_cells()
                elif event.key == pygame.K_1:
                    object_to_place = 'glider' if object_to_place != 'glider' else 'square'
                elif event.key == pygame.K_2:
                    object_to_place = 'ship' if object_to_place != 'ship' else 'square'
                elif event.key == pygame.K_3:
                    object_to_place = 'pulsar' if object_to_place != 'pulsar' else 'square'
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL]\
                        and object_to_place != 'square':
                    if event.key == pygame.K_UP:
                        direction = 'up'
                    elif event.key == pygame.K_DOWN:
                        direction = 'down'
                    elif event.key == pygame.K_LEFT:
                        direction = 'left'
                    elif event.key == pygame.K_RIGHT:
                        direction = 'right'
                    else:
                        direction = 'random'

        window.fill(BLACK)
        cells.draw_cells(WHITE)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
