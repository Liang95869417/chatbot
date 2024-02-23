from src.agents.interaction import interaction_chain
from src.agents.overview import overview_evaluation_chain
from src.agents.offerings import offerings_evaluation_chain
from src.agents.usp import usp_evaluation_chain
from src.agents.use_cases import use_cases_evaluation_chain
from src.agents.intent_recognition import intent_recognition_chain
from src.agents.integration import integration_chain
from src.db.db_handler import DBHandler
from src.utils import get_aspect

class Chatbot:
    def __init__(self, company_name):
        self.company_name = company_name
        self.company_profile = self.get_company_profile(company_name)
        self.aspects = {
            "general_overview": get_aspect(self.company_profile, "general_overview"),
            "offerings": get_aspect(self.company_profile, "offerings"),
            "unique_selling_points": get_aspect(self.company_profile, "unique_selling_points"),
            "customer_success_stories": get_aspect(self.company_profile, "customer_success_stories"),
        }

    def get_company_profile(self, company_name):
        with DBHandler() as db_handler:
            company_profile = db_handler.get_company_profile(company_name)
        return company_profile

    def evaluate_aspect(self, aspect, aspect_value):
        evaluation_chain = {
            "general_overview": overview_evaluation_chain,
            "offerings": offerings_evaluation_chain,
            "unique_selling_points": usp_evaluation_chain,
            "customer_success_stories": use_cases_evaluation_chain,
        }
        evaluation = evaluation_chain[aspect].invoke({aspect: aspect_value})
        return evaluation.json()

    def process_intent(self, user_input, current_aspect):
        intent = intent_recognition_chain.invoke({"user_message": user_input})
        print("Intent:", intent)
        if intent["intent"] == "Add More Information":
            updated_aspect = integration_chain.invoke(
                {"aspect": current_aspect, "add_info": user_input}
            )
            return updated_aspect, True
        elif intent["intent"] == "Accept Information":
            return current_aspect, False
        else:
            print("Unrecognized intent!!")
            return current_aspect, None

    def run(self):
        greeting = """
I am the Virtual SDR from Market Shriek, dedicated to assisting you in crafting your company profile. To facilitate this process, we have already prepared a preliminary draft for you, utilizing the publicly available information from your website.

For clarity and comprehensiveness, we've organized the profile into four main sections:

1. General Overview: We'll start here to ensure all foundational details about your company are correct.
2. Offering: This section outlines the products or services you provide.
3. Unique Selling Proposition: Here, we highlight what sets your company apart from competitors.
4. Customer Success Story: We conclude with real-world examples of how your customers benefit from your offerings.

Let's begin with the General Overview to confirm that every detail accurately represents your business.
"""
        print(greeting)

        for aspect, value in self.aspects.items():
            evaluation = self.evaluate_aspect(aspect, str(value))
            interaction_chain.memory.set_evaluation(evaluation)
            response = interaction_chain.invoke(input="")
            print(f"Here is current {aspect}: \n{str(value)}")
            print(response["response"])

            while True:
                user_input = input("Enter your query (or type 'exit' to stop): ")
                if user_input.lower() == "exit":
                    break

                updated_aspect, should_continue = self.process_intent(user_input, value)
                if should_continue is None:
                    continue
                elif should_continue:
                    evaluation = self.evaluate_aspect(aspect, updated_aspect)
                    interaction_chain.memory.set_evaluation(evaluation)
                    response = interaction_chain.invoke(input=user_input)
                    print(f"Here is updated {aspect}: \n{updated_aspect}")
                    print(response["response"])
                else:
                    with DBHandler() as db_handler:
                        updates = {aspect: value}
                        db_handler.update_company_profile(self.company_name, updates)
                    interaction_chain.memory.clear()
                    break


if __name__ == "__main__":
    assistant = Chatbot("Defigo")
    assistant.run()
