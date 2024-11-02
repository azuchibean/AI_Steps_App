const API_BASE_URL = "http://127.0.0.1:8000";  // Base URL for the backend API

async function checkAuthentication() {
    const token = localStorage.getItem("token");

    if (!token) {
        // Redirect to login if no token
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/verify-token`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error("Unauthorized access. Please log in.");
        }

        const data = await response.json();
        console.log("User is authenticated:", data);
        document.body.style.display = 'block';  // Show content if authenticated
    } catch (error) {
        console.error(error);
        window.location.href = "login.html";  // Redirect to login on error
    }
}

window.onload = async () => {
    if (window.location.pathname === '/landing.html') {
        await checkAuthentication();
    }
};