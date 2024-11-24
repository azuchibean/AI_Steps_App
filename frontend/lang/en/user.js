const messages = {
    // app.js
    loggingIn: "Logging in...",
    loginFailure: "Login failed.",
    loginSuccess: "Login successful!",
    registering: "Registering...",
    registerFailure: "Registration failed.",
    registerSuccess: "Registration successful!",

    // password.js
    sendingResetLink: "Sending reset link...",
    resetLinkSent: "Reset link sent! Check your email.",
    resetLinkFailure: "Failed to send reset link.",
    resetPasswordSuccess: "Password reset successful!",
    genericErrorMessage: (errorDetail) => `Error: ${errorDetail}`,

    // Profile
    invalidNameError: "Please enter a valid name.",
    updateNameSuccess: "Name updated successfully!",
    deleteAccountConfirmation: "Are you sure you want to delete your account? This action cannot be undone.",
    deleteAccountSuccess: "Account deleted successfully!",

    // auth.js
    logoutFailure: "Logout failed. Please try again.",
    logoutError: "An error occurred during logout. Please try again.",
    deleteAccountFailure: "Failed to delete account. Please try again.",
    deleteAccountError: "An error occurred while deleting your account. Please try again.",
    updateNameErrorDetail: (detail) => `Error updating name: ${detail}`,
    genericError: "An error occurred. Please try again.",

    //Admin page
    adminPageMessage: 'Welcome, Admin!',
    endpointStatistics: 'Endpoint Statistics',
    landingPageMessage: 'Landing Page',
    landingPageWelcome: (userName) => `Welcome, ${userName}!`,
    apiUsageMessage: (apiUsage) => `API Usage: ${apiUsage} requests`,
    freeCallsRemainingMessage: (freeCallsRemaining) => `Free Calls Remaining: ${freeCallsRemaining}`,
    errormessage: 'Error loading API usage data. Please try again.',

    //Landing page
    apiUsageTitle: "API Usage",
    userInputTitle: "User Input",
    userSelectionTitle: "Your Selection",
    llmResponseTitle: "Response",
    bestParkTitle: "Best Park",
    userSelectionPlaceholder: "Your selection will be displayed here.",
    llmResponsePlaceholder: "The response will be displayed here.",

    locationFetching: 'Fetching location...',
    locationError: 'Unable to fetch your location.',
    locationNotSupported: 'Geolocation is not supported by your browser.',
    submitButton: 'Submit',
    saveResponseButton: 'Save Response',
    selectedMessage: (steps, type, lat, lon, h) =>
        `Selected: ${steps} steps<br>Location Type: ${type}<br>Your Height: ${h} cm<br>Location: Latitude ${lat}°, Longitude ${lon}°`,
    locationMessage: (latitude, longitude) =>
        `Latitude: ${latitude}°, Longitude: ${longitude}°`,
    llmResponseError: 'Error generating LLM message.',
    heightValidationError: 'Please enter a valid positive integer for height.',

    recommendationsTitle: "Recommended Locations:",
    recommendationTitle: "AI recommendation:",
    viewOnGoogleMaps: "View on Google Maps",
    addressLabel: "Address: ",
    distanceLabel: "Distance: ",
    ratingLabel: "Rating: ",

    endpointStatsTitle: "API Endpoint Stats",
    userAPIConsumptionTitle: "User API Consumption",
    endpointMethodTitle: "Method",
    endpointEndpointTitle: "Endpoint",
    endpointRequestsTitle: "Requests",
    usageUsernameTitle: "Username",
    usageEmailTitle: "Email",
    usageTotalRequestsTitle: "Total requests",
};
