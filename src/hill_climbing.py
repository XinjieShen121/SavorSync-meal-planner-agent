from typing import List, Dict, Any
from meal_plan import MealPlan
from neighbors import random_initial_plan, generate_neighbor
from scoring import score_meal_plan


def hill_climb(
    recipes: List[Dict[str, Any]],
    weights: Dict[str, float],
    iterations: int = 500,
    return_history: bool = False
):
    # start with one random weekly meal plan
    current = random_initial_plan(recipes)

    # score that starting plan so we have something to compare against
    current_score = score_meal_plan(current, weights)

    # keep track of score history for plotting later
    history = [current_score]

    #  try to improve the current plan one move at a time
    for _ in range(iterations):
        # generate one neighboring plan by making a small change
        neighbor = generate_neighbor(current, recipes)
        neighbor_score = score_meal_plan(neighbor, weights)

        # Hill climbing only accepts a move if it improves the score
        if neighbor_score > current_score: # Hill climbing is greedy
            current = neighbor
            current_score = neighbor_score

        # record the current score after each iteration
        history.append(current_score)  # if no better move was found, the score stays the same

    # Keep old behavior by default, but optionally return history too
    if return_history:
        return current, history

    return current