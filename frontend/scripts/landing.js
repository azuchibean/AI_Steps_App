function loadLandingPageContent(userData) {
    const contentDiv = document.getElementById("content"); // Get the content div
    contentDiv.style.display = "block"; // Ensure the content div is visible

    // Access user data
    const userName = userData.first_name;  

    const landingPageMessageElement = document.createElement('h1');
    landingPageMessageElement.textContent = messages.landingPageMessage; 

    const welcomeMessageElement = document.createElement('h2');
    welcomeMessageElement.textContent = messages.landingPageWelcome(userName); 

    contentDiv.appendChild(landingPageMessageElement);
    contentDiv.appendChild(welcomeMessageElement); 

    loadConsumptionData(userData, contentDiv); // Pass contentDiv to the consumption data function

    console.log("Landing page content loaded successfully!");
}

async function loadConsumptionData(userData, contentDiv) {
    const apiUsage = userData.total_api_calls;  
    const freeCallsRemaining = userData.free_api_calls_remaining;

    const usageMessageElement = document.createElement('p');
    usageMessageElement.textContent = messages.apiUsageMessage(apiUsage); 
    contentDiv.appendChild(usageMessageElement); 

    const freeCallsRemainingUsageElement = document.createElement('p');
    freeCallsRemainingUsageElement.textContent = messages.freeCallsRemainingMessage(freeCallsRemaining);
    contentDiv.appendChild(freeCallsRemainingUsageElement);

    const generateButton = document.createElement('button');
    generateButton.textContent = "What is the best park in Vancouver?";
    contentDiv.appendChild(generateButton);

    const llmMessageDiv = document.createElement('div');
    contentDiv.appendChild(llmMessageDiv);

    generateButton.addEventListener('click', async () => {
        const llmMessageContent = await generate_llm_message();
        llmMessageDiv.innerHTML = llmMessageContent || "Error generating message."; // Update to use the content directly
    });
}

// Temporary spot
async function generate_llm_message() {
    try {
        const response = await fetch(`${API_BASE_URL}/llm_test`, {
            method: "GET",
        });

        if (!response.ok) {
            throw new Error("Failed to fetch data from server");
        }

        const data = await response.json();
        console.log("Received data:", data.response);
        return data.response;
    } catch (error) {
        console.error("Error:", error);
    }
}
