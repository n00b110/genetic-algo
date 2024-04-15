import random
import numpy as np

# Constants
NUM_ACTIVITIES = 10
NUM_ROOMS = 9
NUM_TIMES = 6
POPULATION_SIZE = 500
GENERATIONS = 100
MUTATION_RATE = 0.01

# Data structures
activities = [
    {"name": "SLA100A", "enrollment": 50, "preferred": ["Glen", "Lock", "Banks", "Zeldin"], "other": ["Numen", "Richards"]},
    {"name": "SLA100B", "enrollment": 50, "preferred": ["Glen", "Lock", "Banks", "Zeldin"], "other": ["Numen", "Richards"]},
    # Add all other activities here...
]

rooms = [
    {"name": "Slater 003", "capacity": 45},
    {"name": "Roman 216", "capacity": 30},
    # Add all other rooms here...
]

times = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

# Fitness function
def calculate_fitness(schedule):
    fitness = 0
    # Implement fitness calculation based on the detailed rules in the document
    return fitness

# Initialization of population
def initialize_population():
    population = []
    for _ in range(POPULATION_SIZE):
        schedule = [{"activity": random.choice(activities), "room": random.choice(rooms), "time": random.choice(times)} for _ in range(NUM_ACTIVITIES)]
        population.append(schedule)
    return population

# Selection
def selection(population):
    fitness_scores = [calculate_fitness(individual) for individual in population]
    probabilities = np.exp(fitness_scores) / np.sum(np.exp(fitness_scores))
    selected_indices = np.random.choice(range(POPULATION_SIZE), size=POPULATION_SIZE, replace=True, p=probabilities)
    return [population[i] for i in selected_indices]

# Crossover
def crossover(parent1, parent2):
    child = []
    for i in range(NUM_ACTIVITIES):
        if random.random() > 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# Mutation
def mutate(individual):
    for i in range(NUM_ACTIVITIES):
        if random.random() < MUTATION_RATE:
            individual[i] = {"activity": random.choice(activities), "room": random.choice(rooms), "time": random.choice(times)}

# Main GA loop
population = initialize_population()
for generation in range(GENERATIONS):
    selected = selection(population)
    next_generation = []
    for i in range(0, POPULATION_SIZE, 2):
        parent1 = selected[i]
        parent2 = selected[i + 1]
        child1 = crossover(parent1, parent2)
        child2 = crossover(parent1, parent2)
        mutate(child1)
        mutate(child2)
        next_generation.extend([child1, child2])
    population = next_generation
    # Evaluate the population and possibly update mutation rate, etc.

# Output the best schedule
best_individual = max(population, key=calculate_fitness)
print("Best Schedule Fitness:", calculate_fitness(best_individual))
for entry in best_individual:
    print(f"Activity: {entry['activity']['name']}, Room: {entry['room']['name']}, Time: {entry['time']}")

