from src.agents.interaction import interaction_chain
from src.agents.overview import overview_evaluation_chain
from src.agents.offerings import offerings_evaluation_chain
from src.agents.usp import usp_evaluation_chain
from src.agents.use_cases import use_cases_evaluation_chain
from src.agents.intent_recognition import intent_recognition_chain
from src.agents.integration import integration_chain
from src.db.db_handler import DBHandler
from src.utils import get_aspect

with DBHandler() as db_handler:
    company_profile = db_handler.get_company_profile("Defigo")

aspects = {
    "general_overview": get_aspect(company_profile, "general_overview"),
    "offerings": get_aspect(company_profile, "offerings"),
    "unique_selling_points": get_aspect(company_profile, "unique_selling_points"),
    "customer_success_stories": get_aspect(company_profile, "customer_success_stories"),
}
general_overview = get_aspect(company_profile, "general_overview")
offerings = get_aspect(company_profile, "offerings")
offerings = "\n".join([f"{p['product']}: {p['description']}" for p in offerings])
unique_selling_points = get_aspect(company_profile, "unique_selling_points")
unique_selling_points = "\n".join(unique_selling_points)
customer_success_stories = get_aspect(company_profile, "customer_success_stories")
customer_success_stories = "\n".join(customer_success_stories)

print("general_overview", general_overview)
print("offerings", offerings)
print("unique_selling_points", unique_selling_points)
print("customer_success_stories", customer_success_stories)
print()


# res = overview_evaluation_chain.invoke({'general_overview':general_overview})
# res = offerings_evaluation_chain.invoke({'offerings':""})
# res = usp_evaluation_chain.invoke({'unique_selling_points':unique_selling_points})
res = use_cases_evaluation_chain.invoke({'customer_success_stories':customer_success_stories})

print(res)
