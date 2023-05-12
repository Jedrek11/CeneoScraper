import os
import pandas as pd

# print([*filename.removesuffix(".json") for filename in os.listdir("opinions")])
print(*list(map(lambda x: x.removesuffix(".json"), os.listdir("opinions"))), sep="\n")
product_code = input("Podaj kot produktu: ")
opinions = pd.read_json(f"opinions/{product_code}.json")
# print(opinions)
opinions.stars = opinions.stars.map(lambda x: float(x.split("/")[0].replace(",",".")))

stats = {
    'opinions_count': len(opinions),
    # 'opinions_count': opinions.shape[0],
    'pros_count':  opinions.pros.map(bool).sum(),
    'cons_count':  opinions.cons.map(bool).sum(),
    'average_score': opinions.stars.mean()
}
print(f"""Dla produktu o indetyfikatorze {product_code}
pobrano {stats["opinions_count"]} opinii.
Dla {stats["pros_count"]} opinii podana została lista zalet produktu,
a dla {stats["cons_count"]} opinii podana została lista jego wad.
Średnia ocena produktu wynosi {stats["average_score"]:.2f}.""")