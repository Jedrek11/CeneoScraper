import requests
from bs4 import BeautifulSoup


# product_code = input("Podaj kot produktu: ")
product_code = '58835954'


URL = f"https://www.ceneo.pl/{product_code}#tab=reviews"
res = requests.get(URL)


if res.status_code == requests.codes.ok:
    page_DOM = BeautifulSoup(res.text, 'html.parser')
    opinions_DOM = page_DOM.select("div.js_product-review")
    
    if len(opinions_DOM) > 0:
        opinions_all = []
        print(opinions_DOM)
        for opinion in opinions_DOM:
            single_opinion = {
                "opinion_id": opinion["data-entry-id"],
                "author": opinion.select_one("span.user-post__author-name").get_text().strip(),
                "recommendation": opinion.select_one("span.user-post__author-recomendation > em").get_text().strip(), 
                "stars": opinion.select_one("span.user-post__score-count").get_text().strip(),
                "purchased": opinion.select_one("div.review-pz").get_text().strip(),
                "opinion_date": opinion.select_one("span.user-post__published > time:nth-child(1)")['datetime'].strip(),
                "purchase_date": opinion.select_one("span.user-post__published > time:nth-child(2)")['datetime'].strip(),
                "usefull_count": opinion.select_one("button.vote-yes")["data-total-vote"].strip(),
                "unusefull_count": opinion.select_one("button.vote-no")["data-total-vote"].strip(),
                "content": opinion.select_one("div.user-post__text").get_text().strip(),
                "pros": [p.get_text().strip() for p in opinion.select("div.review-feature__title--positives ~ div.review-feature__item")],
                "cons": [p.get_text().strip() for p in opinion.select("div.review-feature__title--negatives ~ div.review-feature__item")] 
            }
        opinions_all.append(single_opinion)
        print(opinions_all)
    else:
        print("Nie ma opinii")
 

    # else:
    # print("Nie ma opinii")
        

# kod: 58835954
# r.status_code == request.codes.ok
