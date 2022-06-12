import logging
from operator import ge
import random as rn
import math
from tqdm import tqdm
from creatures.brain.neurons import ActionNeurons, SensoryNeurons
from creatures.brain.brain import Neuron
from creatures.genome.genome import initialiseRandomGenome
from creatures.creatures import Creature
from creatures.genome.reproduction import generateChildGenome
from logs.frames import convertFramesToVideo, saveFrame
from parameters.paramManager import ParamManager
from world.survival_criterias import getSurvivalCriteria
from world.world import World
from world.world_utils import CREATURE_PRESENT


class Simulator:
    params = None
    world = None
    creatures = None
    survival_criteria: None
    image_count = 1
    # world grid with value 0xFF contains a creature
    def __init__(self, configFile: str):
        self.params = ParamManager(configFileName=configFile).params
        self.world = World(height=self.params.sizeY, width=self.params.sizeX)
        self.survival_criteria = getSurvivalCriteria(self.params)
        self.creatures = []
        for _ in range(self.params.population):
            valid = False
            while not valid:
                x = rn.randint(0, self.params.sizeX-1)
                y = rn.randint(0, self.params.sizeY-1)
                if self.world.grid[x][y] == 0:
                    self.world.grid[x][y] = CREATURE_PRESENT
                    valid = True
            self.creatures.append(
                Creature(
                    genome=initialiseRandomGenome(
                        noOfGenes=rn.randint(
                            self.params.genomeInitialLengthMin,
                            self.params.genomeInitialLengthMax),
                        params=self.params),
                    location=(x,y),
                    last_location=(x,y)
                )
            )

    def simulate(self):
        print("Starting simulation")
        for generation in tqdm(range(self.params.maxGenerations),"Generation: "):
            saveFrame(self.params.imageDir , self.image_count , self.world.grid)
            self.image_count += 1

            for _ in range(self.params.stepsPerGeneration):

                for index in range(len(self.creatures)):

                    self.feed_forward(index=index)
                saveFrame(self.params.imageDir , self.image_count , self.world.grid)
                self.image_count += 1
            self.evaluateSurvival()
            self.spawnNewGeneration()
        print("Completed simulation.\nGenerating video.")
        convertFramesToVideo(self.params.imageDir)

    def spawnNewGeneration(self):
        last_generation = [c  for c in self.creatures if c.alive]
        self.world = World(height=self.params.sizeY, width=self.params.sizeX)
        logging.info("{} alive of {}".format(len(last_generation), len(self.creatures)))
        self.creatures = []
        while len(self.creatures) < self.params.population:
            for creature in last_generation:
                if len(self.creatures) >  self.params.population:
                    return
                valid = False
                while not valid:
                    x = rn.randint(0, self.params.sizeX-1)
                    y = rn.randint(0, self.params.sizeY-1)
                    if self.world.grid[x][y] == 0:
                        self.world.grid[x][y] = CREATURE_PRESENT
                        valid = True
                self.creatures.append(
                    Creature(
                        genome=generateChildGenome(creature.genome,creature.genome, self.params),
                        location=(x,y),
                        last_location=(x,y)
                    )
                )


    def evaluateSurvival(self):
        for index , creature in enumerate(self.creatures):
            if self.survival_criteria[creature.location] == -1:
               self.creatures[index].alive == False 

    # supply creature index
    def feed_forward(self, index: int):
        if self.creatures[index].alive:
            self.creatures[index].age += 1
            for neurons in self.creatures[index].brain.wirings:
                try:
                    input = self.getInput(neurons[0], index)
                    action, result = self.getAction(neurons=neurons, input=input)
                    self.executeAction(action, result, index)
                except:
                    pass


    def getInput(self, neuron: Neuron, index: int):
        if neuron.source is SensoryNeurons.LOC_X:
            return self.creatures[index].location[0]
        elif neuron.source is SensoryNeurons.LOC_Y:
            return self.creatures[index].location[1]
        elif neuron.source is SensoryNeurons.W:
            result = 0
            cst = index - 2
            rst = index - 2
            ced = index + 2
            red = index + 2
            if cst < 0:
                cst = 0
            if rst < 0:
                rst = 0
            if ced >= self.params.sizeX:
                ced = self.params.sizeX - 1
            if red >= self.params.sizeY:
                red = self.params.sizeY - 1
            for r in range(rst, red):
                for c in range(cst, ced):
                    if self.world.grid[r][c] == CREATURE_PRESENT:
                        result += 1
            return result / ((ced - cst) * (red - rst))
        elif neuron.source is SensoryNeurons.AGE:
            return self.creatures[index].age
        elif neuron.source is SensoryNeurons.LAST_MOVE_X:
            return self.creatures[index].last_location[0]
        elif neuron.source is SensoryNeurons.LAST_MOVE_Y:
            return self.creatures[index].last_location[1]
        else:
            logging.debug("Incorrect Wiring: Sensory")
            raise

    def getAction(self, neurons: list, input: float):
        result = math.tanh(input)
        for neuron in neurons:
            if type(neuron.sink) is ActionNeurons:
                result = math.tanh(result*neuron.weight)
            else:
                result = 4*math.acosh(result*neuron.weight)

        return neurons[-1].sink, result

    def executeAction(self, action: ActionNeurons, result: float , index: int):
        if result < 0.5:
            return None
        
        if action is ActionNeurons.MOV_D:
            last_location = self.creatures[index].location
            if last_location[1] == self.params.sizeY-1:
                return
            new_location = (last_location[0],last_location[1]+1)

            while self.world.grid[new_location] == CREATURE_PRESENT:
                if new_location[1] == self.params.sizeY-1:
                    return
                new_location = (new_location[0],new_location[1]+1)

            self.creatures[index].last_location = last_location
            self.creatures[index].location = new_location
            self.world.grid[last_location] = 0
            self.world.grid[new_location] = CREATURE_PRESENT
        elif action is ActionNeurons.MOV_L:
            last_location = self.creatures[index].location
            if last_location[0] == 0:
                return
            new_location = (last_location[0]-1,last_location[1])

            while self.world.grid[new_location] == CREATURE_PRESENT:
                if new_location[0] == 0:
                    return
                new_location = (new_location[0]-1,new_location[1])

            self.creatures[index].last_location = last_location
            self.creatures[index].location = new_location
            self.world.grid[last_location] = 0
            self.world.grid[new_location] = CREATURE_PRESENT
        elif action is ActionNeurons.MOV_R:
            last_location = self.creatures[index].location
            if last_location[0] == self.params.sizeX-1:
                return
            new_location = (last_location[0]+1,last_location[1])

            while self.world.grid[new_location] == CREATURE_PRESENT:
                if new_location[0] == self.params.sizeX-1:
                    return
                new_location = (new_location[0]+1,new_location[1])

            self.creatures[index].last_location = last_location
            self.creatures[index].location = new_location
            self.world.grid[last_location] = 0
            self.world.grid[new_location] = CREATURE_PRESENT
        elif action is ActionNeurons.MOV_U:
            last_location = self.creatures[index].location
            if last_location[1] == 0:
                return
            new_location = (last_location[0],last_location[1]-1)
            while self.world.grid[new_location] == CREATURE_PRESENT:
                if new_location[1] == 0:
                    return
                new_location = (new_location[0],new_location[1]-1)
            self.creatures[index].last_location = last_location
            self.creatures[index].location = new_location
            self.world.grid[last_location] = 0
            self.world.grid[new_location] = CREATURE_PRESENT
        elif action is ActionNeurons.MOV_Rn:
            direction = rn.randint(0,255)
            if direction % 4 == 0:
                self.executeAction(ActionNeurons.MOV_D,result,index)
            elif direction % 4 == 1:
                self.executeAction(ActionNeurons.MOV_L,result,index)
            elif direction % 4 == 2:
                self.executeAction(ActionNeurons.MOV_R,result,index)
            else:
                self.executeAction(ActionNeurons.MOV_U,result,index)
            
        elif action is ActionNeurons.KILL:
            pass
        else:
            logging.debug("Incorrect Wiring: Action")
            raise

    