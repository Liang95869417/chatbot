from src.agents.interaction import interaction_chain
from src.agents.overview import overview_evaluation_chain
from src.agents.offerings import offerings_evaluation_chain
from src.agents.usp import usp_evaluation_chain
from src.agents.use_cases import use_cases_evaluation_chain
from src.agents.intent_recognition import intent_recognition_chain
from src.agents.integration import integration_chain

# res = overview_evaluation_chain.invoke({'general_overview':""})
# res = offerings_evaluation_chain.invoke({'offerings':""})
# res = usp_evaluation_chain.invoke({'unique_selling_points':""})
res = use_cases_evaluation_chain.invoke({'customer_success_stories':""})
print(res)