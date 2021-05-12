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
	def __init__(self, sizeX=10, sizeY=10, surface=None, drawMode=True):
		self.height = sizeY
		self.width = sizeX
		self.clock = pygame.time.Clock()
		self.grid = [[Squares.EMPTY for x in range(self.height)] for y in range(self.width)]
		self.snake = Snake(self)
		foundSpot = False
		while not foundSpot:
			randX = random.randint(0, self.width-1)
			randY = random.randint(0, self.height-1)
			if self.grid[randX][randY] == Squares.EMPTY:
				self.grid[randX][randY] = Squares.FOOD
				foundSpot = True
		self.drawMode = drawMode
		if(drawMode):
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
		self.updatedSquares.clear()

	def updateGameState(self, time):
		self.snake.updatePosition()
		self.clock.tick(time)

	def headlessNextState(self, decision, clocktime=0):
		self.snake.updateDirection(self.snake.decisionToDirection(decision))
		result = self.snake.updatePosition()
		flattenedGrid = self.gridToNNInput()
		if clocktime != 0:
			self.clock.tick(clocktime)
		return (result, flattenedGrid)

	def gridToNNInput(self):
		flatGridRepresentation = [0]*self.width*self.height*3
		# the flat grid will be a list the same length as the grid (w*h),
		# times the number of channels (one for the snake, food, hazards (3))
		foodOffset = self.width*self.height
		hazardOffset = self.width*self.height*2
		idx = 0
		for row in range(len(self.grid)):
			for col in range(len(self.grid[row])):
				if(self.grid[row][col].value > Squares.HEAD.value):
					flatGridRepresentation[idx + hazardOffset] = 1
				elif self.grid[row][col] == Squares.FOOD:
					flatGridRepresentation[idx + foodOffset] = 1
				elif self.grid[row][col] == Squares.HEAD:
					flatGridRepresentation[idx] = 1
				idx = idx + 1
		return flatGridRepresentation


class Snake():
	def __init__(self, board=None, length=3, position=None):
		if position == None:
			self.headPos = (length, length)
		else:
			self.headPos = position
		self.board=board	# The game board this snake is on
		self.length=length
		self.score=0
		self.direction = (1, 0)
		self.nextDirection = (1, 0)
		self.bodyPositionsQueue = []
		for x in range(length-1, 0, -1):
			board.grid[self.headPos[0]-x][self.headPos[1]] = Squares.SNAKE
			self.bodyPositionsQueue.append((self.headPos[0]-x, self.headPos[1]))
		board.grid[self.headPos[0]][self.headPos[1]] = Squares.HEAD

	def updatePosition(self):
		x, y = self.headPos
		dx, dy = self.nextDirection
		self.direction = self.nextDirection
		newPos = ((x+dx) % self.board.width), ((y+dy) % self.board.height)
		if self.board.grid[newPos[0]][newPos[1]] == Squares.FOOD:
			self.score += 1
			foundSpot = False
			while not foundSpot:
				randX = random.randint(0, self.board.width-1)
				randY = random.randint(0, self.board.height-1)
				if self.board.grid[randX][randY] == Squares.EMPTY:
					self.board.grid[randX][randY] = Squares.FOOD
					if(self.board.drawMode):
						self.board.updatedSquares.add((randX, randY))
					foundSpot = True
		elif self.board.grid[newPos[0]][newPos[1]] == Squares.SNAKE:
			if self.board.drawMode:
				pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"EVENT":"GAMEOVER"}))
			return self.score
		else:
			lastX, lastY = self.bodyPositionsQueue.pop(0)
			self.board.grid[lastX][lastY] = Squares.EMPTY
			if(self.board.drawMode):
				self.board.updatedSquares.add((lastX, lastY))
		self.headPos = newPos
		self.board.grid[x][y]=Squares.SNAKE
		self.bodyPositionsQueue.append((x,y))
		self.board.grid[newPos[0]][newPos[1]]=Squares.HEAD
		if(self.board.drawMode):
			self.board.updatedSquares.update([newPos, (x,y)])
		return -1 # game has not ended


	def updateDirection(self, direction):
		if self.direction[0] != direction[0] and self.direction[1] != direction[1]:
			self.nextDirection = direction

	def decisionToDirection(self, decision):
		# This can be done in a branchless way using bit manipulation,
		# need to check if python allows sign bit to be explicitly changed
		if decision == 0:
			return (1, 0)
		if decision == 1:
			return (0, 1)
		if decision == 2:
			return (0, -1)
		if decision == 3:
			return (-1, 0)

		
