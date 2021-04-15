
import pygame
import constant as const
import time
import snake
import threading
import random

def graphics(board):
	pygame.init()

	# Set up the drawing window
	screen = pygame.display.set_mode([const.SCREEN_WIDTH, const.SCREEN_HEIGHT])
	font = pygame.font.Font(None, 24)
	snekText = font.render(("SNEK" if random.randint(0,100) > 33 else ("SHNAKE" if random.randint(0,1) > 0 else "SHLUG")), True, (230,230,255), (0,0,0))
	snekTextRect = snekText.get_rect()
	snekTextRect.topleft = (5, 5)
	font = pygame.font.Font(None, 16)
	text = font.render("", True, (200,200,0), (0,0,0))
	textRect = text.get_rect()
	textRect.center = (const.SCREEN_WIDTH-70, 5)
	screen.blit(snekText, snekTextRect)
	boardSurface = pygame.Surface((const.SCREEN_WIDTH-2*const.BORDER, const.SCREEN_HEIGHT-2*const.BORDER))
	boardSurface.fill((150, 150, 150))
	board.drawInit(boardSurface)

	#board = snake.Board(sizeX=40,sizeY=40, surface=boardSurface)
	# Run until the user asks to quit
	running = True
	count = 0
	lastFrameTime = time.time()
	FPS = 0
	while running:
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_UP]:
			board.snake.updateDirection((0,-1))
		elif pressed_keys[pygame.K_DOWN]:
			board.snake.updateDirection((0,1))
		elif pressed_keys[pygame.K_LEFT]:
			board.snake.updateDirection((-1,0))
		elif pressed_keys[pygame.K_RIGHT]:
			board.snake.updateDirection((1,0))
		count = (count + 1) % 30
		if count == 0:
			now = time.time()
			frameTime = now-lastFrameTime
			lastFrameTime = now
			if frameTime == 0:
				FPS = "N/A"
			else:
				FPS = (1/frameTime)*30
		text = font.render(("FPS: " + str(FPS)), True, (200,200,0), (0,0,0))
		screen.blit(text, textRect)
		board.draw()
		screen.blit(boardSurface, (const.BORDER, const.BORDER))
		# Did the user click the window close button?
		if pygame.event.peek(pygame.QUIT):
			running = False
			pygame.event.clear()

		pygame.display.flip()

def gameplay(board):
	gameOver = False
	clock = pygame.time.Clock()
	while not gameOver:
		board.updateGameState()
		if pygame.event.peek(pygame.USEREVENT) or pygame.event.peek(pygame.QUIT):
			gameOver = True
		clock.tick(const.GAME_SPEED)

def main():
	board = snake.Board(sizeX=20,sizeY=20)
	t = threading.Thread(target=graphics, args=[board])
	t.start()
	gameplay(board)

if __name__ == '__main__':
	main()