from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionLLMFallback(Action):

    print('we get some questions ..')
    def name(self):
        return "action_llm_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        # Replace this with actual LLM response
        response_text = "Hello! I am your fallback assistant."

        dispatcher.utter_message(text=response_text)
        return []
