from openai import OpenAI
from config.settings import settings
from utils.prompt_templates import PromptTemplates

class ScammerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    async def generate_message(self, scam_type, previous_reply=None):
        prompt = PromptTemplates.SCAMMER_ZERO_SHOT.format(
            scam_type=scam_type,
            previous_reply=previous_reply or "Initial message"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
            ],
            temperature=0.7
        )

        return response.choices[0].message.content
