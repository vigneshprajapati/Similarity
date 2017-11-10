from ..model_templates.model import Model
from ..scoring_models.similarity import SimilarModel


class Apple(Model):
    def __init__(self, bc_mappings, inventory_type):
        self.set_name("Apple")
        self.brand_category_model = SimilarModel(bc_mappings, i_type)

    def calculate_similar_inventory(self):
        similar_inventory = self.brand_category_model.calculate_similarity()
        return similar_inventory

    def gain(self):
        pass

    def loss(self):
        pass
