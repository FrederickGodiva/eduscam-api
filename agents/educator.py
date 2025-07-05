from openai import OpenAI
from config.settings import settings
from utils.prompt_templates import PromptTemplates

class EducatorAgent:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    async def generate_feedback(self, user_flag, scam_type, conversation_history):
        prompt = PromptTemplates.EDUCATOR_ZERO_SHOT.format(
            user_flag=user_flag,
            scam_type=scam_type
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                *conversation_history
            ]
        )

        return response.choices[0].message.content
