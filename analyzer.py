import os
import pandas as pd
import numpy as np
import _json
from matplotlib import pyplot as plt

try:
    os.mkdir("charts")
except FileExistsError:
   pass
# print([*filename.removesuffix(".json") for filename in os.listdir("opinions")])
print(*list(map(lambda x: x.removesuffix(".json"), os.listdir("opinions"))), sep="\n")
product_code = input("Podaj kot produktu: ")
opinions = pd.read_json(f"opinions/{product_code}.json")
# print(opinions)
opinions.stars = opinions.stars.map(lambda x: float(x.split("/")[0].replace(",",".")))

stats = {
    'opinions_count': len(opinions),
    # 'opinions_count': opinions.shape[0],
    'pros_count':  int(opinions.pros.map(bool).sum()),
    'cons_count':  int(opinions.cons.map(bool).sum()),
    'average_score': float(opinions.stars.mean())
}
print(f"""Dla produktu o indetyfikatorze {product_code}
pobrano {stats["opinions_count"]} opinii.
Dla {stats["pros_count"]} opinii podana została lista zalet produktu,
a dla {stats["cons_count"]} opinii podana została lista jego wad.
Średnia ocena produktu wynosi {stats["average_score"]:.2f}.""")

colors_stats = {}
for i in np.arange(0,5.5,0.5):
    colors_stats[i] = "crimson" if i <= 2.5 else "steelblue" if i <= 3.5 else "forestgreen"
stars = opinions.stars.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
print(stars)
stars.plot.bar(color=colors_stats.values())
plt.xticks(rotation='horizontal')
plt.title("Rozkład liczby gwiazdek w opinii konsumentów")
plt.xlabel("liczby gwiazdek")
plt.ylabel("liczba opinii")
plt.ylim(0,max(stars)+10)
for index, value in enumerate(stars):
    plt.text(index, value+0.5, str(value), ha="center")
# plt.show()
plt.savefig(f"charts/{product_code}_stars.png")
plt.close()

recommendation = opinions["recommendation"].value_counts(dropna= False).reindex(["Polecam","Nie Polecam",None], fill_value=0)
recommendation.plot.pie(
    lable="",
    autopct= lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
    lables = ["Polecam","Nie Polecam","Nie mam zdania"],
    colors = ["forestgreen","crismon","steelblue"]
)
plt.legend(loc='upper center',ncol=3)
plt.title("Rozkład rekomendacji w oppinii konsumentów")
plt.savefig(f"./charts/{product_code}_recommendation.png")
plt.close()

stats['stars'] = stars.to_dict()
stats['recommendation'] = recommendation.to_dict()

print(stats)
with open(f"stats/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(stats, jf, indent=4, ensure_ascii=False)