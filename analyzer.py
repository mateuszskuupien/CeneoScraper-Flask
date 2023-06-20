import os
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def analyzeit(product_code):

    opinions = pd.read_json(f"./opinions/{product_code}.json")
    opinions.score = opinions.score.map(
        lambda x: x.split("/")[0].replace(",", ".")).astype(float)
    stats = {

        "opinions_count": opinions.shape[0],
        "pros_count": int(opinions.pros.astype(bool).sum()),
        "cons_count": int(opinions.cons.astype(bool).sum()),
        "average_score": opinions.score.mean()
    }

    if not os.path.exists("./plots"):
        os.mkdir("./plots")

    score = opinions.score.value_counts().reindex(
        list(np.arange(0, 5.5, 0.5)), fill_value=0)

    score.plot.bar()
    plt.savefig(f"./plots/{product_code}_score.png")
    plt.close()

    recommendation = opinions.recommendation.value_counts(dropna=False)

    recommendation.plot.pie()
    plt.savefig(f"./plots/{product_code}_recommendation.png")
    plt.close()

    if not os.path.exists("./stats"):
        os.mkdir("./stats")

    stats["score"] = score.to_dict()
    stats["recommendation"] = recommendation.to_dict()
    with open(f"./stats/{product_code}.json", "w", encoding="UTF-8") as jf:
        json.dump(stats, jf, indent=4, ensure_ascii=False)

    return stats
