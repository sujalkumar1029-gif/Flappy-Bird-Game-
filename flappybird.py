import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Fixed dimensions for mobile - standard phone aspect ratio
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Game settings optimized for mobile screen
GRAVITY = 0.3
JUMP_STRENGTH = -7
PIPE_SPEED = 2
PIPE_GAP = 180
PIPE_WIDTH = 52

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 12
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x + 4), int(self.y - 4)), 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 350)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.height), 2)
        
        # Bottom pipe  
        bottom_y = self.height + PIPE_GAP
        bottom_height = SCREEN_HEIGHT - bottom_y
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y, PIPE_WIDTH, bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, bottom_height), 2)
        
    def collides_with(self, bird):
        if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + PIPE_WIDTH:
            if bird.y - bird.radius < self.height or bird.y + bird.radius > self.height + PIPE_GAP:
                return True
        return False

def main():
    # Create screen with exact dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    clock = pygame.time.Clock()
    
    # Font for mobile
    font = pygame.font.Font(None, 28)
    big_font = pygame.font.Font(None, 36)
    
    # Game objects
    bird = Bird()
    pipes = []
    score = 0
    game_over = False
    
    # Pipe spawn timer
    pipe_spawn_timer = 0
    PIPE_SPAWN_TIME = 80
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP]:
                    if not game_over:
                        bird.jump()
                    else:
                        # Reset game
                        bird = Bird()
                        pipes = []
                        score = 0
                        game_over = False
                        pipe_spawn_timer = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    bird.jump()
                else:
                    # Reset game
                    bird = Bird()
                    pipes = []
                    score = 0
                    game_over = False
                    pipe_spawn_timer = 0
        
        if not game_over:
            bird.update()
            
            # Check boundaries
            if bird.y + bird.radius >= SCREEN_HEIGHT or bird.y - bird.radius <= 0:
                game_over = True
            
            # Spawn pipes
            pipe_spawn_timer += 1
            if pipe_spawn_timer >= PIPE_SPAWN_TIME:
                pipes.append(Pipe(SCREEN_WIDTH))
                pipe_spawn_timer = 0
            
            # Update pipes
            for pipe in pipes[:]:
                pipe.update()
                
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                
                if pipe.collides_with(bird):
                    game_over = True
                
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1
        
        # Draw everything
        screen.fill(BLUE)
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen)
        
        # Draw bird
        bird.draw(screen)
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = big_font.render('GAME OVER', True, RED)
            score_final = font.render(f'Final Score: {score}', True, WHITE)
            restart_text = font.render('Tap to Restart', True, WHITE)
            
            # Center text
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            score_rect = score_final.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_final, score_rect)
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
