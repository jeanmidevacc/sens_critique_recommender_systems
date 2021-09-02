import ast
import math as mth
import numpy as np

def compute_hit_ratio_at_k(item, recommendations, k):
    if item in recommendations[:k]:
        return 1
    return 0

def compute_ndcg_at_k(item, recommendations, k):
    for idx, elt in enumerate(recommendations[:k]):
        if elt == item:
            return mth.log(2) / mth.log(idx+2)
    return 0

def build_catalog_coverage(recommendations, size_catalog):
    contents = []
    for str_recommendations in recommendations:
        recommendations = ast.literal_eval(str_recommendations)
        new_contents = list(set(recommendations) - set(contents))
        if len(new_contents) > 0:
            contents += new_contents
    return 1.0 * len(contents) / size_catalog

def build_average_year(recommendations, catalog):
    yearids = []
    for contentid in recommendations:
        if contentid in catalog:
            if not np.isnan(catalog[contentid]['year']):
                yearids.append(catalog[contentid]['year'])
                
    if len(yearids) == 0:
        return None
    else:
        return np.mean(yearids)

def build_refresh_rate(model, details, item, rules, k=10):
    category_item = model.catalog[item]['category']
    if category_item not in rules:
        return k
    
    threshold_category_item = rules[model.catalog[item]['category']]
    ranked_items_category = model.build_recommendations_top_k_category(details, category_item, k=k*threshold_category_item)
    
    refresh_rate = k
    
    if item in ranked_items_category:
        return int(ranked_items_category.index(item) / threshold_category_item)
        
    return refresh_rate