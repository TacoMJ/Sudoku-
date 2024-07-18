import copy
import pygame
import math
from sudoku_generator import SudokuGenerator


class Board:
    def __init__(self, width, height, screen, difficulty):
        easy = SudokuGenerator(9, 30)
        medium = SudokuGenerator(9, 40)
        hard = SudokuGenerator(9, 50)
        self.solution = easy.solution #Not part of the code
        self.width = width #Width of the playing grid.
        self.height = height #Height of the playing grid
        self.screen = screen #The window that the game is set upon
        self.difficulty = difficulty
        self.selected_row = None #Variable for a selected row
        self.selected_col = None
        self.grid = None #The list of the playing grid.
        if self.difficulty == 'easy':
            self.grid = easy.get_board()
        elif self.difficulty == 'medium':
            self.grid = medium.get_board()
        elif self.difficulty == 'hard':
            self.grid = hard.get_board()
        self.original_grid = copy.deepcopy(self.grid) #Copies the playing grid so that it is not affected when the original playing grid is changed
        self.value = None
        self.sketchedlist = [[0 for _ in range(9)] for _ in range(9)] #Creates a list of 0s so that when a sketched number is inputted into the game, it is not placed inside the list of the playing grid
        self.original_sketch_grid = copy.deepcopy(self.sketchedlist) #Copies the sketched list so that when the game is reset, it removes the red sketched numbers


    def draw(self):
        # Draw the Sudoku grid without the numbers on them. Just the lines
        cell_size = self.width // 9

        thick_grids = cell_size * 3  # Size of each 3x3 subgrid
        for row in range(9):
            for col in range(9):
                cell_x = col * cell_size
                cell_y = row * cell_size
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

                #Drawing bold lines for the grids to seperate 3x3 cell groups
                if row % 3 == 0 and col % 3 == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0), (cell_x, cell_y, thick_grids, thick_grids), 2)
                elif row % 3 == 0:
                    pygame.draw.line(self.screen, (0, 0, 0), (cell_x, cell_y), (cell_x + cell_size, cell_y), 2)
                elif col % 3 == 0:
                    pygame.draw.line(self.screen, (0, 0, 0), (cell_x, cell_y), (cell_x, cell_y + cell_size), 2)

                #Drawing the numbers in the cells. This is the black numbers. From the user inputting and also the original sudoku grid
                number = self.grid[row][col]
                if number != 0:
                    font = pygame.font.Font(None, 30)
                    text = font.render(str(number), True, (0, 0, 0))
                    text_rect = text.get_rect(center=cell_rect.center)
                    self.screen.blit(text, text_rect.topleft)
                #sketching numbers in the empty cells. This is the red number at the top left corner.
                numbersketch = self.sketchedlist[row][col]
                if number == 0:
                    font = pygame.font.Font(None, 20)
                    if numbersketch > 0:
                        text = font.render(str(numbersketch), True, (255, 0, 0))
                        text_rect = text.get_rect(topleft=cell_rect.center)
                        text_rect.centerx += -14.5
                        text_rect.centery += -14.5
                        self.screen.blit(text, text_rect.topleft)


        posy_x, pos_y = pygame.mouse.get_pos() #Used so that the cells outside the grid isn't highlighted
        # Highlight the selected cell. The Red square when choosing a cell
        if self.selected_row is not None and self.selected_col is not None and pos_y < self.height and posy_x < self.width:
            selected_cell_x = self.selected_col * cell_size
            selected_cell_y = self.selected_row * cell_size
            selected_cell_rect = pygame.Rect(selected_cell_x, selected_cell_y, cell_size, cell_size)
            pygame.draw.rect(self.screen, (255, 0, 0), selected_cell_rect, 2)

        pygame.display.update()



    #Used to select a cell
    def select(self, row, col):
        self.selected_row = row - 1
        self.selected_col = col - 1
        cell_size = self.width // 9
        for row in range(9):
            for col in range(9):
                cell_x = col * cell_size
                cell_y = row * cell_size
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                if row == self.selected_row and col == self.selected_col:
                    # Highlight the selected cell
                    pygame.draw.rect(self.screen, (255, 0, 0), cell_rect, 4)
                else:
                    # Draw the cell outline
                    pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)
        pygame.display.update()


    def click(self, x, y):
        self.x = x
        self.y = y
        cell_size = self.width / 9
        row = math.ceil((self.y / math.ceil(cell_size)))
        col = math.ceil((self.x / math.ceil(cell_size)))
        l = (row, col)
        return l

    #Responsible for the backspace and clearing the numbers in the cell.
    def clear(self):
        if self.grid[self.selected_row][self.selected_col] != 0 and self.original_grid[self.selected_row][self.selected_col] == 0: #Clears numbers placed by the players
            self.grid[self.selected_row][self.selected_col] = 0
        if self.sketchedlist[self.selected_row][self.selected_col] != 0:
            self.sketchedlist[self.selected_row][self.selected_col] = 0

    #Responsible for inputting a sketch value which is the red number inputted by the user
    def sketch(self, sketchvalue):
        if self.grid[self.selected_row][self.selected_col] == 0:
            self.sketchvalue = sketchvalue
            self.sketchedlist[self.selected_row][self.selected_col] = self.sketchvalue

    #Responsible for commiting a sketched value into the playing grid.
    def place_number(self, value):
        self.value = value
        row = self.selected_row + 1
        col = self.selected_col + 1
        if self.grid[row -1][col -1] == 0:
            self.grid[row - 1][col - 1] = self.value

    #Respponsible for resetting the sketched list and the playing grid to it's original values
    def reset_to_original(self):
        self.grid = [row[:] for row in self.original_grid]
        self.sketchedlist = [row[:] for row in self.original_sketch_grid]

    #Determines if the playing grid is full. If it is full the game determines it the player has won or lost.
    def is_full(self):
        counter = 0
        for i in self.grid:
            for j in i:
                if j > 0:
                    counter += 1
        if counter == 81:
            return True
        return False

    #When pressing enter, it transfers the red sketched values onto the playing grid list.
    def update_board(self):
        for index_row, row in enumerate(self.grid):
            for index_col, col in enumerate(row):
                if self.grid[index_row][index_col] == 0:
                    self.grid[index_row][index_col] = self.sketchedlist[index_row][index_col]
        self.sketchedlist = [row[:] for row in self.original_sketch_grid]

    #Finds an empty cell
    def find_empty(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 0:
                    return (i + 1, j + 1)

    #Checks the board if the player has solved the sudoku game properly or not.
    def check_board(self):
        list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in self.grid: #checks each row horizontally if the numbers are unique
            if sorted(row) != list:
                return False

        for col in range(9): #checks each column vertically if the numbers are unique
            column_values = [self.grid[row][col] for row in range(9)]
            if sorted(column_values) != list:
                return False

        for i in range(0, 9, 3): #checks each 3x3 cell groups if they have unique numbers
            for j in range(0, 9, 3):
                values = []
                for row in range(i, i + 3):
                    for col in range(j, j + 3):
                        values.append(self.grid[row][col])
                if sorted(values) != list:
                    return False
        return True