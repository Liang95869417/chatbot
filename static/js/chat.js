var botui = new BotUI("botui-app");

// Function to start the conversation and ask for the company name
function startConversation() {
  botui.message
    .add({
      content:
        "Welcome to our chat service! Before we begin, could you please tell me the name of your company?",
    })
    .then(function () {
      askCompanyName(); // Prompt the user for the company name
    });
}

// Function to prompt the user for the company name
function askCompanyName() {
  botui.action
    .text({
      action: {
        placeholder: "Enter your company name here...",
      },
    })
    .then(function (res) {
      var companyName = res.value; // Capture the company name
      startInteractionWithCompany(companyName); // Start the interaction
    });
}

// Function to start interaction with the company by making a request to /start/{company_name}
function startInteractionWithCompany(companyName) {
  fetch(`/start/${companyName}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Replace \n with <br> for HTML display
      var formattedMessage = data.message.replace(/\n/g, "<br>");
      // Display the initial greeting and response from the chatbot
      botui.message.add({
        type: "html", // Specify the message type as HTML
        content: formattedMessage,
      });
      askQuestion(companyName); // Proceed with asking questions and further interaction
    })
    .catch((error) => {
      console.error("Error:", error);
      botui.message.add({
        content: "An error occurred starting the chat. Please try again.",
      });
    });
}

// Function to send messages to the FastAPI backend and handle responses, now includes companyName parameter
function sendMessage(message, companyName) {
  var url = `/interact/${companyName}`; // Use company name in the URL

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_input: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Replace newline characters with HTML line breaks before displaying
      var formattedMessage = data.message.replace(/\n/g, "<br>");
      botui.message.add({
        type: "html", // Specify the message type as HTML
        content: formattedMessage,
      });
      askQuestion(companyName); // Keep asking for user input
    })
    .catch((error) => {
      console.error("Error:", error);
      botui.message.add({
        content: "An error occurred. Please try again.",
      });
      askQuestion(companyName); // Attempt to recover by asking for input again
    });
}

// Modified to accept companyName as a parameter
function askQuestion(companyName) {
  botui.action
    .text({
      action: {
        placeholder: "Type your message here...",
      },
    })
    .then(function (res) {
      sendMessage(res.value, companyName); // Send user input to the backend with the company name
    });
}

// Initialize the conversation
startConversation();
