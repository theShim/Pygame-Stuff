import pygame as pg

# Initialize Pygame
pg.init()

# Set up the display
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Pygame Palette Example")

# Create an 8-bit surface
surface = pg.Surface((800, 600), depth=8)

# Define a color palette (R, G, B tuples)
palette = [
    (0, 0, 0),        # Index 0: Black
    (255, 0, 0),      # Index 1: Red
    (0, 255, 0),      # Index 2: Green
    (0, 0, 255),      # Index 3: Blue
    (255, 255, 0),    # Index 4: Yellow
    (0, 255, 255),    # Index 5: Cyan
    (255, 0, 255),    # Index 6: Magenta
    (255, 255, 255)   # Index 7: White
]
palette = [list(p) + [255] for p in palette]

# Set the palette for the 8-bit surface
surface.set_palette(palette)

# Fill the surface with different colors using the palette indices
surface.fill(0)  # Fill with black (index 0)
pg.draw.rect(surface, 1, (50, 50, 100, 100))  # Draw a red square using index 1
pg.draw.circle(surface, 2, (200, 100), 50)    # Draw a green circle using index 2
pg.draw.line(surface, 3, (300, 50), (400, 150), 5)  # Draw a blue line using index 3
pg.draw.ellipse(surface, 4, (450, 50, 100, 50))  # Draw a yellow ellipse using index 4
pg.draw.polygon(surface, 5, [(100, 300), (200, 300), (150, 400)])  # Draw a cyan triangle using index 5
pg.draw.arc(surface, 6, (300, 250, 100, 100), 0, 3.14, 3)  # Draw a magenta arc using index 6

# Main loop flag
running = True

# Main game loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Blit the 8-bit surface to the main screen
    screen.fill((255, 255, 255))
    screen.blit(surface, (0, 0))

    palette[0][0] += 0.1
    palette[0][-1] -= 1
    # surface.set_palette_at(2, palette[0])
    surface.set_palette(palette)

    # Update the display
    pg.display.flip()

# Quit Pygame
pg.quit()
