import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import json

try:
    os.mkdir("charts")
except FileExistsError:
   pass
try:
    os.mkdir("stats")
except FileExistsError:
   pass

print(*[filename.removesuffix('.json') for filename in os.listdir("./opinions")], sep='\n') #list comprehension
# print(*list(map( lambda x: x.removesuffix('.json'), os.listdir('./opinions'))), sep='\n')


product_code = input("Podaj kod produktu: ")
opinions = pd.read_json(f"opinions/{product_code}.json")
opinions.stars = opinions.stars.map(lambda x: float(x.split('/')[0].replace(",", ".")))

print(opinions)

stats = {
    #'opinions_count': len(opinions),
    'opinions_count': int(opinions.shape[0]),
    'pros_count': int(opinions.pros.map(bool).sum()),
    'cons_count': int(opinions.cons.map(bool).sum()),
    'average_score': float(opinions.stars.mean())
}

print(f"""
Dla produktu o identyfikatorze {product_code}
pobrano {stats["opinions_count"]} opinii. 
Dla {stats['pros_count']} opinii podana została lista zalet produktu,
a dla {stats["cons_count"]} opinii podana została lista jego wad.
Średnia ocena produktu wynosi {stats["average_score"]:.2f}.
""")
colors_stars = {}

for i in np.arange(0, 5.5, 0.5):
    if i <= 2.5:
        colors_stars[i] = "crimson"
    elif i <= 3.5:
        colors_stars[i] = "steelblue"
    else:
        colors_stars[i] = "forestgreen"

stars = opinions.stars.value_counts().reindex(list(np.arange(0, 5.5, 0.5)), fill_value=0)
stars.plot.bar(color=colors_stars.values())
plt.xticks(rotation='horizontal')
plt.title("Rozkład liczby gwiazdek w opiniach konsumentów")
plt.xlabel('Liczba gwiazdek')
plt.ylabel('Liczba opinii')
plt.ylim(0, max(stars) + 10)
for index, value in enumerate(stars):
    plt.text(index, value + 0.5, str(value), ha='center')
plt.savefig(f"charts/{product_code}_stars.png")
plt.close()

recommendations = opinions.recommendation.value_counts(dropna=False).reindex(["Polecam", "Nie polecam", None], fill_value=0)
recommendations.plot.pie(autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '', labels=['Polecam', 'Nie polecam', 'Nie mam zdania'], colors=['forestgreen','crimson', 'steelblue'])
plt.title("Rozkład rekomendacji w opiniach konsumentów")
plt.legend(loc='upper center', ncol=3)
plt.ylabel('')
plt.savefig(f"charts/{product_code}_recommendation.png")
plt.close()

stats['stars'] = stars.to_dict()
stats['recommendations'] = recommendations.to_dict()

with open(f"stats/{product_code}.json", "w", encoding='UTF-8') as jf:
    json.dump(stats, jf, indent=4, ensure_ascii=False)