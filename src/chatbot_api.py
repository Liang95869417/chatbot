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
    def __init__(self, company_domain:str):
        """
        Initializes the Chatbot instance with a specific company name, retrieves the
        company's profile from the database, and sets up the initial aspects of the profile
        for review and refinement.
        """
        self.company_domain = company_domain
        self.company_profile = self.get_company_profile(company_domain)
        self.aspect_order = [
            "general_overview",
            "offerings",
            "unique_selling_points",
            "customer_success_stories",
            None
        ]
        self.aspects = {
            aspect: get_aspect(self.company_profile, aspect) for aspect in self.aspect_order
        }
        self.current_aspect = self.aspect_order[0]
        self.current_index = 0

    def get_company_profile(self, company_domain: str) -> dict:
        """
        Retrieves the company profile from a database using the company name. This method
        is responsible for establishing a connection to the database, querying the company's
        profile, and returning it.

        Parameters:
            company_domain (str): The name of the company whose profile is to be retrieved.

        Returns:
            dict: A dictionary containing the company's profile information.
        """
        with DBHandler() as db_handler:
            company_profile = db_handler.get_company_profile(company_domain)
        return company_profile
    
    def get_next_aspect(self) -> Optional[str]:
        """
        Advances to the next aspect for processing according to the predefined order.
        Returns None if all aspects have been processed.
        """
        self.current_index += 1
        if self.current_index < len(self.aspect_order):
            self.current_aspect = self.aspect_order[self.current_index]
            return self.current_aspect
        else:
            return None

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
        if aspect in evaluation_chain:
            evaluation = evaluation_chain[aspect].invoke({aspect: aspect_value})
            return evaluation.json()
        else:
            return {"error": "Invalid aspect provided."}
        
    def process_intent(self, user_input: str) -> Optional[bool]:
        """
        Processes the user's input to understand their intent regarding a specific aspect of
        the company profile. Based on the recognized intent, it may update the aspect content,
        accept the provided information, or handle unrecognized intents.

        Parameters:
            user_input (str): The input from the user concerning the current aspect.

        Returns:
            tuple: A tuple containing the (potentially updated) aspect content and a boolean flag
                indicating whether to continue refining this aspect (True) or move to the next one (False).
                If the intent is unrecognized, returns the current aspect content and None.
        """      
        intent = intent_recognition_chain.invoke({"user_message": user_input})
        print("Intent:", intent)
        if intent["intent"] == "Add More Information":
            updated_aspect = integration_chain.invoke(
                {"aspect": self.current_aspect, "add_info": user_input}
            )
            self.aspects[self.current_aspect] = updated_aspect  # Update the aspect in the class state
            return True
        elif intent["intent"] == "Accept Information":
            return False
        else:
            print("Unrecognized intent!!")
            return None
        
    def get_interaction(self, user_input: str) -> str:
        """
        Generates an interaction response for a specific aspect based on the user's input.
        """
        aspect_value = self.aspects[self.current_aspect]
        evaluation = self.evaluate_aspect(self.current_aspect, str(aspect_value))
        interaction_chain.memory.set_evaluation(evaluation)
        interaction = interaction_chain.invoke(input=user_input)
        return f"Here is the current {self.current_aspect}: \n{str(aspect_value)}\n\n", interaction["response"]


    @staticmethod
    def get_greeting():
        greeting = """
        I am the Chatbot from Swayle, dedicated to assisting you in crafting your company profile. To facilitate this process, we have already prepared a preliminary draft for you, utilizing the publicly available information from your website.

        For clarity and comprehensiveness, we've organized the profile into four main sections:

        1. General Overview: We'll start here to ensure all foundational details about your company are correct.
        2. Offering: This section outlines the products or services you provide.
        3. Unique Selling Proposition: Here, we highlight what sets your company apart from competitors.
        4. Customer Success Story: We conclude with real-world examples of how your customers benefit from your offerings.

        Let's begin with the General Overview to confirm that every detail accurately represents your business.
        """
        return greeting
    
    def update_profile_aspect(self) -> None:
        """
        Updates the specified aspect of the company profile in the database.
        """
        with DBHandler() as db_handler:
            updates = {self.current_aspect: self.aspects[self.current_aspect]}
            db_handler.update_company_profile(self.company_domain, updates)
        interaction_chain.memory.clear()  # Clear interaction chain memory after update

    def run(self, user_input: str = "") -> str:
        """
        Main method to process user input for a given aspect and generate a response.
        """
        if user_input:
            should_continue = self.process_intent(user_input)
            if should_continue is not None:
                if should_continue:
                    return self.get_interaction(user_input)
                else:
                    self.update_profile_aspect()  # Update the database when aspect refinement is done
                    self.get_next_aspect()
                    if self.current_aspect:
                        return self.get_interaction(user_input)
                    else:
                        return "Thank you for sharing your information with us. Your input is invaluable, and we've successfully collected all the necessary details. If there are any next steps, such as verification processes or additional actions required on your part, we will notify you promptly. In the meantime, if you have any questions or need further assistance, please don't hesitate to reach out. We're here to help. Have a great day!"

        else:
            return self.get_interaction(user_input)
