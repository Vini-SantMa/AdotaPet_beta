import unittest

from services.recommendations.main import score_pet


class RecommendationScoringTests(unittest.TestCase):
    def setUp(self):
        self.pet = {
            "id": 2,
            "name": "Toto",
            "species": "cat",
            "size": "small",
            "energy_level": "medium",
            "good_with_children": True,
        }
        self.preferences = {
            "species": "any",
            "size": "any",
            "activity_level": "medium",
            "home_type": "apartment",
            "has_children": False,
        }

    def test_open_preferences_can_reach_one_hundred_points(self):
        result = score_pet(self.pet, self.preferences)

        self.assertEqual(result["score"], 100)
        self.assertEqual(result["label"], "Ótima combinação")
        self.assertEqual(len(result["reasons"]), 5)

    def test_one_activity_level_difference_is_explained(self):
        preferences = {**self.preferences, "activity_level": "low"}

        result = score_pet(self.pet, preferences)

        self.assertEqual(result["score"], 89)
        self.assertIn(
            "Considere se o nível de energia combina com a sua rotina.",
            result["reasons"],
        )

    def test_incompatible_profile_is_lower_scored_and_labeled(self):
        pet = {
            **self.pet,
            "size": "large",
            "energy_level": "low",
            "good_with_children": False,
        }
        preferences = {
            **self.preferences,
            "species": "dog",
            "size": "large",
            "activity_level": "high",
            "has_children": True,
        }

        result = score_pet(pet, preferences)

        self.assertEqual(result["score"], 28)
        self.assertEqual(result["label"], "Vale conhecer melhor")
        self.assertIn(
            "O perfil do pet indica cautela na convivência com crianças.",
            result["reasons"],
        )


if __name__ == "__main__":
    unittest.main()
