from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
import collections


class SimilarModel():
    def __init__(self, B_C_mappings, inventery_type='brand'):
        self.mlb = None
        self.similar_brands = {}
        self.unique_categories = set()
        self.B_C_mappings = B_C_mappings
        self.B_C_mappings_binary = collections.defaultdict(dict)
        print(inventery_type + ' similarity model initialised.')
        self.pre_process_mappings()

    def train_multi_binarizer(self, all_features):
        self.mlb = MultiLabelBinarizer()
        self.mlb.fit_transform([all_features])
        return

    def get_binary_features(self, features):
        features = [set(features)]
        binary_features = self.mlb.transform(features)
        return binary_features

    def get_binary_features1(self, features):
        features = [set(features)]
        binary_features = self.mlb.transform([features])
        return binary_features

    def calculate_distance(self, a, b):
        '''
        :param a: Feature vector for brand/category/collection
        :param b: Feature vector for brand/category/collection
        :return: Angular distance between two vectors a and b
        '''
        d = cosine_similarity(a, b)[0][0]
        d = "{0:.4f}".format(d)
        return float(d)

    def get_feature_classes(self):
        return self.mlb.classes_

    def get_sorted_items(self, similarity_scores):
        sorted_items = []

        sorted_dict = sorted(similarity_scores.items(), key=operator.itemgetter(1), reverse=True)
        for k, v in sorted_dict:
            sorted_items.append(k)

        return sorted_items

    def get_unique_categories(self):

        all_categories_list = self.B_C_mappings.values()
        for each_list_el in all_categories_list:
            self.unique_categories.update(each_list_el)

        self.train_multi_binarizer(list(self.unique_categories))
        return self.unique_categories

    # def get_unique_categories_filterwise(self):
    #     filters = ['gender']
    #     filter_values = {'gender':['men','women']}
    #
    #     for each_filter in filter_values:
    #         input_data_keys = self.B_C_mappings.keys()
    #
    #         matched_keys = []
    #
    #         for each_gender in genders:
    #             all_categories_list = self.B_C_mappings.get(each_gender).values()
    #             for each_list_el in all_categories_list:
    #                 self.unique_categories.update(each_list_el)
    #
    #         self.train_multi_binarizer(list(self.unique_categories))
    #         return self.unique_categories


    def pre_process_mappings(self):
        categories = self.get_unique_categories()

        for each_elem in self.B_C_mappings.keys():
            try:
                self.B_C_mappings_binary[each_elem] = self.get_binary_features(self.B_C_mappings.get(each_elem))
            except Exception as ee:
                print('Exception =>',ee)

    def calculate_similarity(self):

        similar_brands = {}
        gender_keys = self.B_C_mappings.keys()

        brands = self.B_C_mappings.keys()
        for each_b in brands:
            similarity_scores = {}
            for each_c in brands:
                if each_c != each_b:
                    dist = self.calculate_distance(self.B_C_mappings_binary.get(each_b),
                                                   self.B_C_mappings_binary.get(each_c))
                    similarity_scores[each_c] = dist
            similar_brands[each_b] = self.get_sorted_items(similarity_scores)
        # self.similar_brands = similar_brands

        return similar_brands
