const API_BASE_URL = "https://coral-app-3m7bi.ondigitalocean.app"; // For production

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
            const response = await fetch(`${API_BASE_URL}/api/v1/logout`, {
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
                alert(messages.logoutFailure);
            }
        } catch (error) {
            console.error("Error during logout:", error);
            logoutError(messages.logoutError);
        }
    }

    // Verify token and handle routing based on user role
    async verifyTokenAndRoute(requiredRole = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/verify-token`, {
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
    
            // Allow admins to access shared pages like profile.html
            if (requiredRole === 'user' && userData.isAdmin) {
                const currentPage = window.location.pathname.split("/").pop();
                if (currentPage !== "profile.html") {
                    console.log("User is admin, redirecting to admin page");
                    window.location.href = "admin.html";
                    return null;
                }
            }
    
            return userData;
        } catch (error) {
            console.error("Error during token verification:", error);
            window.location.href = "login.html";
            return null;
        }
    }
    

    async deleteAccount() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/delete-account`, {
                method: "DELETE",
                credentials: "include",
                headers: {
                    "Accept": "application/json"
                }
            });
    
            if (response.ok) {
                console.log("Account deleted successfully");
                window.location.href = "login.html";
                return true;
            } else {
                console.error("Failed to delete account:", response.statusText);
                alert(messages.deleteAccountFailure);
                return false;
            }
        } catch (error) {
            console.error("Error deleting account:", error);
            alert(messages.deleteAccountError);
            return false;
        }
    }


    async updateName(newName) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/update-name`, {
                method: "PUT",
                credentials: "include",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ new_name: newName })
            });
    
            if (response.ok) {
                const data = await response.json();
                console.log(data.message);
                return true;
            } else {
                const error = await response.json();
                console.error("Failed to update name:", error.detail);
                alert(messages.updateNameErrorDetail(error.detail));
                return false;
            }
        } catch (error) {
            console.error("Error during name update:", error);
            alert(messages.genericError);
            return false;
        }
    }
    
}

// Create and export a single instance
const auth = new Auth();
export default auth;