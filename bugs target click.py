import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (101, 67, 33)
DARK_BROWN = (76, 47, 21)

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bug Clicker Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

class Bug:
    def __init__(self, bug_type, x, y):
        self.type = bug_type
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        
        if bug_type == "ant":
            self.size = 15
            self.points = 1
            self.color = (139, 69, 19)
        elif bug_type == "beetle":
            self.size = 25
            self.points = 2
            self.color = (0, 0, 0)
        else:  # ladybug
            self.size = 20
            self.points = 3
            self.color = (220, 20, 60)
            # Ladybugs move faster, making them harder to click
            self.speed_x *= 2
            self.speed_y *= 2
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off walls
        if self.x - self.size < 0 or self.x + self.size > WIDTH:
            self.speed_x *= -1
        if self.y - self.size < 0 or self.y + self.size > HEIGHT:
            self.speed_y *= -1
        
        # Keep within bounds
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))
    
    def draw(self, surface):
        if self.type == "ant":
            # Draw ant (three circles for body)
            pygame.draw.circle(surface, self.color, (int(self.x - 8), int(self.y)), 4)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)
            pygame.draw.circle(surface, self.color, (int(self.x + 8), int(self.y)), 4)
            # Antennae
            pygame.draw.line(surface, self.color, (int(self.x - 8), int(self.y)), 
                           (int(self.x - 12), int(self.y - 6)), 2)
            pygame.draw.line(surface, self.color, (int(self.x - 8), int(self.y)), 
                           (int(self.x - 12), int(self.y + 6)), 2)
        
        elif self.type == "beetle":
            # Draw beetle (oval body)
            pygame.draw.ellipse(surface, self.color, 
                              (self.x - self.size, self.y - self.size//1.5, 
                               self.size * 2, self.size * 1.3))
            # Head
            pygame.draw.circle(surface, self.color, (int(self.x - self.size), int(self.y)), 8)
            # Shell line
            pygame.draw.line(surface, (50, 50, 50), (int(self.x), int(self.y - self.size//1.5)), 
                           (int(self.x), int(self.y + self.size//1.5)), 2)
        
        else:  # ladybug
            # Draw ladybug (red circle with spots)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            # Head (black) - made bigger
            pygame.draw.circle(surface, BLACK, (int(self.x - self.size//1.3), int(self.y)), 9)
            # Black spots - made bigger
            pygame.draw.circle(surface, BLACK, (int(self.x - 6), int(self.y - 6)), 5)
            pygame.draw.circle(surface, BLACK, (int(self.x + 6), int(self.y - 6)), 5)
            pygame.draw.circle(surface, BLACK, (int(self.x - 6), int(self.y + 6)), 5)
            pygame.draw.circle(surface, BLACK, (int(self.x + 6), int(self.y + 6)), 5)
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 4)
    
    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2)
        return distance <= self.size

def draw_background(surface):
    # Create dirt and rocks background
    surface.fill(BROWN)
    
    # Add texture with darker brown patches
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(20, 60)
        darkness = random.randint(0, 30)
        color = (BROWN[0] - darkness, BROWN[1] - darkness, BROWN[2] - darkness)
        pygame.draw.circle(surface, color, (x, y), size)
    
    # Add rocks
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(10, 30)
        # Gray rocks
        gray = random.randint(80, 140)
        pygame.draw.circle(surface, (gray, gray, gray), (x, y), size)
        # Add highlight to rocks
        pygame.draw.circle(surface, (gray + 30, gray + 30, gray + 30), 
                         (x - size//3, y - size//3), size//3)

def spawn_bug():
    # Spawn rates: 50% ants, 25% beetles, 25% ladybugs (more ladybugs!)
    rand = random.random()
    if rand < 0.5:
        bug_type = "ant"
    elif rand < 0.75:
        bug_type = "beetle"
    else:
        bug_type = "ladybug"
    
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    return Bug(bug_type, x, y)

def main():
    # Create static background
    background = pygame.Surface((WIDTH, HEIGHT))
    draw_background(background)
    
    bugs = []
    score = 0
    spawn_timer = 0
    spawn_delay = 60  # Spawn a new bug every 60 frames (1 second at 60 FPS)
    
    # Start with more bugs including more ladybugs
    for _ in range(3):
        bugs.append(spawn_bug())
    # Add extra ladybugs at start
    for _ in range(3):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        bugs.append(Bug("ladybug", x, y))
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check clicks from last to first (top to bottom)
                for bug in reversed(bugs):
                    if bug.is_clicked(mouse_pos):
                        score += bug.points
                        bugs.remove(bug)
                        break
        
        # Update bugs
        for bug in bugs:
            bug.update()
        
        # Spawn new bugs
        spawn_timer += 1
        if spawn_timer >= spawn_delay and len(bugs) < 15:
            bugs.append(spawn_bug())
            spawn_timer = 0
        
        # Draw everything
        screen.blit(background, (0, 0))
        
        for bug in bugs:
            bug.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_bg = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10))
        score_bg.fill(BLACK)
        score_bg.set_alpha(180)
        screen.blit(score_bg, (10, 10))
        screen.blit(score_text, (20, 15))
        
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()