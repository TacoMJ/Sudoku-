import pygame
from board import Board

class Text(): #Creates a text object so that it is easier to place texts within the window
	def __init__(self, text, font_size, font_color, SCREEN_WIDTH, SCREEN_HEIGHT, x, y):
		self.text = text
		self.font_size = font_size
		self.font_color = font_color
		self.SCREEN_WIDTH = SCREEN_WIDTH
		self.SCREEN_HEIGHT = SCREEN_HEIGHT
		self.x = x
		self.y = y


	def draw(self, surface):
		font = pygame.font.Font(None, 30)
		text_ = font.render(self.text, True, (255, 0, 0))
		text_align = text_.get_rect(center=(self.SCREEN_WIDTH // self.x, self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT / self.y)))
		surface.blit(text_, text_align)

class Button(): #Button object to create buttons to use
	def __init__(self, x, y, text):
		pygame.font.init()
		self.font = pygame.font.Font(None, 30)
		self.text = text
		self.rendered_text = self.font.render(text, True, (255, 0, 0))
		self.rect = self.rendered_text.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface, width, height):
		action = False
		pos = pygame.mouse.get_pos()
		self.width = width
		self.height = height

		x = self.rect.x
		y = self.rect.y

		br = pygame.Rect((x, y), (self.width, self.height))
		pygame.draw.rect(surface, 'gray', br)

		outline = pygame.Rect((x, y), (self.width, self.height))
		pygame.draw.rect(surface, 'black', outline, 2)

		tr = self.rendered_text.get_rect(center=br.center)

		surface.blit(self.rendered_text, tr.topleft)

		if br.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				self.clicked = True
				action = True
			#When colliding with a mouse cursor, the buttons turn white:
			br = pygame.Rect((x, y), (self.width, self.height))
			pygame.draw.rect(surface, (255, 255, 255), br)
			outline = pygame.Rect((x, y), (self.width, self.height))
			pygame.draw.rect(surface, 'black', outline, 2)
			tr = self.rendered_text.get_rect(center=br.center)
			surface.blit(self.rendered_text, tr.topleft)
			#-----------------------------------------------------------
		else:
			self.clicked = False

		return action




def GameWon(): #Displays the game won screen after the player has won
	# create display window for Game won
	SCREEN_HEIGHT = 700
	SCREEN_WIDTH = 495
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('SUDOKU')
	exit = Button(SCREEN_WIDTH / 2.4, SCREEN_HEIGHT - 500, 'Exit') #Creates the exit button

	# game loop
	run = True
	while run:
		# --------------------------------------------WELCOME WINDOW FOR SUDOKU-----------------------------------------------
		screen.fill((202, 228, 241))
		text1 = Text("Game Won!", 30, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT, 2, 1.2)
		text1.draw(screen) #Displays the "Game Won!" Text

		ex = exit.draw(screen, 90, 50) #Displays the exit button
		# ---------------------------------------------------------------------------------------------------------------------
		if ex == True: #When the exit button is pressed, it becomes True exiting the program.
			run = False
		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

def GameOver(): #Displays the gamover screen when the player has lost
	# create display window for Game over
	SCREEN_HEIGHT = 700
	SCREEN_WIDTH = 495
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('SUDOKU')
	restart = Button(SCREEN_WIDTH / 2.4, SCREEN_HEIGHT - 500, 'Restart')

	# game loop
	run = True
	while run:
		# --------------------------------------------WELCOME WINDOW FOR SUDOKU-----------------------------------------------
		screen.fill((202, 228, 241))
		text1 = Text("Game Over :(", 30, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT, 2, 1.2)
		text1.draw(screen) #Displays the "Game Over :(" Text

		rest = restart.draw(screen, 90, 50) #Displays the restart button
		# ---------------------------------------------------------------------------------------------------------------------
		if rest == True: #When the restart button is pressed, it becomes True and opens up the main() window/function
			main()
		# event handler
		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()
def SudokuGameEasy(): #Opens up the window for the easy mode for SUDOKU. This is pretty much the same as SudokuGameMedium() and SudokuGameHard(). So I will just comment on this.
	SCREEN_HEIGHT = 700
	SCREEN_WIDTH = 495
	row = 1
	col = 1
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('SUDOKU')


	sudoku = Board(500, 500, screen, 'easy') #Creates the sudkou board object
	reset = Button(100, SCREEN_HEIGHT - 150, 'Reset') #Creates the buttons
	restart = Button(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT - 150, 'Restart')
	exit = Button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 150, 'Exit')
	print(sudoku.grid)
	print('Hello')
	run = True
	while run:



	#---------------------------------------Sudoku Game WINDOW---------------------------------
		screen.fill((255, 255, 255))
		res = reset.draw(screen, 90, 50)
		rest = restart.draw(screen, 90, 50)
		ex = exit.draw(screen, 90, 50)
		sudoku.draw()
		sudoku.select(row, col)
		sudoku.check_board()

		if res == True:
			sudoku.reset_to_original()
		if rest == True:
			main()
		if ex == True:
			run = False
		if sudoku.is_full() == True:
			sudoku.check_board()
			if sudoku.check_board() == False:
				GameOver()
			elif sudoku.check_board() == True:
				GameWon()


		# event handler
		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Handle mouse click events
				x, y = pygame.mouse.get_pos()
				row, col = sudoku.click(x, y)
				print("Clicked cell:", row, col)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(1)
					print(number)
				elif event.key == pygame.K_2:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(2)
					print(number)
				elif event.key == pygame.K_3:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(3)
					print(number)
				elif event.key == pygame.K_4:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(4)
					print(number)
				elif event.key == pygame.K_5:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(5)
					print(number)
				elif event.key == pygame.K_6:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(6)
					print(number)
				elif event.key == pygame.K_7:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(7)
					print(number)
				elif event.key == pygame.K_8:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(8)
					print(number)
				elif event.key == pygame.K_9:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(9)
					print(number)
				elif event.key == pygame.K_BACKSPACE:
					#Backspace for clearing the cells
					sudoku.clear()
				elif event.key == pygame.K_RETURN:
					sudoku.update_board()
				elif event.key == pygame.K_UP:
					if 1 < row < 10:
						row = row - 1
				elif event.key == pygame.K_DOWN:
					if 0 < row < 9:
						row = row + 1
				elif event.key == pygame.K_LEFT:
					if 1 < col < 10:
						col = col - 1
				elif event.key == pygame.K_RIGHT:
					if 0 < col < 9:
						col = col + 1
				print("ACTUAL GRID")
				print(sudoku.grid)
				print("SKETCHED GRID")
				print(sudoku.sketchedlist)
		pygame.display.update()
	pygame.quit()

def SudokuGameMedium():
	SCREEN_HEIGHT = 700
	SCREEN_WIDTH = 495
	row = 1
	col = 1
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('SUDOKU')

	sudoku = Board(500, 500, screen, 'medium')
	reset = Button(100, SCREEN_HEIGHT - 150, 'Reset')
	restart = Button(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT - 150, 'Restart')
	exit = Button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 150, 'Exit')
	print(sudoku.grid)
	print('Hello')
	run = True
	while run:

		# ---------------------------------------Sudoku Game WINDOW---------------------------------
		screen.fill((255, 255, 255))
		res = reset.draw(screen, 90, 50)
		rest = restart.draw(screen, 90, 50)
		ex = exit.draw(screen, 90, 50)
		sudoku.draw()
		sudoku.select(row, col)
		sudoku.check_board()

		if res == True:
			sudoku.reset_to_original()
		if rest == True:
			main()
		if ex == True:
			run = False
		if sudoku.is_full() == True:
			sudoku.check_board()
			if sudoku.check_board() == False:
				GameOver()
			elif sudoku.check_board() == True:
				GameWon()

		# event handler
		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Handle mouse click events
				x, y = pygame.mouse.get_pos()
				row, col = sudoku.click(x, y)
				print("Clicked cell:", row, col)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(1)
					print(number)
				elif event.key == pygame.K_2:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(2)
					print(number)
				elif event.key == pygame.K_3:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(3)
					print(number)
				elif event.key == pygame.K_4:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(4)
					print(number)
				elif event.key == pygame.K_5:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(5)
					print(number)
				elif event.key == pygame.K_6:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(6)
					print(number)
				elif event.key == pygame.K_7:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(7)
					print(number)
				elif event.key == pygame.K_8:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(8)
					print(number)
				elif event.key == pygame.K_9:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(9)
					print(number)
				elif event.key == pygame.K_BACKSPACE:
					# Backspace for clearing the cells
					sudoku.clear()
				elif event.key == pygame.K_RETURN:
					sudoku.update_board()
				elif event.key == pygame.K_UP:
					if 1 < row < 10:
						row = row - 1
				elif event.key == pygame.K_DOWN:
					if 0 < row < 9:
						row = row + 1
				elif event.key == pygame.K_LEFT:
					if 1 < col < 10:
						col = col - 1
				elif event.key == pygame.K_RIGHT:
					if 0 < col < 9:
						col = col + 1
				print("ACTUAL GRID")
				print(sudoku.grid)
				print("SKETCHED GRID")
				print(sudoku.sketchedlist)
		pygame.display.update()
	pygame.quit()
def SudokuGameHard():
	SCREEN_HEIGHT = 700
	SCREEN_WIDTH = 495
	row = 1
	col = 1
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('SUDOKU')

	sudoku = Board(500, 500, screen, 'hard')
	reset = Button(100, SCREEN_HEIGHT - 150, 'Reset')
	restart = Button(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT - 150, 'Restart')
	exit = Button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 150, 'Exit')
	print(sudoku.grid)
	print('Hello')
	run = True
	while run:

		# ---------------------------------------Sudoku Game WINDOW---------------------------------
		screen.fill((255, 255, 255))
		res = reset.draw(screen, 90, 50)
		rest = restart.draw(screen, 90, 50)
		ex = exit.draw(screen, 90, 50)
		sudoku.draw()
		sudoku.select(row, col)
		sudoku.check_board()

		if res == True:
			sudoku.reset_to_original()
		if rest == True:
			main()
		if ex == True:
			run = False
		if sudoku.is_full() == True:
			sudoku.check_board()
			if sudoku.check_board() == False:
				GameOver()
			elif sudoku.check_board() == True:
				GameWon()

		# event handler
		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Handle mouse click events
				x, y = pygame.mouse.get_pos()
				row, col = sudoku.click(x, y)
				print("Clicked cell:", row, col)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(1)
					print(number)
				elif event.key == pygame.K_2:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(2)
					print(number)
				elif event.key == pygame.K_3:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(3)
					print(number)
				elif event.key == pygame.K_4:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(4)
					print(number)
				elif event.key == pygame.K_5:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(5)
					print(number)
				elif event.key == pygame.K_6:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(6)
					print(number)
				elif event.key == pygame.K_7:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(7)
					print(number)
				elif event.key == pygame.K_8:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(8)
					print(number)
				elif event.key == pygame.K_9:
					number = int(pygame.key.name(event.key))
					sudoku.sketch(9)
					print(number)
				elif event.key == pygame.K_BACKSPACE:
					# Backspace for clearing the cells
					sudoku.clear()
				elif event.key == pygame.K_RETURN:
					sudoku.update_board()
				elif event.key == pygame.K_UP:
					if 1 < row < 10:
						row = row - 1
				elif event.key == pygame.K_DOWN:
					if 0 < row < 9:
						row = row + 1
				elif event.key == pygame.K_LEFT:
					if 1 < col < 10:
						col = col - 1
				elif event.key == pygame.K_RIGHT:
					if 0 < col < 9:
						col = col + 1
				print("ACTUAL GRID")
				print(sudoku.grid)
				print("SKETCHED GRID")
				print(sudoku.sketchedlist)
		pygame.display.update()
	pygame.quit()

def main():
	#create display window
	SCREEN_HEIGHT = 700
	SCREEN_WIDTH = 800
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('SUDOKU')
	# create button instances
	easy = Button(100, SCREEN_HEIGHT - 400, 'Easy ')
	medium = Button(SCREEN_WIDTH / 2.3, SCREEN_HEIGHT - 400, 'Medium ')
	hard = Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 400, 'Hard ')


	#game loop
	run = True
	while run:
	#--------------------------------------------WELCOME WINDOW FOR SUDOKU-----------------------------------------------
		screen.fill((0, 230, 230))
		text1 = Text("Welcome to Sudoku!", 30, (0,0,0), SCREEN_WIDTH, SCREEN_HEIGHT, 2, 1.2)
		text1.draw(screen)
		text2 = Text('Select Game Mode:', 30, (0,0,0), SCREEN_WIDTH, SCREEN_HEIGHT,2, 1.5)
		text2.draw(screen)
		if easy.draw(screen, 90, 50):
			SudokuGameEasy() #Initialize the sudoku game window
		if medium.draw(screen, 90, 50):
			SudokuGameMedium()
		if hard.draw(screen, 90, 50):
			SudokuGameHard()
	#---------------------------------------------------------------------------------------------------------------------


		for event in pygame.event.get():
			#quit game
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

	pygame.quit()

main()