import numpy as np
from scipy.special import softmax

# Define the problem parameters
num_activities = 10
num_rooms = 9
num_timeslots = 6
num_facilitators = 10
population_size = 500
num_generations = 100

# Define the activity information
activities = [
    {"name": "SLA100A", "expected_enrollment": 50, "preferred_facilitators": [0, 1, 2, 5], "other_facilitators": [8, 3]},
    {"name": "SLA100B", "expected_enrollment": 50, "preferred_facilitators": [0, 1, 2, 5], "other_facilitators": [8, 3]},
    {"name": "SLA191A", "expected_enrollment": 50, "preferred_facilitators": [0, 1, 2, 5], "other_facilitators": [8, 3]},
    {"name": "SLA191B", "expected_enrollment": 50, "preferred_facilitators": [0, 1, 2, 5], "other_facilitators": [8, 3]},
    {"name": "SLA201", "expected_enrollment": 50, "preferred_facilitators": [0, 2, 5, 4], "other_facilitators": [8, 3, 6]},
    {"name": "SLA291", "expected_enrollment": 50, "preferred_facilitators": [1, 2, 5, 6], "other_facilitators": [8, 3, 4, 7]},
    {"name": "SLA303", "expected_enrollment": 60, "preferred_facilitators": [0, 5, 2], "other_facilitators": [8, 6, 4]},
    {"name": "SLA304", "expected_enrollment": 25, "preferred_facilitators": [0, 2, 7], "other_facilitators": [8, 6, 4, 3, 9, 5]},
    {"name": "SLA394", "expected_enrollment": 20, "preferred_facilitators": [7, 6], "other_facilitators": [3, 5]},
    {"name": "SLA449", "expected_enrollment": 60, "preferred_facilitators": [7, 6, 4], "other_facilitators": [5, 9]},
    {"name": "SLA451", "expected_enrollment": 100, "preferred_facilitators": [7, 6, 4], "other_facilitators": [5, 9, 3, 2]}
]

# Define the room information
rooms = [
    {"name": "Slater 003", "capacity": 45},
    {"name": "Roman 216", "capacity": 30},
    {"name": "Loft 206", "capacity": 75},
    {"name": "Roman 201", "capacity": 50},
    {"name": "Loft 310", "capacity": 108},
    {"name": "Beach 201", "capacity": 60},
    {"name": "Beach 301", "capacity": 75},
    {"name": "Logos 325", "capacity": 450},
    {"name": "Frank 119", "capacity": 60}
]

# Define the fitness function
def calculate_fitness(schedule):
    fitness = 0
    for i, (room, timeslot, facilitator) in enumerate(schedule):
        activity = activities[i]

        # Check for activity conflicts
        for j, (other_room, other_timeslot, _) in enumerate(schedule):
            if i != j and other_timeslot == timeslot and other_room == room:
                fitness -= 0.5

        # Check room size
        room_capacity = rooms[room]["capacity"]
        if activity["expected_enrollment"] > room_capacity:
            fitness -= 0.5
        elif room_capacity > 3 * activity["expected_enrollment"]:
            fitness -= 0.2
        elif room_capacity > 6 * activity["expected_enrollment"]:
            fitness -= 0.4
        else:
            fitness += 0.3

        # Check facilitator preferences
        if facilitator in activity["preferred_facilitators"]:
            fitness += 0.5
        elif facilitator in activity["other_facilitators"]:
            fitness += 0.2
        else:
            fitness -= 0.1

        # Check facilitator load
        facilitator_load = sum(1 for _, _, f in schedule if f == facilitator)
        if facilitator_load == 1:
            fitness += 0.2
        elif facilitator_load > 1:
            fitness -= 0.2
        if facilitator_load > 4:
            fitness -= 0.5
        if facilitator_load < 3 and facilitator == 7:  # Dr. Tyler exception
            fitness -= 0.4

        # Check activity-specific adjustments
        for j, (_, other_timeslot, _) in enumerate(schedule):
            if activity["name"] == "SLA101A" and activities[j]["name"] == "SLA101B":
                if abs(timeslot - other_timeslot) > 4:
                    fitness += 0.5
                else:
                    fitness -= 0.5
            if activity["name"] == "SLA191A" and activities[j]["name"] == "SLA191B":
                if abs(timeslot - other_timeslot) > 4:
                    fitness += 0.5
                else:
                    fitness -= 0.5
            if (activity["name"] == "SLA191A" or activity["name"] == "SLA191B") and (activities[j]["name"] == "SLA101A" or activities[j]["name"] == "SLA101B"):
                if abs(timeslot - other_timeslot) == 1:
                    if (room in [1, 7] and other_room not in [1, 7]) or (room not in [1, 7] and other_room in [1, 7]):
                        fitness -= 0.4
                    else:
                        fitness += 0.5
                elif abs(timeslot - other_timeslot) == 2:
                    fitness += 0.25
                else:
                    fitness -= 0.25

    return fitness

# Initialize the population
population = [
    [(np.random.randint(num_rooms), np.random.randint(num_timeslots), np.random.randint(num_facilitators))
     for _ in range(num_activities)]
    for _ in range(population_size)
]

# Run the genetic algorithm
mutation_rate = 0.01
for generation in range(num_generations):
    # Evaluate fitness
    fitness_scores = [calculate_fitness(schedule) for schedule in population]
    fitness_probs = softmax(fitness_scores)

    # Select parents
    parents = np.random.choice(population_size, size=(2,), p=fitness_probs)

    # Crossover
    offspring = [population[parents[0]], population[parents[1]]]

    # Mutate
    for i in range(len(offspring)):
        if np.random.rand() < mutation_rate:
            offspring[i][np.random.randint(num_activities)] = (
                np.random.randint(num_rooms),
                np.random.randint(num_timeslots),
                np.random.randint(num_facilitators)
            )

    # Replace the least fit individuals
    worst_indices = np.argsort(fitness_scores)[:2]
    population[worst_indices[0]] = offspring[0]
    population[worst_indices[1]] = offspring[1]

    # Adjust the mutation rate
    if generation % 10 == 0 and generation > 0:
        mutation_rate /= 2

# Print the best schedule
best_schedule = population[np.argmax(fitness_scores)]
print("Best Schedule:")
for i, (room, timeslot, facilitator) in enumerate(best_schedule):
    print(f"{activities[i]['name']} - Room: {rooms[room]['name']}, Time: {timeslot}, Facilitator: {facilitator}")
