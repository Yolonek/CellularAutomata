import pygame
from Cells import Cells, evolve_grid
from time import time


BLACK = (16, 16, 16)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
CELL_UPDATE_FREQUENCY = 10
FPS = 60
CAPTION = "Cellular Automata"


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    playing = False
    mouse_button_pressed = False
    count = 0
    generation_time = CELL_UPDATE_FREQUENCY / FPS

    cells = Cells(window, WIDTH, HEIGHT, CELL_SIZE)
    # evolve_grid({(0, 0)}, 1, 1)

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
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_button_pressed = False

            if mouse_button_pressed:
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

        window.fill(BLACK)
        cells.draw_cells(WHITE)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
