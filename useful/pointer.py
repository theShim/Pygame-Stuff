
#example code from previous game, draws a polygon and rotates it to the mouse position

# #pointer
# vec = pygame.math.Vector2
# mousePos = vec(pygame.mouse.get_pos()) - self.offset
# player = self.blobs.sprites()[0]
# px, py = player.rect.center

# dx = mousePos.x - px
# dy = mousePos.y - py
# angle = (180 / math.pi) * math.atan2(dy, dx) + 90

# if self.pointer == None:
#     self.pointer = pygame.Surface((20, 20), pygame.SRCALPHA)
#     pygame.draw.polygon(
#         self.pointer,
#         (player.col),
#         [
#             (0, 0),
#             (20, 0),
#             (10, math.sqrt(20**2 - 10**2)),
#         ]a
#     )
#     self.pointer = pygame.transform.flip(self.pointer, False, True)
#     self.initial_vec_angle = pygame.math.Vector2(0, -player.mass/1.4)

# pointA = pygame.math.Vector2(px, py)
# pointB = vec(pointA + self.initial_vec_angle.rotate(angle)) - vec(10, 10)
# self.image.blit(pygame.transform.rotate(self.pointer, -angle), pointB)