// auth.js
const API_BASE_URL = "http://127.0.0.1:8000"; // For local testing
// const API_BASE_URL = "https://coral-app-3m7bi.ondigitalocean.app"; // For production

class Auth {
    constructor() {
        this.initializeLogout();
    }

    // Initialize logout button functionality
    initializeLogout() {
        const logoutButton = document.getElementById("logout-button");
        if (logoutButton) {
            console.log("Logout button found");
            logoutButton.removeEventListener("click", this.handleLogout);
            logoutButton.addEventListener("click", this.handleLogout);
        }
    }

    // Handle logout functionality
    handleLogout = async (event) => {
        event.preventDefault();
        console.log("Logout initiated");
        
        try {
            const response = await fetch(`${API_BASE_URL}/logout`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                console.log("Logout successful");
                window.location.href = "login.html";
            } else {
                console.error("Logout failed:", response.statusText);
                alert("Logout failed. Please try again.");
            }
        } catch (error) {
            console.error("Error during logout:", error);
            alert("An error occurred during logout. Please try again.");
        }
    }

    // Verify token and handle routing based on user role
    async verifyTokenAndRoute(requiredRole = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/verify-token`, {
                method: "GET",
                credentials: "include",
                headers: {
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                console.log("Token verification failed");
                window.location.href = "login.html";
                return null;
            }

            const userData = await response.json();
            console.log("User data:", userData);

            // Handle admin-only pages
            if (requiredRole === 'admin' && !userData.isAdmin) {
                console.log("Admin access required but user is not admin");
                window.location.href = "landing.html";
                return null;
            }

            // Handle regular user pages
            if (requiredRole === 'user' && userData.isAdmin) {
                console.log("User is admin, redirecting to admin page");
                window.location.href = "admin.html";
                return null;
            }

            return userData;
        } catch (error) {
            console.error("Error during token verification:", error);
            window.location.href = "login.html";
            return null;
        }
    }
}

// Create and export a single instance
const auth = new Auth();
export default auth;