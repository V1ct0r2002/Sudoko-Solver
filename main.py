import random
import math
import pygame
import time
import os

# PYGAME SETUP
WIDTH= 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

highlighted = [0,0]

# IMAGES
background = pygame.image.load(os.path.join("res", "sudoku_grid.png"))

pygame.font.init()
gridFont = pygame.font.SysFont('Times New Roman', 30)

grid = []
moves = [1,2,3,4,5,6,7,8,9]

def empty_grid(n,m):
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(0)
        grid.append(row)
    return grid

def init():
    global grid
    grid = [[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0], [0,9,8,0,0,0,0,6,0], [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]
    #grid = [[0,3,0,0,7,0,0,0,0],[6,0,0,1,9,0,0,0,0], [0,9,8,0,0,0,0,6,0], [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]

def print_grid(grid):
    r = 0
    for i in range(13):
        if i%4 == 0:
            print("  -  -  -   -  -  -   -  -  -  ")
        else:
            print("| " + str(grid[r][0]) + "  " + str(grid[r][1]) + "  " + str(grid[r][2]) + " | " + str(grid[r][3]) + "  " + str(grid[r][4]) + "  " + str(grid[r][5]) + " | " + str(grid[r][6]) + "  " + str(grid[r][7]) + "  " + str(grid[r][8]) + " |")
            r += 1

def possible(row, col, num, grid):
    global moves
    # Check row
    for entry in grid[row]:  # Loop through each entry in row
        if entry == num:  # If entry is number we are trying to add
            return False  # This move is not valid

    # Check col
    for i in range(len(grid)):  # Loop through each entry in column
        if grid[i][col] == num:  # If entry is number we are trying to add
            return False  # This move is not valid

    # Check sub-grid
    n = row // 3  # Find which 3x3 sub-grid we are in
    m = col // 3

    for i in range(n*3, n*3 + 3):
        for j in range(m*3, m*3 +3):  # Loop through each entry in 3x3 sub-grid
            if grid[i][j] == num:  # If entry is number we are trying to add
                return False  # This move is not valid

    return True  # If we haven't returned False yet, this move is valid!

def solve(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                for num in moves:
                    if possible(row, col, num, grid):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def fill_grid(n, m):
    global moves

    new_grid = empty_grid(n, m)
    # Pick 17 random starting indices
    starting_indices = []
    for i in range(17):
        while True:
            index = random.randint(0,(n*m)-1)
            if not index in starting_indices:
                starting_indices.append(index)
                break
    for ind in starting_indices:
        r = math.floor(ind/m)
        c = ind % m
        while True:
            move = random.choice(moves)
            if possible(r, c, move, new_grid):
                new_grid[r][c] = move
                break
    solve(new_grid)
    return new_grid

def generate_grid(difficulty):
    # Beginner = 0, Easy = 1, Intermediate = 2, Expert = 3, Master = 4
    difficulty_factor = 4 * (5-difficulty)
    number_of_blanks = 81 - (17+difficulty_factor)

    #print(number_of_blanks)

    generated_grid = fill_grid(9,9)

    blank_indices = []
    for i in range(number_of_blanks):
        while True:
            new_index = random.randint(0,80)
            if not new_index in blank_indices:
                blank_indices.append(new_index)
                break

    for index in blank_indices:
        row = math.floor(index / 9)
        col = index % 9
        generated_grid[row][col] = 0

    return generated_grid


def write_text(text, x, y, font = gridFont, color="Coral"):
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(x,y))
    return text, text_rect

GRID_WIDTH = 500
CELL_WIDTH = 500/9
CENTER_ALIGN = 500/18
X_START = 150
Y_START = 50

def fill_cell(num, i, j, window):
    a,b = write_text(str(num), X_START + i*CELL_WIDTH + CENTER_ALIGN, Y_START + j*CELL_WIDTH + CENTER_ALIGN, color = (0, 0, 0))
    window.blit(a,b)

def draw_highlighted_cell(window):
    pygame.draw.rect(window, (255,0,0), pygame.Rect(150+highlighted[0]*CELL_WIDTH, 50+highlighted[1]*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH), 2)

def clear_window():
    window.blit(background, (0,0))
    draw_highlighted_cell(window)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if not grid[i][j] == 0:
                fill_cell(grid[i][j], i, j, window)
    pygame.display.update()

def main():
    global highlighted
    g = generate_grid(3)

    running = True
    fps = 60
    clock = pygame.time.Clock()

    while running:
        clock.tick(fps)
        clear_window()

        pos = pygame.mouse.get_pos()
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

        if pressed1:
            if pos[0] > 150 and pos[0] < 650 and pos[1] > 50 and pos[1] < 550:
                i = (pos[0] - 150)//CELL_WIDTH
                j = (pos[1] - 50)//CELL_WIDTH
                highlighted[0] = i
                highlighted[1] = j

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solve(grid)
                if event.key == pygame.K_RIGHT:
                    if highlighted[0] < 8:
                        highlighted[0] += 1
                    else:
                        highlighted[0] = 0
                elif event.key == pygame.K_LEFT:
                    if highlighted[0] > 0:
                        highlighted[0] -= 1
                    else:
                        highlighted[0] = 8
                if event.key == pygame.K_UP:
                    if highlighted[1] > 0:
                        highlighted[1] -= 1
                    else: highlighted[1] = 8
                elif event.key == pygame.K_DOWN:
                    if highlighted[1] < 8:
                        highlighted[1] += 1
                    else:
                        highlighted[1] = 0


init()
main()
#solve(grid)
#print_grid(grid)
#g = generate_grid(0)
#print_grid(g)
#solve(g)
#print("\n")
#print_grid(g)
