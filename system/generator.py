import os
import anthropic

API_KEY=os.getenv("ANTHROPIC_API_KEY")
API_MODEL="claude-sonnet-4-5"

def construire_prompt(entreprise, secteur, tonalite):
    return (
        f"Tu es un expert en prospection B2B. "
        f"Génère un email court et personnalisé pour l'entreprise {entreprise} "
        f"qui opère dans le secteur {secteur}. "
        f"Ton : {tonalite}."
    )

class EmailClient:
    def __init__(self):
        self.client=anthropic.Anthropic(api_key=API_KEY)

    def ask(self, prompt: str, context: list) -> str:
        try:
            messages=context.copy()
            messages.append({"role": "user", "content": prompt})

            response=self.client.messages.create(
                model=API_MODEL,
                max_tokens=2048,
                messages=messages,
            )

            return "\n".join(
                block.text for block in response.content
                if hasattr(block, "text")
            )
        except Exception as e:
            return f"Erreur : {str(e)}"
        
    def generer_email(self, entreprises, tonalite):
        nom=entreprises.get("nom_entreprise")
        site=entreprises.get("site_web", "")
        secteur = entreprises.get("secteur")
        p = construire_prompt(nom, secteur, tonalite)
        answer = self.ask(p, [])
        entreprises["email_genere"] = answer 
        return entreprises
    
    def generer_tous(self, entreprises, tonalite):
        resultat=[]
        for entreprise in entreprises:
            resultat.append(self.generer_email(entreprise, tonalite))
        return resultat
