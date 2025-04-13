import random

def enrich_comic(comic_data, max_views=10000, min_review=1.0, max_review=10.0, cost_per_letter=5):
    # Calculate views between 0 and max_views
    views = int(random.random() * max_views)
    
    # Generate a random review between min_review and max_review
    review = round(random.uniform(min_review, max_review), 1)
    
    # The cost is calculated according to the number of letters in the title.
    cost = len(comic_data['title']) * cost_per_letter
    
    return views, review, cost