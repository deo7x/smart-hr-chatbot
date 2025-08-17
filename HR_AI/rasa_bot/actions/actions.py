from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import subprocess
import json

class ActionLLMFallback(Action):

    def name(self):
        return "action_llm_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        user_message = tracker.latest_message.get("text")

        # Call Ollama LLaMA2 model
        try:
            result = subprocess.run(
                ["ollama", "query", "llama2", user_message],
                capture_output=True, text=True
            )
            llm_response = result.stdout.strip()
        except Exception as e:
            llm_response = "Sorry, I couldn't process that. 😅"

        dispatcher.utter_message(text=llm_response)
        return []
