from typing import List, Dict, Any
from meal_plan import MealPlan
from neighbors import random_initial_plan, generate_neighbor
from scoring import score_meal_plan


def hill_climb(
    recipes: List[Dict[str, Any]],
    weights: Dict[str, float],
    iterations: int = 500
) -> MealPlan:
    # Start with one random weekly meal plan
    current = random_initial_plan(recipes)  # initial state in the search space

    # Evaluate how good the starting meal plan is 
    # using the weighted utility / scoring function
    current_score = score_meal_plan(current, weights)

    # Try to improve the plan step by step
    for _ in range(iterations):
        # Create a nearby plan by making a small change such as replacing or swapping meals
        neighbor = generate_neighbor(current, recipes)

        # Score the new candidate plan
        neighbor_score = score_meal_plan(neighbor, weights)

        # Hill climbing only accepts the new plan if it's better than the current one
        if neighbor_score > current_score:
            current = neighbor
            current_score = neighbor_score

    return current # return the best plan reached by repeated local improvement