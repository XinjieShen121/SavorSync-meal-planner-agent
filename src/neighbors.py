import random
from typing import List, Dict, Any
from meal_plan import MealPlan


def random_initial_plan(recipes: List[Dict[str, Any]], plan_size: int = 10) -> MealPlan:
    # Build a random starting meal plan using unique recipes
    if len(recipes) < plan_size:
        raise ValueError("Not enough recipes to create an initial plan.")
    chosen = random.sample(recipes, plan_size)
    return MealPlan(meals=chosen)


def replace_one_meal(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    neighbor = plan.copy() # Make a copy

    # Pick one random meal slot and replace it with a random recipe
    idx = random.randrange(len(neighbor.meals))
    neighbor.meals[idx] = random.choice(recipes)
    return neighbor


def swap_two_meals(plan: MealPlan) -> MealPlan:
    neighbor = plan.copy()

    # Pick two positions and swap them
    i, j = random.sample(range(len(neighbor.meals)), 2)
    neighbor.meals[i], neighbor.meals[j] = neighbor.meals[j], neighbor.meals[i]
    return neighbor


def replace_with_same_cuisine(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # Replace one meal with another from the same cuisine
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current_meal = neighbor.meals[idx]
    same_cuisine = [r for r in recipes if r["cuisine"] == current_meal["cuisine"] and r["id"] != current_meal["id"]]

    if same_cuisine:
        neighbor.meals[idx] = random.choice(same_cuisine)

    return neighbor


def replace_with_different_cuisine(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # Replace one meal with something from a different cuisine
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current_meal = neighbor.meals[idx]
    different_cuisine = [r for r in recipes if r["cuisine"] != current_meal["cuisine"]]

    if different_cuisine:
        neighbor.meals[idx] = random.choice(different_cuisine)

    return neighbor


def reduce_prep_time(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # Find the meal with the longest prep time and try to replace it
    neighbor = plan.copy()
    idx = max(range(len(neighbor.meals)), key=lambda i: neighbor.meals[i]["prep_time"])
    current_meal = neighbor.meals[idx]

    better_options = [
        r for r in recipes
        if r["prep_time"] < current_meal["prep_time"]
    ]

    if better_options:
        neighbor.meals[idx] = random.choice(better_options)

    return neighbor


def improve_diversity(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # Find duplicate meals and try to replace one with a new recipe
    neighbor = plan.copy()
    names = [meal["name"] for meal in neighbor.meals]

    duplicates = [name for name in set(names) if names.count(name) > 1]
    if not duplicates:
        return neighbor

    duplicate_name = random.choice(duplicates)
    duplicate_indices = [i for i, meal in enumerate(neighbor.meals) if meal["name"] == duplicate_name]
    idx = random.choice(duplicate_indices)

    used_ids = {meal["id"] for meal in neighbor.meals}
    replacement_candidates = [r for r in recipes if r["id"] not in used_ids]

    if replacement_candidates:
        neighbor.meals[idx] = random.choice(replacement_candidates)

    return neighbor


def culturally_similar_substitution(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    """
    A simple heuristic:
    replace one meal with another from the same cuisine,
    or from a cuisine that is somewhat regionally similar.
    """
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current = neighbor.meals[idx]

    cuisine_groups = {
        "Chinese": ["Chinese", "Japanese", "Korean"],
        "Japanese": ["Japanese", "Chinese", "Korean"],
        "Korean": ["Korean", "Chinese", "Japanese"],
        "Indian": ["Indian", "Thai", "Middle Eastern"],
        "Thai": ["Thai", "Vietnamese", "Indian"],
        "Vietnamese": ["Vietnamese", "Thai", "Chinese"],
        "Mexican": ["Mexican", "American"],
        "American": ["American", "Mexican"],
        "Greek": ["Greek", "Middle Eastern", "Italian"],
        "Italian": ["Italian", "French", "Greek"],
        "French": ["French", "Italian"],
        "Middle Eastern": ["Middle Eastern", "Greek", "Indian"]
    }

    allowed_cuisines = cuisine_groups.get(current["cuisine"], [current["cuisine"]])

    candidates = [
        r for r in recipes
        if r["cuisine"] in allowed_cuisines and r["id"] != current["id"]
    ]

    if candidates:
        neighbor.meals[idx] = random.choice(candidates)

    return neighbor


def generate_neighbor(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # Randomly choose one type of neighbor-generation action
    action = random.choice([
        "replace",
        "swap",
        "same_cuisine",
        "different_cuisine",
        "reduce_prep",
        "improve_diversity",
        "cultural_sub"
    ])

    if action == "replace":
        return replace_one_meal(plan, recipes)
    if action == "swap":
        return swap_two_meals(plan)
    if action == "same_cuisine":
        return replace_with_same_cuisine(plan, recipes)
    if action == "different_cuisine":
        return replace_with_different_cuisine(plan, recipes)
    if action == "reduce_prep":
        return reduce_prep_time(plan, recipes)
    if action == "improve_diversity":
        return improve_diversity(plan, recipes)
    if action == "cultural_sub":
        return culturally_similar_substitution(plan, recipes)

    return plan.copy()