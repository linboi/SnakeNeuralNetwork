from enum import Enum
import pygame
import random

class Squares(Enum):
	EMPTY = 0
	FOOD = 1
	HEAD = 2
	SNAKE = 3
	WALL = 4

	def isHazard(self, square):
		if square == self.SNAKE or square == self.WALL:
			return True
		else:
			return False



class Board():
	def __init__(self, sizeX=10, sizeY=10, surface=None):
		self.height = sizeY
		self.width = sizeX
		self.grid = [[Squares.EMPTY for x in range(self.height)] for y in range(self.width)]
		if surface != None:
			self.drawInit(surface)
		self.snake = Snake(self)
		foundSpot = False
		while not foundSpot:
			randX = random.randint(0, self.width-1)
			randY = random.randint(0, self.height-1)
			if self.grid[randX][randY] == Squares.EMPTY:
				self.grid[randX][randY] = Squares.FOOD
				foundSpot = True
		self.updatedSquares = set()
		for rowIdx, row in enumerate(self.grid):
			for colIdx in range(len(row)):
				self.updatedSquares.add((rowIdx, colIdx))

	def drawInit(self, surface):
		self.surface = surface
		self.drawingWidth = surface.get_width()
		self.drawingHeight = surface.get_height()
		self.blockWidth = self.drawingWidth/self.width
		self.blockHeight = self.drawingHeight/self.height

	def draw(self):
		#if not self.beans:
		#	for a in self.grid:
		#		print(a)
		#		#for b in a:
		#		#	print(b, end=" ")
		#		#print("", end="\n")
		#self.beans = True
		for position in self.updatedSquares:
			rowIdx, colIdx = position
			square = self.grid[rowIdx][colIdx]
			temp = pygame.Surface((self.blockWidth-1, self.blockHeight-1))
			if square == Squares.EMPTY:
				temp.fill((30,30,30))
			elif square == Squares.WALL:
				temp.fill((255,255,255))
			elif square == Squares.SNAKE:
				temp.fill((0,150,0))
			elif square == Squares.HEAD:
				temp.fill((0,255,0))
			elif square == Squares.FOOD:
				temp.fill((255,0,0))
			self.surface.blit(temp, (rowIdx*self.blockWidth+1, colIdx*self.blockHeight+1))
			#self.beans = True
		self.updatedSquares.clear()

	def updateGameState(self):
		self.snake.updatePosition()

class Snake():
	def __init__(self, board=None, length=3, position=None):
		if position == None:
			self.headPos = (length, length)
		else:
			self.headPos = position
		self.board=board	# The game board this snake is on
		self.length=length
		self.direction = (1, 0)
		self.nextDirection = (1, 0)
		self.bodyPositionsQueue = []
		for x in range(length-1, 0, -1):
			board.grid[self.headPos[0]-x][self.headPos[1]] = Squares.SNAKE
			self.bodyPositionsQueue.append((self.headPos[0]-x, self.headPos[1]))
		print(self.bodyPositionsQueue)
		board.grid[self.headPos[0]][self.headPos[1]] = Squares.HEAD

	def updatePosition(self):
		x, y = self.headPos
		dx, dy = self.nextDirection
		self.direction = self.nextDirection
		newPos = ((x+dx) % self.board.width), ((y+dy) % self.board.height)
		if self.board.grid[newPos[0]][newPos[1]] == Squares.FOOD:
			foundSpot = False
			while not foundSpot:
				randX = random.randint(0, self.board.width-1)
				randY = random.randint(0, self.board.height-1)
				if self.board.grid[randX][randY] == Squares.EMPTY:
					self.board.grid[randX][randY] = Squares.FOOD
					self.board.updatedSquares.add((randX, randY))
					foundSpot = True
		elif self.board.grid[newPos[0]][newPos[1]] == Squares.SNAKE:
			return pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"EVENT":"GAMEOVER"}))
		else:
			lastX, lastY = self.bodyPositionsQueue.pop(0)
			self.board.grid[lastX][lastY] = Squares.EMPTY
			self.board.updatedSquares.add((lastX, lastY))
		self.headPos = newPos
		self.board.grid[x][y]=Squares.SNAKE
		self.bodyPositionsQueue.append((x,y))
		self.board.grid[newPos[0]][newPos[1]]=Squares.HEAD
		self.board.updatedSquares.update([newPos, (x,y)])



	def updateDirection(self, direction):
		if self.direction[0] != direction[0] and self.direction[1] != direction[1]:
			self.nextDirection = direction

		
