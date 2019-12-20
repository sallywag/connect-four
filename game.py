import sys
import itertools
from typing import Optional, List

import pygame

import inputmanager


class Game:

    def __init__(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.fps = 30
        window_size = (640, 480)
        self.displaysurf = pygame.display.set_mode(window_size)
        self.cell_size = (64, 64)
        self.rect_locations = (16, 80, 144, 208, 272, 336, 400)
        self.grid = []
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.column_rects = [
            pygame.Rect(16, 16, 64, 448),
            pygame.Rect(80, 16, 64, 448),
            pygame.Rect(144, 16, 64, 448),
            pygame.Rect(208, 16, 64, 448),
            pygame.Rect(272, 16, 64, 448),
            pygame.Rect(336, 16, 64, 448),
            pygame.Rect(400, 16, 64, 448),
        ]
        self.refresh_button_rect = pygame.Rect(480, 16, 128, 64)
        self.red_score_rect = pygame.Rect(480, 144, 64, 64)
        self.blue_score_rect = pygame.Rect(544, 144, 64, 64)
        self.rect_to_highlight = None
        self.current_players_disk_color = self.red
        self.red_score = 0
        self.blue_score = 0
        self.game_over = False
        pygame.display.set_caption("Connect Four")

    def main(self) -> None:
        self.get_grid()
        while True:
            self.get_input()
            self.handle_input()
            self.render()
            self.fps_clock.tick(self.fps)

    def get_grid(self) -> None:
        self.grid = []
        for column, x in enumerate(self.rect_locations):
            self.grid.append([])
            for y in self.rect_locations:
                self.grid[column].append(
                    {"color": self.black, "rect": pygame.Rect((x, y), self.cell_size)}
                )

    def get_input(self) -> None:
        inputmanager.InputManager.get_events()
        inputmanager.InputManager.check_for_quit_event()
        inputmanager.InputManager.update_keyboard_key_state()
        inputmanager.InputManager.get_keyboard_input()
        inputmanager.InputManager.update_mouse_button_state()
        inputmanager.InputManager.get_mouse_input()

    def handle_input(self) -> None:
        if inputmanager.InputManager.quit:
            self.terminate()
        self.rect_to_highlight = None
        for column_rect, column in zip(self.column_rects, self.grid):
            if column_rect.collidepoint(inputmanager.InputManager.cursor_location):
                if (
                    inputmanager.InputManager.mouse[1]
                    == inputmanager.InputManager.pressed
                    and not self.game_over
                ):
                    if not self.column_full(column):
                        self.drop_disk_in_column(column)
                        disks = self.four_in_a_row()
                        if disks is not None:
                            self.color_disks_green(disks)
                            self.increment_score()
                            self.game_over = True
                        self.swap_current_players_disk_color()
                self.rect_to_highlight = column_rect
                break
        else:
            if self.refresh_button_rect.collidepoint(
                inputmanager.InputManager.cursor_location
            ):
                if (
                    inputmanager.InputManager.mouse[1]
                    == inputmanager.InputManager.pressed
                ):
                    self.get_grid()
                    self.game_over = False
                self.rect_to_highlight = self.refresh_button_rect

    def terminate(self) -> None:
        pygame.quit()
        sys.exit()

    def column_full(self, column: List) -> bool:
        for disk in column:
            if disk["color"] == self.black:
                return False
        return True

    def drop_disk_in_column(self, column: List) -> None:
        for disk in reversed(column):
            if disk["color"] == self.black:
                disk["color"] = self.current_players_disk_color
                break

    def four_in_a_row(self) -> Optional[List]:
        for function in [
            self.four_in_a_row_horizontal,
            self.four_in_a_row_vertical,
            self.four_in_a_row_diagonal_descending,
            self.four_in_a_row_diagonal_ascending,
        ]:
            disks = function()
            if disks is not None:
                return disks
        return None

    def four_in_a_row_horizontal(self) -> Optional[List]:
        for row in range(len(self.grid)):
            disks = []
            for column in self.grid:
                disks.append(column[row])
                if (
                    disks[-1]["color"] == self.black
                    or len(disks) >= 2
                    and disks[-1]["color"] != disks[-2]["color"]
                ):
                    disks = [column[row]]
                if len(disks) == 4:
                    return disks
        return None

    def four_in_a_row_vertical(self) -> Optional[List]:
        for row, column in itertools.product(range(4), self.grid):
            disks = column[row : 4 + row]
            disk_colors = {disk["color"] for disk in disks}
            if len(disk_colors) == 1 and self.black not in disk_colors:
                return disks
        return None

    def four_in_a_row_diagonal_descending(self) -> Optional[List]:
        disks = []
        for x, y in itertools.product(range(4), range(4)):
            for column, row in zip(
                self.grid[0 + y : 4 + y], itertools.cycle(range(0 + x, 4 + x))
            ):
                disks.append(column[row])
                if len(disks) == 4:
                    disk_colors = {disk["color"] for disk in disks}
                    if self.black not in disk_colors and len(disk_colors) == 1:
                        return disks
                    disks = []
        return None

    def four_in_a_row_diagonal_ascending(self) -> Optional[List]:
        disks = []
        for x, y in itertools.product(range(4), range(4)):
            for column, row in zip(
                self.grid[0 + y : 4 + y], itertools.cycle(reversed(range(0 + x, 4 + x)))
            ):
                disks.append(column[row])
                if len(disks) == 4:
                    disk_colors = {disk["color"] for disk in disks}
                    if self.black not in disk_colors and len(disk_colors) == 1:
                        return disks
                    disks = []
        return None

    def color_disks_green(self, disks: List) -> None:
        for disk in disks:
            disk["color"] = self.green

    def increment_score(self) -> None:
        if self.current_players_disk_color == self.red:
            self.red_score += 1
        else:
            self.blue_score += 1

    def swap_current_players_disk_color(self) -> None:
        if self.current_players_disk_color == self.red:
            self.current_players_disk_color = self.blue
        else:
            self.current_players_disk_color = self.red

    def render(self) -> None:
        self.draw_grid()
        self.draw_refresh_button_rect()
        self.draw_score()
        if self.rect_to_highlight is not None:
            self.highlight_rect(self.rect_to_highlight)
        self.draw_refresh_button_text()
        self.draw_disks()
        pygame.display.update()

    def draw_grid(self) -> None:
        for coulmn_rect in self.column_rects:
            pygame.draw.rect(self.displaysurf, self.yellow, coulmn_rect)

    def draw_refresh_button_rect(self) -> None:
        pygame.draw.rect(self.displaysurf, self.yellow, self.refresh_button_rect)

    def draw_score(self) -> None:
        font = pygame.font.Font(None, 24)
        red_score_text = font.render(str(self.red_score), True, self.yellow)
        blue_score_text = font.render(str(self.blue_score), True, self.yellow)
        pygame.draw.rect(self.displaysurf, self.red, self.red_score_rect)
        pygame.draw.rect(self.displaysurf, self.blue, self.blue_score_rect)
        self.displaysurf.blit(
            red_score_text,
            (
                self.red_score_rect.centerx
                - self.red_score_rect.centerx / self.red_score_rect.y,
                self.red_score_rect.centery
                - self.red_score_rect.centery / self.red_score_rect.x,
            ),
        )
        self.displaysurf.blit(
            blue_score_text,
            (
                self.blue_score_rect.centerx
                - self.blue_score_rect.centerx / self.blue_score_rect.y,
                self.blue_score_rect.centery
                - self.blue_score_rect.centery / self.blue_score_rect.x,
            ),
        )

    def highlight_rect(self, rect: pygame.Rect) -> None:
        pygame.draw.rect(self.displaysurf, self.current_players_disk_color, rect)

    def draw_refresh_button_text(self) -> None:
        font = pygame.font.Font(None, 24)
        text = font.render("Refresh", True, self.black)
        self.displaysurf.blit(
            text,
            (
                self.refresh_button_rect.centerx
                - self.refresh_button_rect.centerx / self.refresh_button_rect.y,
                self.refresh_button_rect.centery
                - self.refresh_button_rect.centery / self.refresh_button_rect.x,
            ),
        )

    def draw_disks(self) -> None:
        for column in self.grid:
            for disk in column:
                pygame.draw.ellipse(self.displaysurf, disk["color"], disk["rect"])


if __name__ == "__main__":
    Game().main()
