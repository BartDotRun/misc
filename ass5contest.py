import exceptions
import numbers
import random
from pacman import agents, gamestate, util, distancer

class ContestAgent(agents.PacmanAgent):
    def prepare(self, gstate):
        super().prepare(gstate)
        self.d = distancer.Distancer(gstate)
        self.d.precompute_distances()

    def move(self, gstate):
        possibleMoves = gstate.legal_moves_id(self.id)
        maxScore = [-float("inf"), None]
        for move in possibleMoves:
            score= self.evaluate(gstate.successor(self.id, move))
            if score > maxScore[0]:
                maxScore[0] = score
                maxScore[1] = move
        return maxScore[1]

    def evaluate(self, gstate: gamestate.Gamestate):

        score=0

        if gstate:
            if gstate.loss:
                return -10000000
            if gstate.win:
                return 100000000
            if len(gstate.dots.list()) > 0:
                min=gstate.dots.list()[0]
                for food in gstate.dots.list():
                    distance= self.d.get_distance(gstate.pacman, food )
                    if distance<self.d.get_distance(gstate.pacman, min):
                        min=food
                score+= -3 * self.d.get_distance(gstate.pacman, min)

            scaredGhost = False
            minGhost = 0
            minScaredGhost = 0
            for i in range(0,len(gstate.ghosts)):
                    distance = self.d.get_distance(gstate.pacman, gstate.ghosts[i])
                    if gstate.timers[i]==0:
                        if distance < self.d.get_distance(gstate.pacman, gstate.ghosts[minGhost]):
                             minGhost = i
                    else:
                        scaredGhost = True
                        if distance < self.d.get_distance(gstate.pacman, gstate.ghosts[minScaredGhost]):
                            minScaredGhost = i
            if  self.d.get_distance(gstate.pacman, gstate.ghosts[minGhost])<2:
                return -10000000
            score += -2 * -self.d.get_distance(gstate.pacman, gstate.ghosts[minGhost])
            if scaredGhost == True:
                if self.d.get_distance(gstate.pacman, gstate.ghosts[minScaredGhost]) != 0:
                    score += 100 * 1/self.d.get_distance(gstate.pacman, gstate.ghosts[minScaredGhost])
                else:
                     score += 10000


            score += len(gstate.dots.list())*(-50)
            score += len(gstate.pellets.list()) *(-20)

        return score
