import requests
from bs4 import BeautifulSoup

def get_cos(ancestor, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.get_text().strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute].strip()
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    "opinion_id": (None, "data-entry-id"),
    "author": ("span.user-post__author-name",),
    "recommendation": ("span.user-post__author-recomendation > em",),
    "stars": ("span.user-post__score-count",),
    "purchased": ("div.review-pz",),
    "opinion_date": ("span.user-post__published > time:nth-child(1)","datetime"),
    "purchase_date": ("span.user-post__published > time:nth-child(2)","datetime"),
    "usefull_count": ("button.vote-yes","data-total-vote"),
    "unusefull_count": ("button.vote-no","data-total-vote"),
    "content": ("div.user-post__text",),
    "pros": ("div.review-feature__title--positives ~ div.review-feature__item", None, True),
    "cons": ("div.review-feature__title--negatives ~ div.review-feature__item", None, True)
}



# product_code = input("Podaj kot produktu: ")
product_code = "39562616"

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"

respons = requests.get(url)
if  respons.status_code == requests.codes.ok:
    page_dom = BeautifulSoup(respons.text, 'html.parser')
    opinions = page_dom.select("div.js_product-review")
    opinions_all = []
    for opinion in opinions:
        single_opinion = {}
        for key, value in selectors.items():
            single_opinion[key] = get_cos(opinion, *value)
        opinions_all.append(single_opinion)
    print(opinions_all)

    # else:
    # print("Nie ma opinii")
        

# kod: 58835954
# r.status_code == request.codes.ok
#   "opinion_id": get_cos(opinion, None, "data-entry-id"),
#             "author": get_cos(opinion, "span.user-post__author-name"),
#             "recommendation": get_cos(opinion, "span.user-post__author-recomendation > em"), 
#             "stars": get_cos(opinion, "span.user-post__score-count"),
#             "purchased": get_cos(opinion, "div.review-pz"),
#             "opinion_date": get_cos(opinion, "span.user-post__published > time:nth-child(1)"),
#             "purchase_date": get_cos(opinion, "span.user-post__published > time:nth-child(2)"),
#             "usefull_count": get_cos(opinion, "button.vote-yes"),
#             "unusefull_count": get_cos(opinion, "button.vote-no"),
#             "content": get_cos(opinion, "div.user-post__text"),
#             "pros": get_cos(opinion, "div.review-featuretitle--positives ~ div.review-featureitem", None, True),
#             "cons": get_cos(opinion, "div.review-featuretitle--negatives ~ div.review-featureitem", None, True) 