import snake
import constant as const
import pygame
import os
import neat
import time

genCount = 0

def eval_genomes(genomes, config):
	fittestScore = 0
	seed = 214#time.time_ns()	# Seeding the snake game gives control over the randomness
	for genome_id, genome in genomes:
		fittestScore = max(eval_fitness(genome, config, seed=seed), fittestScore)
	global genCount
	genCount += 1
	print("Fittest genome in generation {:d} got a score of:{:d}".format(genCount, fittestScore))

def eval_fitness(genome, config, seed=None):
	net = neat.nn.FeedForwardNetwork.create(genome, config)
	if(seed != None):
		snakeGame = snake.Board(const.X_GRID_SIZE, const.Y_GRID_SIZE, drawMode=False, maxTurns=40, seed=seed)
	else:
		snakeGame = snake.Board(const.X_GRID_SIZE, const.Y_GRID_SIZE, drawMode=False, maxTurns=40)

	decision = maxActivatedDecision(net.activate(snakeGame.gridToSnakeSightInput()))
	finalScore, grid = snakeGame.headlessNextState(decision)
	while finalScore == -1:
		decision = maxActivatedDecision(net.activate(grid))
		finalScore, grid = snakeGame.headlessNextState(decision)

	genome.fitness = finalScore#-(snakeGame.snake.turns/100)	#possibly punish for taking longer?
	return finalScore

def maxActivatedDecision(decisionList):
	highestVal = 0
	idxOfHighest = 0
	for i, value in enumerate(decisionList):
		if value > highestVal:
			highestVal = value
			idxOfHighest = i
	return idxOfHighest

def train():
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward')

	# Load configuration.
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						neat.DefaultSpeciesSet, neat.DefaultStagnation,
						config_path)
						
	p = neat.Population(config)
	#p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-2199')	#to start from a checkpointed generation
	p.add_reporter(neat.Checkpointer(100))	#to checkpoint generations

	winner = p.run(eval_genomes, 200)
	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
	drawAgentDecisions(winner_net)
	print(winner)

def drawAgentDecisions(net):
	screen = pygame.display.set_mode([const.SCREEN_WIDTH, const.SCREEN_HEIGHT])
	boardSurface = pygame.Surface((const.SCREEN_WIDTH-2*const.BORDER, const.SCREEN_HEIGHT-2*const.BORDER))
	snakeGame = snake.Board(7,7, drawMode=True)#, seed=56887654)
	snakeGame.drawInit(boardSurface)
	snakeGame.draw()
	screen.blit(boardSurface, (const.BORDER, const.BORDER))
	decision = maxActivatedDecision(net.activate(snakeGame.gridToSnakeSightInput()))
	finalScore, grid = snakeGame.headlessNextState(decision, clocktime=const.GAME_SPEED)
	while finalScore == -1:
		decision = maxActivatedDecision(net.activate(grid))
		finalScore, grid = snakeGame.headlessNextState(decision, clocktime=const.GAME_SPEED)
		snakeGame.draw()
		screen.blit(boardSurface, (const.BORDER, const.BORDER))
		if pygame.event.peek(pygame.QUIT):
			running = False
			pygame.event.clear()
		pygame.display.flip()
	print(finalScore)

if __name__ == '__main__':
	train()