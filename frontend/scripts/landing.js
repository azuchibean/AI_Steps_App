function loadLandingPageContent(userData) {
    // Get the content div
    const contentDiv = document.getElementById("content");
    contentDiv.style.display = "block"; // Ensure the content div is visible

    // Dynamically populate the landing page title and welcome message using `messages`
    const landingPageMessageElement = document.createElement('h1');
    landingPageMessageElement.textContent = messages.landingPageMessage;

    const welcomeMessageElement = document.createElement('h2');
    welcomeMessageElement.textContent = messages.landingPageWelcome(userData.first_name);

    // Append landing page and welcome messages to the content div
    contentDiv.appendChild(landingPageMessageElement);
    contentDiv.appendChild(welcomeMessageElement);

    // Dynamically populate Section Titles
    document.getElementById("api-usage-section").querySelector("h2").textContent = messages.apiUsageTitle;
    document.getElementById("user-input-section").querySelector("h2").textContent = messages.userInputTitle;
    document.getElementById("user-selection-section").querySelector("h2").textContent = messages.userSelectionTitle;
    document.getElementById("llm-response-section").querySelector("h2").textContent = messages.llmResponseTitle;
    document.getElementById("best-park-section").querySelector("h2").textContent = messages.bestParkTitle;

    // Populate placeholders for user selection and LLM response sections
    document.getElementById("user-selection").textContent = messages.userSelectionPlaceholder;
    document.getElementById("llm-response").textContent = messages.llmResponsePlaceholder;

    // Load Section 1: API Usage
    const apiUsageSection = document.getElementById("api-usage-content");
    loadConsumptionData(userData, apiUsageSection);

    // Load Section 2: User Input
    const userInputSection = document.getElementById("user-input-section");
    loadInteractiveComponents(userData, userInputSection);

    // Load Section 5: Best Park Button (for testing)
    const bestParkSection = document.getElementById("best-park-button-container");
    loadBestParkButton(bestParkSection);

    console.log("Landing page content loaded successfully!");
}


async function loadConsumptionData(userData, apiUsageSection) {
    const apiUsage = userData.total_api_calls;
    const freeCallsRemaining = userData.free_api_calls_remaining;

    const usageMessageElement = document.createElement("p");
    usageMessageElement.textContent = messages.apiUsageMessage(apiUsage);
    apiUsageSection.appendChild(usageMessageElement);

    const freeCallsRemainingUsageElement = document.createElement("p");
    freeCallsRemainingUsageElement.textContent = messages.freeCallsRemainingMessage(freeCallsRemaining);
    apiUsageSection.appendChild(freeCallsRemainingUsageElement);
}


async function loadInteractiveComponents(userData, userInputSection) {
    // Steps buttons
    const stepsButtonsContainer = document.createElement("div");
    stepsButtonsContainer.innerHTML = `
        <button id="steps-1000" class="step-button">1000 steps</button>
        <button id="steps-5000" class="step-button">5000 steps</button>
        <button id="steps-10000" class="step-button">10000 steps</button>
    `;
    userInputSection.appendChild(stepsButtonsContainer);

    // Dropdown for location type
    const locationTypeContainer = document.createElement("div");
    locationTypeContainer.innerHTML = `
        <label for="location-dropdown">Choose location type: </label>
        <select id="location-dropdown">
            <option value="park">Park</option>
            <option value="beach">Beach</option>
            <option value="mall">Mall</option>
        </select>
    `;
    userInputSection.appendChild(locationTypeContainer);

    // Add location placeholder
    const locationElement = document.createElement("p");
    locationElement.id = "location";
    locationElement.textContent = messages.locationFetching;
    userInputSection.appendChild(locationElement);

    // Add Submit button
    const submitButton = document.createElement("button");
    submitButton.id = "submit-selection";
    submitButton.textContent = messages.submitButton;
    userInputSection.appendChild(submitButton);

    // Track step selection
    let selectedSteps = "1000 steps"; // Default
    const stepButtons = document.querySelectorAll(".step-button");

    stepButtons.forEach((button) => {
        button.addEventListener("click", () => {
            stepButtons.forEach((btn) => btn.classList.remove("selected")); // Remove "selected" class
            button.classList.add("selected"); // Add "selected" class
            selectedSteps = button.textContent; // Update selected steps
        });
    });

    // Handle location fetching
    const userLocation = await loadUserLocation(locationElement);

    // Handle Submit button click
    submitButton.addEventListener("click", async () => {
        const locationType = document.getElementById("location-dropdown").value;

        const requestData = {
            distance: selectedSteps,
            type: locationType,
            userLocation,
        };

        console.log("Request Data:", requestData);

        // Fetch LLM response
        const llmResponse = await generate_llm_message2(requestData);

        // Section 3: Display the user selections
        const userSelectionDisplay = document.getElementById("user-selection");
        userSelectionDisplay.innerHTML = messages.selectedMessage(
            selectedSteps,
            locationType,
            userLocation.latitude,
            userLocation.longitude
        );

        // Section 4: Display the LLM response
        const llmResponseDisplay = document.getElementById("llm-response");
        llmResponseDisplay.textContent = llmResponse || messages.llmResponsePlaceholder;

        // Add a POST button to the LLM Response section (outside the response block)
        let postButton = document.getElementById("post-response"); // Avoid duplicates
        if (!postButton) {
            postButton = document.createElement("button");
            postButton.id = "post-response";
            postButton.textContent = messages.saveResponseButton;
            const llmResponseSection = document.getElementById("llm-response-section");
            llmResponseSection.appendChild(postButton); // Append the button to the section
        }


        // Handle POST button click
        postButton.addEventListener("click", () =>
            postResponse({
                user_id: userData.user, // now is email, need to fix the endpoint
                location_from: userLocation,
                location_to: llmResponse,
                type: locationType,
                distance: selectedSteps,
            })
        );
    });
}



// Request location from the user
async function loadUserLocation(locationElement) {
    return new Promise((resolve) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    locationElement.textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;
                    resolve({ latitude, longitude });
                },
                (error) => {
                    console.error("Error fetching location:", error);
                    locationElement.textContent = messages.locationError;
                    resolve({ latitude: null, longitude: null });
                }
            );
        } else {
            locationElement.textContent = messages.locationNotSupported;
            resolve({ latitude: null, longitude: null });
        }
    });
}


// for sending POST request to llm
async function generate_llm_message2(requestData) {
    try {
        const response = await fetch(`${API_BASE_URL}/llm_endpoint`, {  // for testing
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch data from server");
        }

        const data = await response.json();
        console.log("LLM Response Data:", data);
        return data.response; // Adjust this based on the actual API's response structure
    } catch (error) {
        console.error("Error generating LLM message:", error);
        return "Error generating LLM message.";
    }
}

// for sending POST request to save response/location to db
async function postResponse(postData) {
    console.log("Post Data:", postData);

    try {
        const postResponse = await fetch(`${API_BASE_URL}/post_endpoint`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(postData),
        });

        if (!postResponse.ok) {
            throw new Error("Failed to post data to the server.");
        }

        const responseData = await postResponse.json();
        console.log("Post Response Data:", responseData);
        alert("Data posted successfully!");
    } catch (error) {
        console.error("Error posting data:", error);
        alert("Error posting data to the server.");
    }
}



// New function for "Best Park" button
function loadBestParkButton(contentDiv) {
    const generateButton = document.createElement('button');
    generateButton.textContent = "What is the best park in Vancouver?";
    contentDiv.appendChild(generateButton);

    const llmMessageDiv = document.createElement('div');
    contentDiv.appendChild(llmMessageDiv);

    generateButton.addEventListener('click', async () => {
        const llmMessageContent = await generate_llm_message();
        llmMessageDiv.innerHTML = llmMessageContent || "Error generating message.";
    });
}

// Temporary spot
async function generate_llm_message() {
    try {
        const response = await fetch(`${API_BASE_URL}/llm_test`, {
            method: "GET",
            credentials: "include",

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
