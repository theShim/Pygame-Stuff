import pygame, numpy as np

def generate_gradient_border_surface(width: int, height: int, border_width: int, *colors: pygame.Color) -> pygame.Surface:
    # Create a surface to hold the gradient
    gradient_surface = pygame.Surface((width, height))

    # Calculate the number of colors
    colors = colors[0] + [colors[0][0]]
    num_colors = len(colors)
    if num_colors < 2:
        raise ValueError("At least two colors are required")

    # Create arrays for x and y coordinates
    x_coords = np.tile(np.linspace(0, 1, width), (height, 1))

    # Calculate the indices of color transition points
    color_transition_points = np.linspace(0, 1, num_colors)

    # Find the indices for the current color segment
    color_indices = np.digitize(x_coords, color_transition_points, right=True)

    # Ensure the indices are within bounds
    color_indices = np.clip(color_indices, 0, num_colors - 1)

    # Get the previous and next colors for interpolation
    prev_colors = np.take(colors, color_indices - 1, axis=0)
    next_colors = np.take(colors, color_indices, axis=0)

    # Calculate the relative position within the current segment
    segment_ratios = (x_coords * (num_colors - 1)) % 1

    # Interpolate colors within the segment
    interpolated_colors = prev_colors + segment_ratios[:, :, np.newaxis] * (next_colors - prev_colors)

    # Fill the gradient surface with interpolated colors
    gradient_surface_array = pygame.surfarray.pixels3d(gradient_surface)
    gradient_surface_array[:, :] = np.transpose(interpolated_colors.astype(int), (1, 0, 2))  # Transpose the array
    gradient_surface_array[-1, :] = colors[-1]

    return gradient_surface

if __name__ == '__main__':
    resolution = (500, 300)
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    
    color_corners = pygame.Color(255, 0, 0)
    color_sides = pygame.Color(0, 255, 0)
    surface = generate_gradient_border_surface(300, 200, 5, color_corners, color_sides)

    screen.fill((100, 50, 70))
    screen.blit(surface, (50, 50))
    pygame.display.flip()

    import time
    while True:
        time.sleep(1)