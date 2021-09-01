class Recommender:
    def __init__(self, name = '', catalog = {}):
        self.name = name
        self.created_date = datetime.utcnow()
        self.catalog = catalog
        
    def update_ranked_items(self, ranked_items):
        self.ranked_items = ranked_items
        
    def get_ranked_items(self, row):
        return self.ranked_items
        
    def build_recommendations_top_k_overall(self, details, k=25):
        ranked_items = self.get_ranked_items(details)
        inventory = details['historic'].split(',')
        
        recommendations = []
        count = 0
        for item in ranked_items:
            if item not in inventory:
                recommendations.append(item)
                count += 1

            if count == k:
                break
        return recommendations
    
    def build_recommendations_top_k_category(self, details, category, k=25):
        ranked_items = self.get_ranked_items(details)
        inventory = details['historic'].split(',')
        
        recommendations = []
        count = 0
        for item in ranked_items:
            if item not in inventory and self.catalog[item]['category'] == category:
                recommendations.append(item)
                count += 1

            if count == k:
                break
        return recommendations
    
    def build_recommendations_with_rules(self, details, rules):
        ranked_items = self.get_ranked_items(details)
        inventory = details['historic'].split(',')
        
        dict_recommendations = {key : [] for key in rules}
        count_recommendations = 0
        
        # Define the maximum recommendations to return
        threshold_recommendations = 0
        for key, value in rules.items():
            threshold_recommendations += value
            
        for contentid in ranked_items:
            if (contentid in self.catalog) and (contentid not in inventory):
                type_content = self.catalog[contentid]['category']
                
                if type_content in dict_recommendations and len(dict_recommendations[type_content]) < rules[type_content]:
                    dict_recommendations[type_content].append(contentid)
                    count_recommendations += 1

            if count_recommendations == threshold_recommendations:
                break
        
        recommendations = [dict_recommendations[key] for key in rules]
        return list(itertools.chain.from_iterable(recommendations))
    
class RandomRecommender(Recommender):
    def get_ranked_items(self, row):
        new_list = self.ranked_items.copy()
        random.shuffle(new_list)
        return new_list
    
class PreviousContentRecommender(Recommender):
    def build_association(self, dfp_association):
        self.dfp_association = dfp_association
        
    def get_ranked_items(self, row):
        if row.empty :
            ranked_items = self.dfp_association.query(f"previous_contentid == ''").sort_values(['like_score'], ascending=False)['contentid'].tolist()
        else:
            previous_contentid = row['previous_contentid']
            ranked_items = self.dfp_association.query(f"previous_contentid == '{previous_contentid}'").sort_values(['like_score'], ascending=False)['contentid'].tolist()
            if len(ranked_items) == 0:
                ranked_items = self.dfp_association.query(f"previous_contentid == ''").sort_values(['like_score'], ascending=False)['contentid'].tolist()
        return ranked_items