import pygame
import random
import os

# Initialize pygame
pygame.init()

# Initialize the mixer for sound
pygame.mixer.init()
pygame.mixer.music.load('tetris.mp3')  # Load the music file
pygame.mixer.music.play(-1)  # Play the music in an infinite loop

# Fullscreen mode
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
block_size = min(screen_width // 12, screen_height // 22)  # Block size based on the screen resolution

# Define the Tetris grid size
grid_width = 12  # Increased grid width
grid_height = 22  # Increased grid height

# Calculate the size and position of the game field in the center
game_width = grid_width * block_size
game_height = grid_height * block_size
game_x_offset = (screen_width - game_width) // 2
game_y_offset = (screen_height - game_height) // 2

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Tetris")

# Load the background image
background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))  # Scale to fit the screen

# Fonts
font = pygame.font.SysFont("comicsans", 40)  # Slightly larger font
large_font = pygame.font.SysFont("comicsans", 60)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (200, 200, 200)
highlight_color = (100, 100, 100)  # Border color for the grid

# Define colors for each shape
shape_colors = [
    (0, 255, 255),  # I
    (255, 165, 0),  # O
    (0, 0, 255),    # T
    (255, 0, 0),    # L
    (0, 255, 0),    # J
    (128, 0, 128),  # S
    (255, 255, 0)   # Z
]

# Shapes of the blocks (Tetrominoes)
shapes = [
    [[1, 1, 1, 1]],               # I shape
    [[1, 1], [1, 1]],             # O shape
    [[0, 1, 1], [1, 1, 0]],       # S shape
    [[1, 1, 0], [0, 1, 1]],       # Z shape
    [[1, 1, 1], [0, 1, 0]],       # T shape
    [[1, 1, 1], [1, 0, 0]],       # L shape
    [[1, 1, 1], [0, 0, 1]],       # J shape
]

# Load highscore from file
def load_highscore():
    if os.path.exists("Highscore Tetris.txt"):
        with open("Highscore Tetris.txt", "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    return 0

# Save highscore to file
def save_highscore(score):
    with open("Highscore Tetris.txt", "w") as file:
        file.write(str(score))

# Block class to represent each falling piece
class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = grid_width // 2 - len(shape[0]) // 2  # Center the block horizontally
        self.y = 0  # Start at the top

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Check if the block position is valid
def valid_move(block, grid, dx=0, dy=0):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = block.x + x + dx
                new_y = block.y + y + dy
                if new_x < 0 or new_x >= grid_width or new_y >= grid_height:
                    return False
                if new_y >= 0 and grid[new_y][new_x]:
                    return False
    return True

# Add block to grid when it lands
def add_to_grid(block, grid):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[block.y + y][block.x + x] = block.color

# Clear complete rows and return the number of cleared rows
def clear_rows(grid):
    cleared = 0
    for y in range(len(grid)):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0 for _ in range(grid_width)])  # Add an empty row at the top
            cleared += 1
    return cleared

# Draw the grid and the block
def draw_grid(screen, grid, block, next_block, score, highscore):
    # Draw the background image
    screen.blit(background_img, (0, 0))

    # Draw highlighted grid boundary
    pygame.draw.rect(screen, highlight_color, (game_x_offset - 5, game_y_offset - 5, game_width + 10, game_height + 10), 5)

    # Draw current block and grid
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (game_x_offset + x * block_size, game_y_offset + y * block_size, block_size, block_size), border_radius=5)
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, block.color, (game_x_offset + (block.x + x) * block_size, game_y_offset + (block.y + y) * block_size, block_size, block_size), border_radius=5)

    # Draw score and highscore
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (game_x_offset + game_width + 50, game_y_offset + 50))
    
    highscore_text = font.render(f"Highscore: {highscore}", True, white)
    screen.blit(highscore_text, (game_x_offset + game_width + 50, game_y_offset + 100))

    # Draw next block
    next_text = font.render("Next Block:", True, white)
    screen.blit(next_text, (game_x_offset + game_width + 50, game_y_offset + 150))
    for y, row in enumerate(next_block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_block.color, (game_x_offset + game_width + 100 + x * block_size, game_y_offset + 200 + y * block_size, block_size, block_size), border_radius=5)

    pygame.display.flip()

# Manage the state when a block lands
def handle_block_landing(block, grid, score):
    add_to_grid(block, grid)  # Add the block to the grid
    score += clear_rows(grid) * 100  # Clear complete rows and update score
    return score

# Display "Game Over" and final score, highscore with retry options
def game_over_screen(screen, score, highscore):
    screen.fill(black)
    game_over_text = large_font.render("GAME OVER", True, white)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))

    highscore_text = font.render(f"Highscore: {highscore}", True, white)
    screen.blit(highscore_text, (screen_width // 2 - highscore_text.get_width() // 2, screen_height // 2 + 100))

    # Menu options
    options = ["Retry", "End"]
    selected_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_option > 0:
                    selected_option -= 1
                elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                    selected_option += 1
                elif event.key == pygame.K_SPACE:  # Select option
                    if selected_option == 0:
                        return True  # Restart the game
                    elif selected_option == 1:
                        pygame.quit()
                        exit()  # Exit the game

        # Highlight selected option
        for i, option in enumerate(options):
            option_text = font.render(option, True, white if selected_option != i else gray)
            screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, screen_height // 2 + 150 + i * 50))

        pygame.display.flip()

# Game loop
def game_loop():
    score = 0
    highscore = load_highscore()

    while True:  # Loop to allow retrying the game
        grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        current_block = Block(random.choice(shapes), random.choice(shape_colors))
        next_block = Block(random.choice(shapes), random.choice(shape_colors))

        clock = pygame.time.Clock()  # Initialize clock for controlling frame rate
        drop_time = 0  # Track time since the last drop
        fall_speed = 500  # Initial fall speed in milliseconds

        hold_side_interval = 100  # Milliseconds to hold for side movement
        hold_down_interval = 50  # Milliseconds to hold for down movement
        hold_rotate_interval = 300  # Milliseconds to hold for rotation delay
        last_side_move = pygame.time.get_ticks()
        last_down_move = pygame.time.get_ticks()
        last_rotate = pygame.time.get_ticks()

        running = True
        while running:
            screen.fill(black)  # Clear the screen

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Exit the game

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if pygame.time.get_ticks() - last_side_move > hold_side_interval:
                    last_side_move = pygame.time.get_ticks()
                    if valid_move(current_block, grid, dx=-1):
                        current_block.x -= 1

            if keys[pygame.K_RIGHT]:
                if pygame.time.get_ticks() - last_side_move > hold_side_interval:
                    last_side_move = pygame.time.get_ticks()
                    if valid_move(current_block, grid, dx=1):
                        current_block.x += 1

            if keys[pygame.K_DOWN]:
                if pygame.time.get_ticks() - last_down_move > hold_down_interval:
                    last_down_move = pygame.time.get_ticks()
                    if valid_move(current_block, grid, dy=1):
                        current_block.y += 1
                    else:
                        score = handle_block_landing(current_block, grid, score)  # Handle landing logic
                        current_block = next_block
                        next_block = Block(random.choice(shapes), random.choice(shape_colors))  # Get new block
                        if not valid_move(current_block, grid):  # Check for game over
                            if score > highscore:
                                save_highscore(score)  # Save highscore if exceeded
                            if game_over_screen(screen, score, highscore):  # Retry
                                break  # Restart the game loop
                            else:
                                running = False  # End the game

            if keys[pygame.K_UP]:  # Rotate the block when the up arrow is pressed
                if pygame.time.get_ticks() - last_rotate > hold_rotate_interval:
                    last_rotate = pygame.time.get_ticks()
                    current_block.rotate()
                    if not valid_move(current_block, grid):  # If the rotation is invalid, revert it
                        current_block.rotate()  # Rotate back

            if keys[pygame.K_q]:  # Quit the game when Q is pressed
                pygame.quit()
                exit()

            # Auto drop
            drop_time += clock.get_time()
            if drop_time > fall_speed:
                drop_time = 0
                if valid_move(current_block, grid, dy=1):
                    current_block.y += 1
                else:
                    score = handle_block_landing(current_block, grid, score)  # Handle landing logic
                    current_block = next_block
                    next_block = Block(random.choice(shapes), random.choice(shape_colors))  # Get new block
                    if not valid_move(current_block, grid):  # Check for game over
                        if score > highscore:
                            save_highscore(score)  # Save highscore if exceeded
                        if game_over_screen(screen, score, highscore):  # Retry
                            break  # Restart the game loop
                        else:
                            running = False  # End the game

            # Draw the current state
            draw_grid(screen, grid, current_block, next_block, score, highscore)
            clock.tick(60)  # Control the frame rate at 60 FPS

    pygame.quit()

# Start the game loop
if __name__ == "__main__":
    game_loop()

    