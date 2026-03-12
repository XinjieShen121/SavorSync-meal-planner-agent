import math
import random
from typing import List, Dict, Any
from meal_plan import MealPlan
from neighbors import random_initial_plan, generate_neighbor
from scoring import score_meal_plan


def simulated_annealing(
    recipes: List[Dict[str, Any]],
    weights: Dict[str, float],
    iterations: int = 1000,
    temperature: float = 10.0,
    cooling_rate: float = 0.995
) -> MealPlan:
    # Start with one random weekly meal plan
    current = random_initial_plan(recipes)

    # Score the initial plan
    current_score = score_meal_plan(current, weights)


    best = current # keep track of the best plan found so far
    best_score = current_score

    # Try to improve the plan over iteration
    for _ in range(iterations):
         # Generate a nearby candidate plan
        neighbor = generate_neighbor(current, recipes)

        # Score the candidate plan
        neighbor_score = score_meal_plan(neighbor, weights)

        # Compute the score difference
        delta = neighbor_score - current_score

        # Always accept better neighbors
        if delta > 0:
            current = neighbor
            current_score = neighbor_score
        else:
            # Sometimes accept a worse neighbor with a probability that decreases over time (simulated annealing)
            if temperature > 0 and random.random() < math.exp(delta / temperature):
                current = neighbor
                current_score = neighbor_score

        # Update the best plan seen so far
        if current_score > best_score:
            best = current
            best_score = current_score

        # Gradually lower the temperature to reduce the chance of accepting worse solutions as the search progresses
        temperature *= cooling_rate

    return best # return the best meal plan