import random
class SudokuGenerator:
    def __init__(self, row_length=9, removed_cells=30):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.solution = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.fill_values()

    def get_board(self):
        return self.board

    def get_solution(self):
        return self.solution

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        self.copy_solution()  # Keep a copy of the solution before removing cells
        self.remove_cells()  # Remove cells based on the specified number

    def copy_solution(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                self.solution[row][col] = self.board[row][col]

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        index = 0
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums[index]
                index += 1

    def fill_remaining(self, row, col):
        if row == self.row_length - 1 and col == self.row_length:
            return True
        if col == self.row_length:
            row += 1
            col = 0
        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def is_valid(self, row, col, num):
        return not self.valid_in_row(row, num) and not self.valid_in_col(col, num) and not self.valid_in_box(
            row - row % 3, col - col % 3, num)

    def valid_in_row(self, row, num):
        return num in self.board[row]

    def valid_in_col(self, col, num):
        return any(self.board[row][col] == num for row in range(self.row_length))

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return True
        return False

    def remove_cells(self):
        removed_positions = set()  # Track which cells are removed
        while len(removed_positions) < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if (row, col) not in removed_positions:
                self.board[row][col] = 0
                removed_positions.add((row, col))

    def print_board(self):
        for row in self.board:
            print(row)


sudoku = SudokuGenerator()
print(sudoku.get_board())