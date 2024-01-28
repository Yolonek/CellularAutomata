import pygame
from Cells import Cells
from time import time


BLACK = (16, 16, 16)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 800
CELL_SIZE_LIST = [1, 2, 4, 8, 10, 20]
UPDATE_FREQUENCY_LIST = [2, 3, 5, 10, 20, 30, 60]
FPS = 60
CAPTION = "Conway's Game of Life"

# Press 1 to place glider
# press 2 to place ship
# press 3 to place pulsar
# press one of arrows to choose direction of the glider/ship
# press P to toggle logs printing
# press E to enter edit mode and change speed and size with arrows


def get_neighboring_number(current_number: int, number_list: list[int], increment: bool) -> int:
    if current_number in number_list:
        current_number_index = number_list.index(current_number)
        try:
            if increment:
                return number_list[current_number_index + 1]
            else:
                if current_number_index - 1 >= 0:
                    return number_list[current_number_index - 1]
                else:
                    return number_list[0]
        except IndexError:
            return current_number


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    playing = False
    print_logs = False
    edit_mode_active = False
    mouse_button_pressed = False
    object_to_place = 'square'
    count = 0
    current_cell_size = CELL_SIZE_LIST[-1]
    current_update_frequency = UPDATE_FREQUENCY_LIST[-1]
    generation_time = current_update_frequency / FPS

    cells = Cells(window, WIDTH, HEIGHT, current_cell_size)

    direction = 'random'
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        if count >= current_update_frequency:
            count = 0
            start = time()
            cells.new_generation()
            if print_logs:
                print(f'Generation time: {time() - start:.4f} s, '
                      f'Generation refresh time: {generation_time:.4f} s, '
                      f'Number of cells: {cells.get_number_of_cells()}')

        pygame.display.set_caption(f'{CAPTION} - {"Playing" if playing else "Paused"}'
                                   f' (s: {current_cell_size}, f: {current_update_frequency})')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not edit_mode_active:
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
                elif event.key == pygame.K_p:
                    print_logs = not print_logs
                elif event.key == pygame.K_e:
                    edit_mode_active = not edit_mode_active
                    print(f'edit_mode_active: {edit_mode_active}')
                elif event.key == pygame.K_c:
                    cells.clear_cells()
                elif event.key == pygame.K_g:
                    cells.generate_random_cells()
                elif event.key == pygame.K_1:
                    object_to_place = 'glider' if object_to_place != 'glider' else 'square'
                    print(f'placing {object_to_place}')
                elif event.key == pygame.K_2:
                    object_to_place = 'ship' if object_to_place != 'ship' else 'square'
                    print(f'placing {object_to_place}')
                elif event.key == pygame.K_3:
                    object_to_place = 'pulsar' if object_to_place != 'pulsar' else 'square'
                    print(f'placing {object_to_place}')
                elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL]:
                    if object_to_place != 'square' and not edit_mode_active:
                        if event.key == pygame.K_UP:
                            direction = 'up' if direction != 'up' else 'random'
                        elif event.key == pygame.K_DOWN:
                            direction = 'down' if direction != 'down' else 'random'
                        elif event.key == pygame.K_LEFT:
                            direction = 'left' if direction != 'left' else 'random'
                        elif event.key == pygame.K_RIGHT:
                            direction = 'right' if direction == 'right' else 'random'
                        else:
                            direction = 'random'
                    if edit_mode_active and object_to_place == 'square':
                        if event.key == pygame.K_UP:
                            current_cell_size = get_neighboring_number(current_cell_size, CELL_SIZE_LIST, True)
                            cells.change_cell_size(current_cell_size)
                        elif event.key == pygame.K_DOWN:
                            current_cell_size = get_neighboring_number(current_cell_size, CELL_SIZE_LIST, False)
                            cells.change_cell_size(current_cell_size)
                        elif event.key == pygame.K_LEFT:
                            current_update_frequency = get_neighboring_number(
                                current_update_frequency, UPDATE_FREQUENCY_LIST, False
                            )
                            generation_time = current_update_frequency / FPS
                        elif event.key == pygame.K_RIGHT:
                            current_update_frequency = get_neighboring_number(
                                current_update_frequency, UPDATE_FREQUENCY_LIST, True
                            )
                            generation_time = current_update_frequency / FPS
                        print(f'current cell size: {current_cell_size}\n'
                              f'current generation time: {generation_time}')

        window.fill(BLACK)
        cells.draw_cells(WHITE)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
