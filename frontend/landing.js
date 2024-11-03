function loadLandingPageContent(userData) {
    const contentDiv = document.getElementById("content"); // Get the content div
    contentDiv.style.display = "block"; // Ensure the content div is visible

    // Access user data
    const userName = userData.first_name;  // Assuming `user` contains the user's name or email

    const landingPageMessage = document.createElement('h1');
    landingPageMessage.textContent = 'Landing Page';
    const welcomeMessage = document.createElement('h2');
    welcomeMessage.textContent = `Welcome, ${userName}!`;
    contentDiv.appendChild(landingPageMessage);
    contentDiv.appendChild(welcomeMessage); 

    loadConsumptionData(userData, contentDiv); // Pass contentDiv to the consumption data function

    console.log("Landing page content loaded successfully!");
}

function loadConsumptionData(userData, contentDiv) {
    const apiUsage = userData.total_api_calls;  
    const freeCallsRemaining = userData.free_api_calls_remaining;

    const usageMessage = document.createElement('p');
    usageMessage.textContent = `API Usage: ${apiUsage} requests`;
    contentDiv.appendChild(usageMessage); 

    const freeCallsRemainingUsage = document.createElement('p');
    freeCallsRemainingUsage.textContent = `Free Calls Remaining: ${freeCallsRemaining}`;
    contentDiv.appendChild(freeCallsRemainingUsage);
}
