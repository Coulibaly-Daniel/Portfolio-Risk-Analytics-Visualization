import requests


def generate_ai_commentary(metrics):

    url = "http://localhost:11434/api/generate"

    prompt = f"""
Tu es un analyste financier spécialisé dans l'analyse
de performance et de risque de portefeuille.

Voici les indicateurs calculés par Python :

{metrics}

Rédige une analyse professionnelle en français avec
les trois parties suivantes :

1. Performance du portefeuille
2. Analyse des risques
3. Points de vigilance

Consignes impératives :

- Les chiffres fournis sont les seuls chiffres autorisés.
- Ne modifie aucun indicateur.
- N'invente aucune donnée ni aucun événement de marché.
- Ne qualifie pas automatiquement une volatilité ou
  un drawdown de faible, élevé ou inacceptable.
- Explique ce que chaque indicateur mesure.
- Distingue les observations chiffrées des interprétations.
- Pour le VaR à 95 %, explique qu'il s'agit d'un seuil
  de perte associé à un niveau de confiance de 95 %,
  sur l'horizon retenu pour son calcul.
- Pour le CVaR, explique la perte moyenne dans la queue
  des pertes au-delà du seuil de VaR.
- Le Tracking Error mesure l'écart-type des différences
  de rendement entre le portefeuille et son benchmark.
- Ne recommande aucune décision d'investissement sans
  informations suffisantes.
- Signale les informations manquantes qui limitent
  l'interprétation des résultats.

Utilise un langage précis, professionnel et concis.
"""

    payload = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        return response.json()["response"]

    except requests.exceptions.RequestException as e:
        return f"Erreur Ollama : {e}"
