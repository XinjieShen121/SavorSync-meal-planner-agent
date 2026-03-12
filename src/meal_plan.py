from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MealPlan:
    # a mealplan object stores one full weekly meal plan
    meals: List[Dict[str, Any]]

    def copy(self) -> "MealPlan":
        return MealPlan(meals=[meal.copy() for meal in self.meals]) # create a deep copy of the meal plan to avoid mutating the original when generating neighbors