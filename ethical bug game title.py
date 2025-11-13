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
medium_font = pygame.font.Font(None, 36)

def desaturate_color(color, intensity):
    """Reduce color intensity, moving towards gray"""
    # intensity ranges from 0 (full color) to 1 (gray)
    r, g, b = color
    gray = (r + g + b) / 3
    new_r = int(r + (gray - r) * intensity)
    new_g = int(g + (gray - g) * intensity)
    new_b = int(b + (gray - b) * intensity)
    return (new_r, new_g, new_b)

class Bug:
    def __init__(self, bug_type, x, y, color_intensity=0):
        self.type = bug_type
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.color_intensity = color_intensity
        
        if bug_type == "ant":
            self.size = 44
            self.points = 1
            base_color = (139, 69, 19)
            self.color = desaturate_color(base_color, color_intensity)
        elif bug_type == "beetle":
            self.size = 25
            self.points = 2
            base_color = (0, 0, 0)
            self.color = desaturate_color(base_color, color_intensity)
        else:  # ladybug
            self.size = 20
            self.points = 3
            base_color = (220, 20, 60)
            self.color = desaturate_color(base_color, color_intensity)
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
            shell_color = desaturate_color((50, 50, 50), self.color_intensity)
            pygame.draw.line(surface, shell_color, (int(self.x), int(self.y - self.size//1.5)), 
                           (int(self.x), int(self.y + self.size//1.5)), 2)
        
        else:  # ladybug
            # Draw ladybug (red circle with spots)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            # Head (black)
            head_color = desaturate_color(BLACK, self.color_intensity)
            pygame.draw.circle(surface, head_color, (int(self.x - self.size//1.3), int(self.y)), 9)
            # Black spots
            pygame.draw.circle(surface, head_color, (int(self.x - 6), int(self.y - 6)), 5)
            pygame.draw.circle(surface, head_color, (int(self.x + 6), int(self.y - 6)), 5)
            pygame.draw.circle(surface, head_color, (int(self.x - 6), int(self.y + 6)), 5)
            pygame.draw.circle(surface, head_color, (int(self.x + 6), int(self.y + 6)), 5)
            pygame.draw.circle(surface, head_color, (int(self.x), int(self.y)), 4)
    
    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2)
        return distance <= self.size

def draw_background(surface, color_intensity=0):
    # Create dirt and rocks background with desaturated colors
    brown = desaturate_color(BROWN, color_intensity)
    surface.fill(brown)
    
    # Add texture with darker brown patches
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(20, 60)
        darkness = random.randint(0, 30)
        color = (brown[0] - darkness, brown[1] - darkness, brown[2] - darkness)
        pygame.draw.circle(surface, color, (x, y), size)
    
    # Add rocks
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(10, 30)
        # Gray rocks
        gray = random.randint(80, 140)
        rock_color = desaturate_color((gray, gray, gray), color_intensity)
        pygame.draw.circle(surface, rock_color, (x, y), size)
        # Add highlight to rocks
        highlight = desaturate_color((gray + 30, gray + 30, gray + 30), color_intensity)
        pygame.draw.circle(surface, highlight, (x - size//3, y - size//3), size//3)

def spawn_bug(color_intensity):
    # Spawn rates: 50% ants, 25% beetles, 25% ladybugs
    rand = random.random()
    if rand < 0.5:
        bug_type = "ant"
    elif rand < 0.75:
        bug_type = "beetle"
    else:
        bug_type = "ladybug"
    
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    return Bug(bug_type, x, y, color_intensity)

def draw_pause_screen(surface):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(200)
    surface.blit(overlay, (0, 0))
    
    # Pause text
    pause_text = font.render("PAUSED", True, WHITE)
    resume_text = medium_font.render("Press SPACE to Resume", True, WHITE)
    
    surface.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 60))
    surface.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2 + 20))

def draw_break_prompt(surface):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(200)
    surface.blit(overlay, (0, 0))
    
    # Break prompt text
    prompt_text = medium_font.render("You've reached 15 points!", True, WHITE)
    question_text = medium_font.render("Would you like a break?", True, WHITE)
    yes_text = small_font.render("Press Y for Yes", True, (100, 255, 100))
    no_text = small_font.render("Press N to Continue", True, (255, 100, 100))
    
    surface.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 - 80))
    surface.blit(question_text, (WIDTH//2 - question_text.get_width()//2, HEIGHT//2 - 30))
    surface.blit(yes_text, (WIDTH//2 - yes_text.get_width()//2, HEIGHT//2 + 30))
    surface.blit(no_text, (WIDTH//2 - no_text.get_width()//2, HEIGHT//2 + 70))

def draw_win_screen(surface, score):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((50, 50, 50))
    overlay.set_alpha(230)
    surface.blit(overlay, (0, 0))
    
    # Win text
    win_text = font.render("YOU WIN!", True, (255, 215, 0))
    score_text = medium_font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("Press R to Restart or Q to Quit", True, WHITE)
    
    surface.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 80))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 10))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

def draw_start_screen(surface):
    # Background
    surface.fill((40, 80, 40))  # Dark green background
    
    # Title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("BUG COLLECTING", True, (255, 255, 100))
    surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 80))
    
    # Instructions
    instructions = [
        "How to Play:",
        "",
        "Click on bugs to collect them!",
        "Ants = 1 point",
        "Beetles = 2 points",
        "Ladybugs = 3 points (fast!)",
        "",
        "Reach 30 points to win!",
        "Press SPACE to pause anytime",
        "",
        "Colors fade as you collect..."
    ]
    
    y_offset = 200
    for line in instructions:
        if line == "How to Play:":
            text = medium_font.render(line, True, WHITE)
        else:
            text = small_font.render(line, True, (200, 255, 200))
        surface.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
        y_offset += 35
    
    # Start button
    button_width, button_height = 200, 60
    button_x = WIDTH//2 - button_width//2
    button_y = HEIGHT - 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Button background
    pygame.draw.rect(surface, (100, 200, 100), button_rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, button_rect, 3, border_radius=10)
    
    # Button text
    button_text = medium_font.render("START", True, WHITE)
    surface.blit(button_text, (WIDTH//2 - button_text.get_width()//2, button_y + 15))
    
    return button_rect

def main():
    game_started = False
    bugs = []
    score = 0
    spawn_timer = 0
    spawn_delay = 60
    paused = False
    break_prompted = False
    game_won = False
    
    # Calculate initial color intensity
    color_intensity = 0
    
    # Create initial background
    background = pygame.Surface((WIDTH, HEIGHT))
    draw_background(background, color_intensity)
    
    running = True
    start_button_rect = None
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle start screen clicks
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect and start_button_rect.collidepoint(mouse_pos):
                    game_started = True
                    # Initialize bugs when game starts
                    for _ in range(3):
                        bugs.append(spawn_bug(color_intensity))
                    for _ in range(3):
                        x = random.randint(50, WIDTH - 50)
                        y = random.randint(50, HEIGHT - 50)
                        bugs.append(Bug("ladybug", x, y, color_intensity))
            
            if event.type == pygame.KEYDOWN:
                # Pause/Resume with SPACE
                if event.key == pygame.K_SPACE and not break_prompted and not game_won and game_started:
                    paused = not paused
                
                # Break prompt response
                if break_prompted:
                    if event.key == pygame.K_y:
                        paused = True
                        break_prompted = False
                    elif event.key == pygame.K_n:
                        break_prompted = False
                
                # Win screen controls
                if game_won:
                    if event.key == pygame.K_r:
                        # Restart game
                        bugs = []
                        score = 0
                        spawn_timer = 0
                        paused = False
                        break_prompted = False
                        game_won = False
                        game_started = False
                        color_intensity = 0
                        background = pygame.Surface((WIDTH, HEIGHT))
                        draw_background(background, color_intensity)
                    elif event.key == pygame.K_q:
                        running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not paused and not break_prompted and not game_won and game_started:
                mouse_pos = pygame.mouse.get_pos()
                for bug in reversed(bugs):
                    if bug.is_clicked(mouse_pos):
                        score += bug.points
                        bugs.remove(bug)
                        
                        # Update color intensity (max desaturation at 30 points)
                        color_intensity = min(score / 30.0, 1.0)
                        
                        # Redraw background with new color intensity
                        background = pygame.Surface((WIDTH, HEIGHT))
                        draw_background(background, color_intensity)
                        
                        # Check for break prompt
                        if score == 15 and not break_prompted:
                            break_prompted = True
                        
                        # Check for win
                        if score >= 30:
                            game_won = True
                        
                        break
        
        # Update game state only if not paused
        if not paused and not break_prompted and not game_won and game_started:
            # Update bugs
            for bug in bugs:
                bug.update()
            
            # Spawn new bugs with current color intensity
            spawn_timer += 1
            if spawn_timer >= spawn_delay and len(bugs) < 15:
                bugs.append(spawn_bug(color_intensity))
                spawn_timer = 0
        
        # Draw everything
        if not game_started:
            # Draw start screen
            start_button_rect = draw_start_screen(screen)
        else:
            # Draw game
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
            
            # Draw pause indicator
            if paused and not break_prompted:
                draw_pause_screen(screen)
            
            # Draw break prompt
            if break_prompted:
                draw_break_prompt(screen)
            
            # Draw win screen
            if game_won:
                draw_win_screen(screen, score)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()