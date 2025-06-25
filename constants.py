TILE_SIZE       = 200
SCREEN_WIDTH    = 4 * TILE_SIZE
SCREEN_HEIGHT   = 5 * TILE_SIZE
FPS             = 60
LOGO_SIZE       = int(TILE_SIZE / 2)
SCORE_SIZE      = int(TILE_SIZE / 5)

TEXT_COLOR_LIGHT = (249, 246, 242)
TEXT_COLOR_DARK = (119, 110, 101)

GRID_COLOR = (187, 173, 160)
BACKGROUND_COLOR = (205, 193, 180)

TILE_COLOR = {
    0:    BACKGROUND_COLOR,
    2:    (238, 228, 218),
    4:    (237, 224, 200),
    8:    (242, 177, 121),
    16:   (245, 149, 99),
    32:   (246, 124, 95),
    64:   (246, 94, 59),
    128:  (237, 207, 114),
    256:  (237, 204, 97),
    512:  (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
