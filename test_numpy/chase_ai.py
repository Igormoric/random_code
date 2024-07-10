import pygame
import numpy as np
import random
import json
import os
import time

# Configurações iniciais
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CIRCLE_RADIUS = 15
USER_SPEED = 2
AI_SPEED = 2
WEIGHTS_FILE = "best_weights.json"
POPULATION_SIZE = 50  # Número de inimigos por geração
MUTATION_RATE = 0.1
GENERATIONS = 1000

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IA Perseguindo o Usuário")
clock = pygame.time.Clock()

# Função para inicializar pesos da rede neural
def initialize_weights(layer_sizes):
    weights = []
    for i in range(len(layer_sizes)):
        weight = np.random.randn(layer_sizes[i], layer_sizes[i - 1])
        if i == 0:
            weight = np.zeros(layer_sizes[i])
        weights.append(weight)
    return weights

# Função para carregar pesos da rede neural de um arquivo JSON
def load_weights(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            weights = json.load(f)
            weights = [np.array(w) for w in weights]
            return weights
    else:
        return initialize_weights([4, 4, 4, 9])

# Função para salvar pesos da rede neural em um arquivo JSON
def save_weights(weights, file_path):
    with open(file_path, "w") as f:
        weights_list = [w.tolist() for w in weights]
        json.dump(weights_list, f)

# Função para a frente da rede neural
def neural_network(inputs, weights):
    
    activations=np.array([])
    for l2,l3 in enumerate(weights):
        if l2 == 0:
            weights[0]=np.array(inputs,dtype=float)
            activations=np.append(activations,inputs)
            continue
        l=[]
        l5=[]
        for n in l3:
            l4=sum(n*activations[l2-1])
            l5=np.append(l5,(l4))
            
        activations=np.append(activations,l5)

    """
        activations = inputs
    for weight in weights:
        activations = np.dot(activations, weight)
        activations = np.tanh(activations)  # Função de ativação tanh
    return activations

    
    """
    return activations[-1]

# Classe para o círculo controlado pelo usuário
class UserCircle:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - USER_SPEED - CIRCLE_RADIUS > 0:
            self.x -= USER_SPEED
        if keys[pygame.K_RIGHT] and self.x + USER_SPEED + CIRCLE_RADIUS < SCREEN_WIDTH:
            self.x += USER_SPEED
        if keys[pygame.K_UP] and self.y - USER_SPEED - CIRCLE_RADIUS > 0:
            self.y -= USER_SPEED
        if keys[pygame.K_DOWN] and self.y + USER_SPEED + CIRCLE_RADIUS < SCREEN_HEIGHT:
            self.y += USER_SPEED

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), CIRCLE_RADIUS)

# Classe para o círculo controlado pela IA
class AICircle:
    def __init__(self,x,y, weights=None):
        self.x = x
        self.y = y
        self.weights = weights if weights is not None else initialize_weights([4, 4, 4, 9])
        self.score = 0

    def move(self, target_x, target_y):
        inputs = np.array([self.x, self.y, target_x, target_y])
        output = neural_network(inputs, self.weights)
        # Escolhe a direção com maior valor na saída
        direction = np.argmax(output)
        if direction >= 7:
            self.y-=AI_SPEED
        if direction <=3:
            self.y+=AI_SPEED
        if direction % 3 == 0:
            self.x+=AI_SPEED
        if direction % 3 == 2:
            self.x-=AI_SPEED
        """
        if direction == 0 and self.x - AI_SPEED - CIRCLE_RADIUS > 0:
            self.x -= AI_SPEED
        elif direction == 1 and self.x + AI_SPEED + CIRCLE_RADIUS < SCREEN_WIDTH:
            self.x += AI_SPEED
        elif direction == 2 and self.y - AI_SPEED - CIRCLE_RADIUS > 0:
            self.y -= AI_SPEED
        elif direction == 3 and self.y + AI_SPEED + CIRCLE_RADIUS < SCREEN_HEIGHT:
            self.y += AI_SPEED"""

        self.score = 1 / (1 + np.linalg.norm(np.array([self.x, self.y]) - np.array([target_x, target_y])))

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), CIRCLE_RADIUS)

# Função de crossover para combinar os pesos de dois pais
def crossover(weights1, weights2):
    new_weights = []
    for w1, w2 in zip(weights1, weights2):
        mask = np.random.rand(*w1.shape) > 0.5
        new_weight = np.where(mask, w1, w2)
        new_weights.append(new_weight)
    return new_weights

# Função de mutação para alterar aleatoriamente os pesos
def mutate(weights, mutation_rate):
    new_weights = []
    for w in weights:
        if np.random.rand() < mutation_rate:
            w += np.random.randn(*w.shape) * 0.1
        new_weights.append(w)
    return new_weights

# Função principal
def main():
    user_circle = UserCircle()

    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    population = [AICircle(x,y) for _ in range(POPULATION_SIZE)]

    running = True
    generation = 0
    steps=0
    steps_limit=50

    while running and generation < GENERATIONS:
        #time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_weights(population[0].weights, WEIGHTS_FILE)
                running = False

        keys = pygame.key.get_pressed()
        user_circle.move(keys)

        for ai in population:
            ai.move(user_circle.x, user_circle.y)
            if user_circle.x == ai.x and user_circle.y == ai.y:
                steps=0
                generation += 1
                print(f"Generation: {generation}")

                population.sort(key=lambda x: x.score, reverse=True)
                top_performers = population[:5]

                new_population = top_performers.copy()
                while len(new_population) < POPULATION_SIZE:
                    parent1, parent2 = random.sample(top_performers, 2)
                    child_weights = crossover(parent1.weights, parent2.weights)
                    child_weights = mutate(child_weights, MUTATION_RATE)
                    new_population.append(AICircle(x,y,child_weights))

                population = new_population

        screen.fill(WHITE)
        user_circle.draw()
        for ai in population:
            ai.draw()
        pygame.display.flip()

        clock.tick(FPS)

        steps+=1

        if steps > steps_limit :
            steps=0
            generation += 1
            print(f"Generation: {generation}")

            population.sort(key=lambda x: x.score, reverse=True)
            top_performers = population[:5]

            new_population = top_performers.copy()
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = random.sample(top_performers, 2)
                child_weights = crossover(parent1.weights, parent2.weights)
                child_weights = mutate(child_weights, MUTATION_RATE)
                new_population.append(AICircle(x,y,child_weights))

            population = new_population

    pygame.quit()

if __name__ == "__main__":
    main()
