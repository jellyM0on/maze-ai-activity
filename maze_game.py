import pygame
import sys
from pygame.locals import *

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Group 3 - Mouse & Cheese Maze Adventure")

DARK_WOOD = (101, 67, 33)
LIGHT_WOOD = (196, 164, 132)
CHEESE_YELLOW = (255, 213, 70)
MOUSE_GRAY = (180, 180, 180)
GREEN_MOSS = (76, 115, 0)
BLUE_SKY = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

has_images = False

title_font = pygame.font.SysFont('Arial', 48, bold=True)
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

CELL_SIZE = min(SCREEN_WIDTH // 20, SCREEN_HEIGHT // 15)
MAZE_WIDTH = 25
MAZE_HEIGHT = 15

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,3,1],
    [1,0,1,1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

mouse_pos = [1, 1]
cheese_collected = 0
game_won = False
show_help = False

def draw_maze():
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            rect = pygame.Rect(
                x * CELL_SIZE + (SCREEN_WIDTH - MAZE_WIDTH * CELL_SIZE) // 2,
                y * CELL_SIZE + (SCREEN_HEIGHT - MAZE_HEIGHT * CELL_SIZE) // 2,
                CELL_SIZE, CELL_SIZE
            )
            if maze[y][x] == 1:
                pygame.draw.rect(screen, DARK_WOOD, rect)
                for i in range(0, CELL_SIZE, 3):
                    pygame.draw.line(
                        screen,
                        (DARK_WOOD[0]-20, DARK_WOOD[1]-20, DARK_WOOD[2]-20),
                        (rect.left, rect.top + i),
                        (rect.right, rect.top + i),
                        1
                    )
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, GREEN_MOSS, rect)
                start_text = small_font.render("START", True, WHITE)
                screen.blit(start_text, (rect.x + 5, rect.y + 15))
            elif maze[y][x] == 3:
                pygame.draw.rect(screen, LIGHT_WOOD, rect)
                points = [
                    (rect.x + 5, rect.y + 5),
                    (rect.x + CELL_SIZE - 5, rect.y + CELL_SIZE // 2),
                    (rect.x + 5, rect.y + CELL_SIZE - 5)
                ]
                pygame.draw.polygon(screen, CHEESE_YELLOW, points)
                pygame.draw.circle(screen, LIGHT_WOOD, (rect.x + 15, rect.y + 15), 4)
                pygame.draw.circle(screen, LIGHT_WOOD, (rect.x + 30, rect.y + 20), 3)
                pygame.draw.circle(screen, LIGHT_WOOD, (rect.x + 20, rect.y + 30), 4)
            else:
                pygame.draw.rect(screen, LIGHT_WOOD, rect)
                for i in range(0, CELL_SIZE, 5):
                    pygame.draw.line(
                        screen,
                        (LIGHT_WOOD[0]+20, LIGHT_WOOD[1]+20, LIGHT_WOOD[2]+20),
                        (rect.left, rect.top + i),
                        (rect.right, rect.top + i),
                        1
                    )

def draw_mouse():
    rect = pygame.Rect(
        mouse_pos[0] * CELL_SIZE + (SCREEN_WIDTH - MAZE_WIDTH * CELL_SIZE) // 2 + CELL_SIZE//2 - 20,
        mouse_pos[1] * CELL_SIZE + (SCREEN_HEIGHT - MAZE_HEIGHT * CELL_SIZE) // 2 + CELL_SIZE//2 - 20,
        40, 40
    )
    pygame.draw.ellipse(screen, MOUSE_GRAY, rect)
    pygame.draw.ellipse(screen, MOUSE_GRAY, (rect.x - 8, rect.y - 8, 16, 20))
    pygame.draw.ellipse(screen, MOUSE_GRAY, (rect.x + 32, rect.y - 8, 16, 20))
    pygame.draw.ellipse(screen, (220, 220, 220), (rect.x - 5, rect.y - 5, 10, 12))
    pygame.draw.ellipse(screen, (220, 220, 220), (rect.x + 35, rect.y - 5, 10, 12))
    pygame.draw.circle(screen, BLACK, (rect.x + 10, rect.y + 12), 3)
    pygame.draw.circle(screen, BLACK, (rect.x + 30, rect.y + 12), 3)
    pygame.draw.line(screen, BLACK, (rect.x + 8, rect.y + 20), (rect.x - 10, rect.y + 18), 1)
    pygame.draw.line(screen, BLACK, (rect.x + 8, rect.y + 23), (rect.x - 10, rect.y + 23), 1)
    pygame.draw.line(screen, BLACK, (rect.x + 32, rect.y + 20), (rect.x + 50, rect.y + 18), 1)
    pygame.draw.line(screen, BLACK, (rect.x + 32, rect.y + 23), (rect.x + 50, rect.y + 23), 1)
    pygame.draw.line(screen, MOUSE_GRAY, (rect.x + 40, rect.y + 20), (rect.x + 60, rect.y + 10), 4)

def draw_ui():
    panel = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
    panel.fill((50, 50, 50, 200))
    screen.blit(panel, (0, SCREEN_HEIGHT - 60))
    cheese_text = font.render(f"Cheese: {cheese_collected}", True, CHEESE_YELLOW)
    screen.blit(cheese_text, (20, SCREEN_HEIGHT - 45))
    controls_text = small_font.render("Arrow Keys: Move | H: Help | ESC: Quit", True, WHITE)
    screen.blit(controls_text, (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 45))
    title_text = title_font.render("Group 3 - Mouse & Cheese Maze Adventure", True, CHEESE_YELLOW)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 20))
    if game_won:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        win_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 200)
        pygame.draw.rect(screen, CHEESE_YELLOW, win_rect, border_radius=20)
        pygame.draw.rect(screen, BLACK, win_rect, 3, border_radius=20)
        win_text = title_font.render("VICTORY!", True, BLACK)
        screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
        message = font.render("You found the cheese!", True, BLACK)
        screen.blit(message, (SCREEN_WIDTH//2 - message.get_width()//2, SCREEN_HEIGHT//2 - 30))
        restart_text = font.render("Press R to play again", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
    if show_help:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        help_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 200, 600, 400)
        pygame.draw.rect(screen, LIGHT_WOOD, help_rect, border_radius=20)
        pygame.draw.rect(screen, BLACK, help_rect, 3, border_radius=20)
        title = title_font.render("HOW TO PLAY", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 180))
        instructions = [
            "Guide the mouse through the maze to find the cheese!",
            "",
            "Controls:",
            "- Arrow Keys: Move the mouse",
            "- ESC: Quit the game",
            "- H: Toggle this help screen",
            "- R: Restart after winning",
            "",
            "Tip: The walls are made of wood - don't bump into them!"
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, BLACK) if i != 2 else font.render(line, True, DARK_WOOD)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 120 + i * 40))
        close_text = font.render("Press H to close", True, DARK_WOOD)
        screen.blit(close_text, (SCREEN_WIDTH//2 - close_text.get_width()//2, SCREEN_HEIGHT//2 + 150))

def move_mouse(dx, dy):
    global mouse_pos, cheese_collected, game_won
    if game_won:
        return
    new_x = mouse_pos[0] + dx
    new_y = mouse_pos[1] + dy
    if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
        mouse_pos[0] = new_x
        mouse_pos[1] = new_y
        if maze[new_y][new_x] == 3:
            cheese_collected += 1
            game_won = True

def reset_game():
    global mouse_pos, cheese_collected, game_won
    mouse_pos = [1, 1]
    cheese_collected = 0
    game_won = False

def main():
    global show_help
    clock = pygame.time.Clock()
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(background, BLUE_SKY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT * 2 // 3))
    pygame.draw.rect(background, GREEN_MOSS, (0, SCREEN_HEIGHT * 2 // 3, SCREEN_WIDTH, SCREEN_HEIGHT // 3))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    move_mouse(0, -1)
                elif event.key == K_DOWN:
                    move_mouse(0, 1)
                elif event.key == K_LEFT:
                    move_mouse(-1, 0)
                elif event.key == K_RIGHT:
                    move_mouse(1, 0)
                elif event.key == K_r and game_won:
                    reset_game()
                elif event.key == K_h:
                    show_help = not show_help
        screen.blit(background, (0, 0))
        draw_maze()
        draw_mouse()
        draw_ui()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
