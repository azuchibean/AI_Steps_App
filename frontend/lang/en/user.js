const messages = {
    adminPageMessage: 'Welcome, Admin!',
    endpointStatistics: 'Endpoint Statistics',
    landingPageMessage: 'Landing Page',
    landingPageWelcome: (userName) => `Welcome, ${userName}!`,
    apiUsageMessage: (apiUsage) => `API Usage: ${apiUsage} requests`,
    freeCallsRemainingMessage: (freeCallsRemaining) => `Free Calls Remaining: ${freeCallsRemaining}`,

    apiUsageTitle: "API Usage",
    userInputTitle: "User Input",
    userSelectionTitle: "Your Selection",
    llmResponseTitle: "LLM Response",
    bestParkTitle: "Best Park",
    userSelectionPlaceholder: "Your selection will be displayed here.",
    llmResponsePlaceholder: "The response will be displayed here.",

    locationFetching: 'Fetching location...',
    locationError: 'Unable to fetch your location.',
    locationNotSupported: 'Geolocation is not supported by your browser.',
    submitButton: 'Submit',
    saveResponseButton: 'Save Response',
    selectedMessage: (steps, type, lat, lon) =>
        `Selected: ${steps}<br>Location Type: ${type}<br>Location: Latitude ${lat}, Longitude ${lon}`,
    llmResponseError: 'Error generating LLM message.',

};
