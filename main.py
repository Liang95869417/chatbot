import uvicorn
from src.chatbot_api import Chatbot
from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


class UserInput(BaseModel):
    user_input: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

chatbot_sessions = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/start/{company_domain}")
async def start_interaction(company_domain: str):
    # Initialize the Chatbot instance
    chatbot = Chatbot(company_domain)
    chatbot_sessions[company_domain] = chatbot
    # Send the greeting and the first aspect to review
    greeting = chatbot.get_greeting()
    aspect, chat_response = chatbot.run()
    return {"greeting": greeting, "aspect": aspect, "chat_response": chat_response}

@app.post("/interact/{company_domain}", summary="Process user interaction with the chatbot",
          description="This endpoint processes user inputs and returns the chatbot's response.")
async def process_user_input(
    company_domain: str = Path(..., description="The name of the company to interact with"),
    user_input: UserInput = Body(..., description="User input to be processed by the chatbot")):
    if company_domain not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    chatbot: Chatbot = chatbot_sessions[company_domain]
    aspect, chat_response = chatbot.run(user_input.user_input)
    return {"aspect": aspect, "chat_response": chat_response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
