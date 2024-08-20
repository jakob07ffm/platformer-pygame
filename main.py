import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Platformer Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

font = pygame.font.SysFont(None, 36)

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
        self.is_facing_right = True
        self.scroll_offset = 0
        self.health = 3
        self.score = 0

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
            self.is_jumping = False

        if self.rect.left < 200:
            self.rect.left = 200
            self.scroll_offset = self.speed_x
        elif self.rect.right > WIDTH - 200:
            self.rect.right = WIDTH - 200
            self.scroll_offset = self.speed_x
        else:
            self.scroll_offset = 0

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_strength
            self.is_jumping = True

    def move_left(self):
        self.speed_x = -5
        self.is_facing_right = False

    def move_right(self):
        self.speed_x = 5
        self.is_facing_right = True

    def stop(self):
        self.speed_x = 0

    def lose_health(self):
        self.health -= 1
        if self.health <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

    def collect_coin(self, coin):
        self.score += 1
        coin.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, offset):
        self.rect.x -= offset

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = random.choice([-3, 3])

    def update(self, offset):
        self.rect.x += self.speed_x - offset
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1

        if random.random() < 0.01:
            self.speed_x *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, offset):
        self.rect.x -= offset

def generate_platforms():
    platforms = []
    y = 450
    for i in range(5):
        x = random.randint(0, WIDTH - 200)
        width = random.randint(100, 300)
        platform = Platform(x, y, width, 20)
        platforms.append(platform)
        y -= random.randint(80, 150)
    return platforms

def generate_coins(platforms):
    coins = []
    for platform in platforms:
        if random.random() < 0.5:
            coin = Coin(platform.rect.centerx, platform.rect.y - 30)
            coins.append(coin)
    return coins

def draw_health(screen, player):
    for i in range(player.health):
        pygame.draw.rect(screen, RED, (10 + i * 40, 10, 30, 30))

def draw_score(screen, player):
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

def main():
    player = Player()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    all_sprites.add(player)

    initial_platforms = generate_platforms()
    for platform in initial_platforms:
        platforms.add(platform)
        all_sprites.add(platform)

    initial_coins = generate_coins(initial_platforms)
    for coin in initial_coins:
        coins.add(coin)
        all_sprites.add(coin)

    for _ in range(3):
        enemy = Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2))
        enemies.add(enemy)
        all_sprites.add(enemy)

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

        player_collide = pygame.sprite.spritecollide(player, platforms, False)
        if player_collide:
            player.rect.bottom = player_collide[0].rect.top
            player.speed_y = 0
            player.is_jumping = False

        if pygame.sprite.spritecollideany(player, enemies):
            player.lose_health()

        for platform in platforms:
            platform.update(player.scroll_offset)
            if platform.rect.right < 0:
                platform.kill()
                new_platform = Platform(WIDTH, random.randint(100, HEIGHT - 100), random.randint(100, 300), 20)
                platforms.add(new_platform)
                all_sprites.add(new_platform)

        for coin in coins:
            coin.update(player.scroll_offset)
            if pygame.sprite.collide_rect(player, coin):
                player.collect_coin(coin)

        for enemy in enemies:
            enemy.update(player.scroll_offset)

        screen.fill(BLUE)
        all_sprites.draw(screen)
        draw_health(screen, player)
        draw_score(screen, player)
        pygame.display.flip()

if __name__ == "__main__":
    main()
