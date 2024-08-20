import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.is_jumping = False

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_strength
            self.is_jumping = True

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    player = Player()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    all_sprites.add(player)

    platform1 = Platform(200, 450, 300, 20)
    platform2 = Platform(500, 300, 200, 20)

    all_sprites.add(platform1)
    all_sprites.add(platform2)

    platforms.add(platform1)
    platforms.add(platform2)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.speed_x > 0:
                    player.stop()

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.rect.bottom = hits[0].rect.top
            player.speed_y = 0
            player.is_jumping = False

        screen.fill(BLUE)
        all_sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
