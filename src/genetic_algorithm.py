import random
from typing import List, Dict, Any
from meal_plan import MealPlan
from neighbors import random_initial_plan, generate_neighbor
from scoring import score_meal_plan



# pick a few random plans and keep the best one
def tournament_selection(population, scores, k=3):
    selected = random.sample(range(len(population)), k)
    best_index = max(selected, key=lambda i: scores[i])
    return population[best_index]


# combine two parent meal plans into one child meal plan
def crossover(parent1: MealPlan, parent2: MealPlan) -> MealPlan:
    split = len(parent1.meals) // 2
    child_meals = parent1.meals[:split] + parent2.meals[split:]
    return MealPlan(meals=child_meals)


def genetic_algorithm(
    recipes: List[Dict[str, Any]],
    weights: Dict[str, float],
    population_size: int = 30,
    generations: int = 50,
    mutation_rate: float = 0.2,
    return_history: bool = False
):
    # start with a random population of meal plans
    population = [random_initial_plan(recipes) for _ in range(population_size)]

    # keep track of the best plan seen across the whole run
    best_plan = None
    best_score = float("-inf")

    # store the best score after each generation for plotting
    history = []

    for _ in range(generations):
        # score every plan in the current population
        scores = [score_meal_plan(p, weights) for p in population]

        # track the best plan found so far
        current_best = max(scores)
        if current_best > best_score:
            best_score = current_best
            best_plan = population[scores.index(current_best)].copy()

        # save the best score so far so I can plot convergence later
        history.append(best_score)

        new_population = []

        # Build the next generation one child at a time
        for _ in range(population_size):
            # select two parents using tournament selection
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)

            # create a child by combining the two parents
            child = crossover(parent1, parent2)

            # occasionally mutate the child using the existing neighbor logic
            if random.random() < mutation_rate:
                child = generate_neighbor(child, recipes)

            
            new_population.append(child)

        # replace the old population with the new one
        population = new_population

    # By default return just the best plan
    # If needed for plotting, also return the score history
    if return_history:
        return best_plan, history

    return best_plan