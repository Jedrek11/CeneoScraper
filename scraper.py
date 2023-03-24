import requests
from bs4 import BeautifulSoup
product_code = input("podaj kod produktu: ")
# url = "https://www.ceneo.pl/" + product_code +"#tab=reviews"

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
respons = requests.get(url)
# print(respons.status_code)
if respons.status_code == requests.codes.ok:
    page_dom =  BeautifulSoup(respons.text, 'html.parser')
    opinions = page_dom.select("div.js_product-review")
    if len(opinions) > 0:
        opinions_all = []
        for opinons in opinions:
            single_opinion = {
                "opinion_id": ""        ,   #opinion.dataset.entry-id="14616342"
                "author": ""            ,   #.user-post__author-name
                "recomedation": ""      ,   #.recomended
                "stars": ""             ,   #.score-maker[style]
                "purchased": ""         ,   #.review-pz[title]
                "opinion_date": ""      ,   #.user-post__published:first-child[datetime]
                "purchase_date": ""     ,   #.user-post__published:last-child[datatime]
                "usefull_count": ""     ,   #.vote-yes[data-vote]
                "unusefull_count":""    ,   #.vote-yes[data-vote]
                "content": ""           ,   #.user-post__text
                "pros": ""              ,   #review-feature__col
                "cons": ""                  #review-feature__col
            }
    else:
        print("Nie ma opinii")
        
    # print(page_dom.title.string)





# kod: 58835954
# r.status_code == request.codes.ok