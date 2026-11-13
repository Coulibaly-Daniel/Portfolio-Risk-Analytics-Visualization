import json
from pathlib import Path

from modules.llm_assistant import generate_ai_commentary

# Indicateurs de test
metrics = {
    "Performance totale": "100.59 %",
    "Volatilité annualisée": "13.71 %",
    "Maximum Drawdown": "-21.17 %",
    "VaR 95 %": "1.34 %",
    "CVaR 95 %": "1.99 %",
    "Tracking Error annualisée": "19.72 %"
}

print("Envoi des indicateurs à Qwen...")

commentary = generate_ai_commentary(metrics)

if commentary.startswith("Erreur Ollama"):
    print(commentary)

else:
    # Chemin du fichier JSON
    output_path = Path("data/ai_commentary.json")

    # Enregistrement du commentaire
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            {"commentary": commentary},
            file,
            ensure_ascii=False,
            indent=4
        )

    print("Analyse générée avec succès !")
    print(f"Commentaire enregistré dans : {output_path}")