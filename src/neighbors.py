
import random
from typing import List, Dict, Any
from meal_plan import MealPlan


def random_initial_plan(recipes: List[Dict[str, Any]], plan_size: int = 10) -> MealPlan:
    # build a random starting meal plan using unique recipes.
    if len(recipes) < plan_size:
        raise ValueError("Not enough recipes to create an initial plan.")
    chosen = random.sample(recipes, plan_size)
    return MealPlan(meals=chosen)


def replace_one_meal(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # replace one meal with a different recipe, preferably one not already used.
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current_meal = neighbor.meals[idx]

    used_ids = {meal["id"] for meal in neighbor.meals}
    candidates = [r for r in recipes if r["id"] != current_meal["id"] and r["id"] not in used_ids]

    # if all unused recipes are exhausted, allow any different recipe.
    if not candidates:
        candidates = [r for r in recipes if r["id"] != current_meal["id"]]

    if candidates:
        neighbor.meals[idx] = random.choice(candidates)

    return neighbor


def swap_two_meals(plan: MealPlan) -> MealPlan:
    # swap two meal positions in the plan.
    neighbor = plan.copy()
    i, j = random.sample(range(len(neighbor.meals)), 2)
    neighbor.meals[i], neighbor.meals[j] = neighbor.meals[j], neighbor.meals[i]
    return neighbor


def replace_with_same_cuisine(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # replace one meal with another meal from the same cuisine.
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current_meal = neighbor.meals[idx]

    used_ids = {meal["id"] for meal in neighbor.meals}
    same_cuisine = [
        r for r in recipes
        if r["cuisine"] == current_meal["cuisine"]
        and r["id"] != current_meal["id"]
        and r["id"] not in used_ids
    ]

    # If there are no unused options, allow any other meal from the same cuisine
    if not same_cuisine:
        same_cuisine = [
            r for r in recipes
            if r["cuisine"] == current_meal["cuisine"]
            and r["id"] != current_meal["id"]
        ]

    if same_cuisine:
        neighbor.meals[idx] = random.choice(same_cuisine)

    return neighbor


def replace_with_different_cuisine(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # replace one meal with something from a different cuisine.
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current_meal = neighbor.meals[idx]

    used_ids = {meal["id"] for meal in neighbor.meals}
    different_cuisine = [
        r for r in recipes
        if r["cuisine"] != current_meal["cuisine"]
        and r["id"] not in used_ids
    ]

    # If no unused options exist, allow any meal from a different cuisine
    if not different_cuisine:
        different_cuisine = [r for r in recipes if r["cuisine"] != current_meal["cuisine"]]

    if different_cuisine:
        neighbor.meals[idx] = random.choice(different_cuisine)

    return neighbor


def reduce_prep_time(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # find the longest-prep meal and replace it with a quicker unused option.
    neighbor = plan.copy()
    idx = max(range(len(neighbor.meals)), key=lambda i: neighbor.meals[i]["prep_time"])
    current_meal = neighbor.meals[idx]

    used_ids = {meal["id"] for meal in neighbor.meals}
    better_options = [
        r for r in recipes
        if r["prep_time"] < current_meal["prep_time"]
        and r["id"] != current_meal["id"]
        and r["id"] not in used_ids
    ]

     # If no unused faster meals exist, allow any faster meal
    if not better_options:
        better_options = [
            r for r in recipes
            if r["prep_time"] < current_meal["prep_time"]
            and r["id"] != current_meal["id"]
        ]

    if better_options:
        neighbor.meals[idx] = random.choice(better_options)

    return neighbor


def improve_diversity(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # replace a duplicate meal with an unused recipe to improve meal diversity.
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


def improve_vegetables(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # replace the lowest-vegetable meal with a higher-vegetable option.
    neighbor = plan.copy()
    idx = min(range(len(neighbor.meals)), key=lambda i: neighbor.meals[i]["nutrition"]["vegetables"])
    current_meal = neighbor.meals[idx]

    used_ids = {meal["id"] for meal in neighbor.meals}
    better_options = [
        r for r in recipes
        if r["nutrition"]["vegetables"] > current_meal["nutrition"]["vegetables"]
        and r["id"] != current_meal["id"]
        and r["id"] not in used_ids
    ]

    # If no unused better option exists, allow any higher-vegetable recipe
    if not better_options:
        better_options = [
            r for r in recipes
            if r["nutrition"]["vegetables"] > current_meal["nutrition"]["vegetables"]
            and r["id"] != current_meal["id"]
        ]

    if better_options:
        neighbor.meals[idx] = random.choice(better_options)

    return neighbor


def culturally_similar_substitution(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # replace one meal with a culturally related option.
    neighbor = plan.copy()
    idx = random.randrange(len(neighbor.meals))
    current = neighbor.meals[idx]

    # These groups are not perfect, but they let the planner make substitutions
    # that still feel somewhat culturally connected
    cuisine_groups = {
        "Chinese": ["Chinese", "Japanese", "Korean", "Vietnamese"],
        "Japanese": ["Japanese", "Chinese", "Korean", "Vietnamese"],
        "Korean": ["Korean", "Chinese", "Japanese"],
        "Indian": ["Indian", "Thai", "Middle Eastern"],
        "Thai": ["Thai", "Vietnamese", "Indian"],
        "Vietnamese": ["Vietnamese", "Thai", "Chinese", "Japanese"],
        "Mexican": ["Mexican", "South American", "American"],
        "American": ["American", "Mexican", "Mediterranean"],
        "Greek": ["Greek", "Mediterranean", "Middle Eastern", "Italian"],
        "Italian": ["Italian", "French", "Greek", "Mediterranean"],
        "French": ["French", "Italian", "German"],
        "Middle Eastern": ["Middle Eastern", "Greek", "Mediterranean", "Indian"],
        "Mediterranean": ["Mediterranean", "Greek", "Italian", "Middle Eastern"],
        "African": ["African", "Middle Eastern", "Mediterranean"],
        "South American": ["South American", "Mexican", "American"],
        "Spanish": ["Spanish", "Mediterranean", "Italian"],
        "German": ["German", "French", "American"]
    }

    allowed_cuisines = cuisine_groups.get(current["cuisine"], [current["cuisine"]])

    used_ids = {meal["id"] for meal in neighbor.meals}
    candidates = [
        r for r in recipes
        if r["cuisine"] in allowed_cuisines
        and r["id"] != current["id"]
        and r["id"] not in used_ids
    ]

    # If no unused candidates are available, allow any meal from the related group
    if not candidates:
        candidates = [
            r for r in recipes
            if r["cuisine"] in allowed_cuisines
            and r["id"] != current["id"]
        ]

    if candidates:
        neighbor.meals[idx] = random.choice(candidates)

    return neighbor


def generate_neighbor(plan: MealPlan, recipes: List[Dict[str, Any]]) -> MealPlan:
    # Randomly choose one type of search move
    action = random.choice([
        "replace",
        "swap",
        "same_cuisine",
        "different_cuisine",
        "reduce_prep",
        "improve_diversity",
        "improve_vegetables",
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
    if action == "improve_vegetables":
        return improve_vegetables(plan, recipes)
    if action == "cultural_sub":
        return culturally_similar_substitution(plan, recipes)

    # Fallback case, though in practice one of the actions above should always run
    return plan.copy()