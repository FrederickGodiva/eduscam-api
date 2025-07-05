from openai import OpenAI
from config.settings import settings
from utils.prompt_templates import PromptTemplates

class EvaluatorAgent:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    async def evaluate_response(self, user_message, conversation_history):
        prompt = PromptTemplates.EVALUATOR_FEW_SHOT.format(
            user_message=user_message
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                *conversation_history,
                {"role": "user", "content": user_message}
            ]
        )

        # Extract flag from response
        evaluation = response.choices[0].message.content
        if "vigilant" in evaluation.lower():
            return "vigilant"
        elif "unsure" in evaluation.lower():
            return "unsure"
        else:
            return "deceived"
