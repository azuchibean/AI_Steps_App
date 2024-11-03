
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

function loadConsumptionData(userData, contentDiv) {
    const apiUsage = userData.total_api_calls;  
    const freeCallsRemaining = userData.free_api_calls_remaining;

    const usageMessageElement = document.createElement('p');
    usageMessageElement.textContent = messages.apiUsageMessage(apiUsage); 
    contentDiv.appendChild(usageMessageElement); 

    const freeCallsRemainingUsageElement = document.createElement('p');
    freeCallsRemainingUsageElement.textContent = messages.freeCallsRemainingMessage(freeCallsRemaining);
    contentDiv.appendChild(freeCallsRemainingUsageElement);
}
