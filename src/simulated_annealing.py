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
    cooling_rate: float = 0.995,
    return_history: bool = False
):
    # start from one random weekly meal plan
    current = random_initial_plan(recipes)
    current_score = score_meal_plan(current, weights)

    # keep track of the best plan seen so far
    best = current
    best_score = current_score

    # keep track of score history for plotting later
    history = [current_score]

    for _ in range(iterations):
        neighbor = generate_neighbor(current, recipes)
        neighbor_score = score_meal_plan(neighbor, weights)

        delta = neighbor_score - current_score

        # always accept better moves
        if delta > 0:
            current = neighbor
            current_score = neighbor_score
        else:
            # sometimes accept worse moves to escape local optima
            if temperature > 0 and random.random() < math.exp(delta / temperature):
                current = neighbor
                current_score = neighbor_score

        # Update best plan if needed
        if current_score > best_score:
            best = current
            best_score = current_score

        # save the current score after this iteration
        history.append(current_score)

        # slowly lower the temperature
        temperature *= cooling_rate

    # keep old behavior by default, but optionally return history too
    if return_history:
        return best, history

    return best