

function loadAdminPageContent(){
    const contentDiv = document.getElementById("content"); // Get the content div
    contentDiv.style.display = "block"; // Ensure the content div is visible

    const adminPageMessageElement = document.createElement('h1');
    adminPageMessageElement.textContent = messages.adminPageMessage;
    contentDiv.appendChild(adminPageMessageElement);

    //load Section 1: endpoint stats 
    document.getElementById("endpoint-stats-title").textContent = messages.endpointStatsTitle;
    document.getElementById("endpointMethod").textContent = messages.endpointMethodTitle;
    document.getElementById("endPointEndpoint").textContent =  messages.endpointEndpointTitle;
    document.getElementById("endpointRequests").textContent = messages.endpointRequestsTitle;
    loadEndpointStats();

    //load Section 2: api usage stats
    document.getElementById("user-api-consumption-title").textContent = messages.userAPIConsumptionTitle;
    document.getElementById("usageUsername").textContent = messages.usageUsernameTitle;
    document.getElementById("usageEmail").textContent = messages.usageEmailTitle;
    document.getElementById("usageTotalRequests").textContent = messages.usageTotalRequestsTitle;
    loadApiUsageStats(); 
 
};

//gets the endpoints data from endpoints table 
async function loadEndpointStats() {
    try {
        const endpointStatsResponse = await fetch(`${API_BASE_URL}/api/v1/stats/endpoints`, {
            method: "GET",
            credentials: "include",
            headers: { "Accept": "application/json" },
        });

        const endpointStats = await endpointStatsResponse.json();
        // console.log("endpoint stats:" + endpointStats)
        renderEndpointStats(endpointStats["endpoints"]); //call render to display data

    } catch (error) {
        console.error("Error loading endpoint stats content:", error);
    } finally {
        hideLoadingEndpoint();
    }
}

//displays the data into the table
function renderEndpointStats(stats) {
    const tableBody = document.querySelector("#endpoint-table tbody");
    tableBody.innerHTML = ""; // Clear any existing data

    stats.forEach((stat) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${stat.method}</td>
            <td>${stat.endpoint}</td>
            <td>${stat.count}</td>
        `;
        tableBody.appendChild(row);
    });
}

//gets the api usage data form api_usage table
async function loadApiUsageStats(){
    try {
        const apiUsageStatsResponse = await fetch(`${API_BASE_URL}/api/v1/stats/apiUsage`, {
            method: "GET",
            credentials: "include",
            headers: { "Accept": "application/json" },
        });

        const apiUsageStats = await apiUsageStatsResponse.json();
        // console.log(apiUsageStats["users"]);
        renderApiUsageStats(apiUsageStats["users"]);  // Call render function to display the data

    } catch (error) {
        console.error("Error loading API usage stats content:", error);
    } finally {
        hideLoadingApi();
    }
}

//displays the data into the table
function renderApiUsageStats(stats) {
    const tableBody = document.querySelector("#user-api-table tbody"); 
    tableBody.innerHTML = ""; // Clear any existing data

    stats.forEach((stat) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${stat.first_name}</td>
            <td>${stat.email}</td>
            <td>${stat.total_api_calls}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Hide loading div
function hideLoadingEndpoint() {
    const loadingElement = document.getElementById("loading-endpoint");
    if (loadingElement) {
        loadingElement.style.display = "none"; 
    }
}
// Hide loading div
function hideLoadingApi() {
    const loadingElement = document.getElementById("loading-api");
    if (loadingElement) {
        loadingElement.style.display = "none"; 
    }
}

document.addEventListener("DOMContentLoaded", function () {
    loadAdminPageContent();
    console.log("loading admin page content");
});