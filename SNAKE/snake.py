import pygame
import random
import sys

pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

block_size = 20

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

class Snake:
    def __init__(self):
        self.length = 5  
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.head_color = RED
        self.body_color = GREEN
        self.score = 0
        self.speed = 10  
        self.frame_count = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * block_size)) % width), (cur[1] + (y * block_size)) % height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 5
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = 10
        self.frame_count = 0

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            if i == 0:  
                pygame.draw.rect(surface, self.head_color, (p[0], p[1], block_size, block_size))
                pygame.draw.rect(surface, WHITE, (p[0], p[1], block_size, block_size), 1)
            else:
                pygame.draw.rect(surface, self.body_color, (p[0], p[1], block_size, block_size))
                pygame.draw.rect(surface, WHITE, (p[0], p[1], block_size, block_size), 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Ball:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.radius = 10
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (width - block_size) // block_size) * block_size,
                         random.randint(0, (height - block_size) // block_size) * block_size)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.position[0] + block_size // 2, self.position[1] + block_size // 2), self.radius)

class Menu:
    def __init__(self):
        self.play_button = pygame.Rect(width // 2 - 100, height // 2 - 30, 200, 50)
        self.quit_button = pygame.Rect(width // 2 - 100, height // 2 + 40, 200, 50)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.play_button)
        pygame.draw.rect(surface, RED, self.quit_button)

        play_text = font.render("Jouer", True, WHITE)
        quit_text = font.render("Quitter", True, WHITE)

        surface.blit(play_text, (width // 2 - play_text.get_width() // 2, height // 2 - 15))
        surface.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 55))


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    snake = Snake()
    ball = Ball()
    menu = Menu()
    in_menu = True
    best_score = 0  

    while True:
        clock.tick(snake.speed)

        if in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.play_button.collidepoint(event.pos):
                        in_menu = False
                    elif menu.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            win.fill((0, 0, 0))
            menu.draw(win)
        else:
            snake.handle_keys()
            if snake.move():
                in_menu = True
                best_score = max(best_score, snake.score)
                snake.reset()
                continue

            snake.frame_count += 1

            if snake.get_head_position() == ball.position:
                snake.length += 1
                snake.score += 1
                ball.randomize_position()
                snake.speed += 1  
                snake.frame_count = 0  

            if snake.frame_count == snake.speed:
                if snake.length > 5:
                    snake.positions.pop()
                snake.frame_count = 0

            win.fill((0, 0, 0))
            snake.draw(win)
            ball.draw(win)

            # Afficher le score
            score_text = font.render(f"Score: {snake.score}", True, WHITE)
            win.blit(score_text,
 (10, 10))
            best_score_text = font.render(f"Best Score: {best_score}", True, WHITE)
            win.blit(best_score_text, (10, 40))

        pygame.display.update()

if __name__ == "__main__":
    main()