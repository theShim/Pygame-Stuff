import pygame

#YELLOW = (255, 255, 0) = NEW ROW OF TILES
#MAGENTA = (255, 0, 255) = NEW INDIVIDUAL TILE
#CYAN = (0, 255, 255) = END OF INDIVIDUAL TILE (VERTICAL OR HORIZONTAL)


#
def crop(spritesheet, x, y, width, height) -> pygame.Surface:
    cropped = pygame.Surface((width, height), pygame.SRCALPHA)
    cropped.blit(spritesheet, (0, 0), (x, y, width, height))
    cropped = pygame.transform.scale(cropped, (width*4, height*4))
    return cropped


def load_sheet(filename):
    spritesheet = pygame.image.load(filename)
    spritesheet_data = []

    rows = []
    for py in range(spritesheet.get_height()):
        if spritesheet.get_at((0, py)) == (255, 255, 0):
            rows.append(py)

    for row in rows:
        row_content = []
        for px in range(spritesheet.get_width()):
            if spritesheet.get_at((px, row)) == (255, 0, 255):
                i = 0
                while True:
                    i += 1
                    if spritesheet.get_at((px + i, row)) == (0, 255, 255):
                        width = i
                        break
                
                i = 0
                while True:
                    i += 1
                    if spritesheet.get_at((px, row + i)) == (0, 255, 255):
                        height = i
                        break

                img = crop(spritesheet, px+1, row+1, width-1, height-1)
                img.set_colorkey(COLOUR_CODES['colourkey'])
                row_content.append(img)

        spritesheet_data.append(row_content)
    return spritesheet_data[0]


class Animator():
    def __init__(self, sprites, loop=False, fps=1):
        self.sprites = sprites
        self.loop = loop
        self.index = -1
        self.fps = fps
        self.f = 0

    def next(self):
        self.f += 1
        if self.f >= self.fps:
            self.f = 0
            self.index += 1

        try:
            return self.sprites[self.index].copy()
        except:
            if self.loop:
                self.index = 0
                return self.sprites[self.index].copy()
            else:
                self.index = 0
                raise Animator.EndOfAnimError

    class EndOfAnimError(Exception):
        pass

                
# dat = load_sheet('assets/characters/test/Run.png')
# print(dat)