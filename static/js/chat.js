var botui = new BotUI("botui-app");

// Function to start the conversation and ask for the company name
function startConversation() {
  botui.message
    .add({
      content:
        "Welcome to our chat service! Before we begin, could you please tell me the name of your company?",
    })
    .then(function () {
      askCompanyDomain(); // Prompt the user for the company name
    });
}

// Function to prompt the user for the company name
function askCompanyDomain() {
  botui.action
    .text({
      action: {
        placeholder: "Enter your company name here...",
      },
    })
    .then(function (res) {
      var companyDomain = res.value; // Capture the company name
      startInteractionWithCompany(companyDomain); // Start the interaction
    });
}

// Function to start interaction with the company by making a request to /start/{company_domain}
function startInteractionWithCompany(companyDomain) {
  fetch(`/start/${companyDomain}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the initial greeting from the chatbot as HTML
      var greeting = data.greeting.replace(/\n/g, "<br>");
      botui.message
        .add({
          type: "html",
          content: greeting,
        })
        .then(() => {
          // Insert an action here: a button that the user can click to get the first response
          return botui.action.button({
            action: [
              {
                text: "Let's Start!",
                value: "show_first_response",
              },
            ],
          });
        })
        .then((res) => {
          // Check the action's value to decide what to do next
          if (res.value === "show_first_response") {
            // Replace \n with <br> for HTML display in the first response
            var aspect = data.aspect.replace(/\n/g, "<br>");
            var chat_response = data.chat_response.replace(/\n/g, "<br>");
            // Display the 'aspect' as HTML in its own bubble
            return botui.message
              .add({
                type: "html",
                content: aspect,
              })
              .then(() => {
                // After displaying the 'aspect', display the 'chat_response' in a new bubble
                return botui.message.add({
                  type: "html",
                  content: chat_response,
                });
              });
          }
        })
        .then(() => {
          // After showing the first response, proceed with asking questions and further interaction
          askQuestion(companyDomain);
        });
    })
    .catch((error) => {
      console.error("Error:", error);
      botui.message.add({
        content: "An error occurred starting the chat. Please try again.",
      });
    });
}

// Function to send messages to the FastAPI backend and handle responses, now includes companyDomain parameter
function sendMessage(message, companyDomain) {
  var url = `/interact/${companyDomain}`; // Use company name in the URL

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
      var aspect = data.aspect.replace(/\n/g, "<br>");
      var chat_response = data.chat_response.replace(/\n/g, "<br>");
      botui.message
        .add({
          type: "html", // Specify the message type as HTML
          content: aspect,
        })
        .then(() => {
          // After displaying the 'aspect', display the 'chat_response' in a new bubble
          return botui.message.add({
            type: "html",
            content: chat_response,
          });
        });
      askQuestion(companyDomain); // Keep asking for user input
    })
    .catch((error) => {
      console.error("Error:", error);
      botui.message.add({
        content: "An error occurred. Please try again.",
      });
      askQuestion(companyDomain); // Attempt to recover by asking for input again
    });
}

// Modified to accept companyDomain as a parameter
function askQuestion(companyDomain) {
  botui.action
    .text({
      action: {
        placeholder: "Type your message here...",
      },
    })
    .then(function (res) {
      sendMessage(res.value, companyDomain); // Send user input to the backend with the company name
    });
}

// Initialize the conversation
startConversation();
