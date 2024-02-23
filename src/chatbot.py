from typing import Tuple, Optional
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
    """
    A chatbot designed for assisting in crafting and refining a company's profile
    for Market Shriek's platform. This chatbot automates the initial drafting of the
    company profile based on publicly available information and facilitates iterative
    refinement through user interaction.
    """
    def __init__(self, company_name:str):
        """
        Initializes the Chatbot instance with a specific company name, retrieves the
        company's profile from the database, and sets up the initial aspects of the profile
        for review and refinement.

        Parameters:
            company_name (str): The name of the company for which the profile is being created.
        """
        self.company_name = company_name
        self.company_profile = self.get_company_profile(company_name)
        self.aspects = {
            "general_overview": get_aspect(self.company_profile, "general_overview"),
            "offerings": get_aspect(self.company_profile, "offerings"),
            "unique_selling_points": get_aspect(self.company_profile, "unique_selling_points"),
            "customer_success_stories": get_aspect(self.company_profile, "customer_success_stories"),
        }

    def get_company_profile(self, company_name: str) -> dict:
        """
        Retrieves the company profile from a database using the company name. This method
        is responsible for establishing a connection to the database, querying the company's
        profile, and returning it.

        Parameters:
            company_name (str): The name of the company whose profile is to be retrieved.

        Returns:
            dict: A dictionary containing the company's profile information.
        """
        with DBHandler() as db_handler:
            company_profile = db_handler.get_company_profile(company_name)
        return company_profile

    def evaluate_aspect(self, aspect: str, aspect_value: str) -> dict:
        """
        Evaluates a given aspect of the company profile using predefined evaluation chains.
        This method processes the aspect's current content (aspect_value) to analyze, suggest
        improvements, or confirm its adequacy.

        Parameters:
            aspect (str): The aspect of the company profile being evaluated (e.g., "general_overview").
            aspect_value (str): The current content/value of the aspect being evaluated.

        Returns:
            dict: The result of the evaluation in JSON format, which may include suggestions for
                improvement or confirmation of the content's adequacy.
        """
        evaluation_chain = {
            "general_overview": overview_evaluation_chain,
            "offerings": offerings_evaluation_chain,
            "unique_selling_points": usp_evaluation_chain,
            "customer_success_stories": use_cases_evaluation_chain,
        }
        evaluation = evaluation_chain[aspect].invoke({aspect: aspect_value})
        return evaluation.json()

    def process_intent(self, user_input: str, current_aspect: str) -> Tuple[str, Optional[bool]]:
        """
        Processes the user's input to understand their intent regarding a specific aspect of
        the company profile. Based on the recognized intent, it may update the aspect content,
        accept the provided information, or handle unrecognized intents.

        Parameters:
            user_input (str): The input from the user concerning the current aspect.
            current_aspect (str): The aspect of the company profile currently being discussed.

        Returns:
            tuple: A tuple containing the (potentially updated) aspect content and a boolean flag
                indicating whether to continue refining this aspect (True) or move to the next one (False).
                If the intent is unrecognized, returns the current aspect content and None.
        """
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
        """
        Initiates the interaction process with the user, guiding them through reviewing and
        refining their company profile. It starts with a greeting and sequentially goes through
        each aspect of the profile, providing opportunities for the user to update or confirm
        the information. The process involves evaluating the current profile aspects, interpreting
        user input for intent, and updating the database with any changes made to the profile.

        The method ensures that the user can interactively refine their company's profile in a
        structured manner, focusing on one aspect at a time, and incorporates user feedback directly
        into the profile refinement process.
        """
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
