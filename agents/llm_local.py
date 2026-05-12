import subprocess
import sys

class LLMAgent:
    def __init__(self, name, prompt=None, model="phi3:mini"):
        self.name = name
        self.prompt = prompt or "Tu es un joueur de Yams standard."
        self.model = model

    def choose_hold(self, dice, roll_index, context):
        query = f"""{self.prompt}

Dés actuels: {dice}
Lancer n°{roll_index+1}
Quels dés veux-tu garder (indices 0-4) ?
Réponds UNIQUEMENT par une liste d'indices séparés par des virgules (ex: 0,2,4)."""
        response = self._call_llm(query)
        return self._parse_indices(response)

    def choose_category(self, dice, available_categories):
        cats = ", ".join(available_categories)
        query = f"""{self.prompt}

Dés finaux: {dice}
Catégories disponibles: {cats}
Quelle catégorie choisis-tu ?
Réponds UNIQUEMENT par le nom exact d'une catégorie ci-dessus."""
        response = self._call_llm(query).strip()
        for cat in available_categories:
            if cat.lower() in response.lower():
                return cat
        return available_categories[0]

    def _call_llm(self, query: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, query],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            sys.stderr.write(f"[ERREUR LLM] Impossible d'appeler le modèle '{self.model}': {e}\n")
            sys.exit(1)  # Arrêt immédiat du script

    def _parse_indices(self, response: str):
        try:
            return [int(x) for x in response.split(",") if x.strip().isdigit()]
        except Exception:
            return []
