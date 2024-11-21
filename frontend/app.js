
// waiting for the backend endpoints to be created
const API_BASE_URL = "http://127.0.0.1:8000";  // Base URL for the backend API
//const API_BASE_URL = "https://coral-app-3m7bi.ondigitalocean.app";  // Base URL for the backend API

// Handle Login
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;
        const loginMessage = document.getElementById("loginMessage");

        loginMessage.textContent = "Logging in...";

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include", // Include cookies in the request
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.detail || "Login failed");

            loginMessage.style.color = "green";
            loginMessage.textContent = "Login successful!";

            // Redirect based on user role
            if (data.isAdmin) {
                window.location.href = "admin.html";
            } else {
                window.location.href = "landing.html";
            }
        } catch (error) {
            loginMessage.style.color = "red";
            loginMessage.textContent = error.message;
        }
    });
}

// Handle Registration
const registerForm = document.getElementById("registerForm");
if (registerForm) {  // Only add event listener if the registration form exists on the page
    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const firstName = document.getElementById("firstName").value;
        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;
        const registerMessage = document.getElementById("registerMessage");

        registerMessage.textContent = "Registering...";

        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ first_name: firstName, email, password }),
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.detail || "Registration failed");

            registerMessage.style.color = "green";
            registerMessage.textContent = "Registration successful!";

           //Redirect to login page after successful registration
                setTimeout(() => {
                    window.location.href = "login.html";
            }, 500);

        } catch (error) {
            registerMessage.style.color = "red";
            registerMessage.textContent = error.message;
        }
    });
}

// Handle Forgot Password
const forgotPasswordForm = document.getElementById("forgotPasswordForm");
if (forgotPasswordForm) {  // Only add event listener if the forgot password form exists on the page
    forgotPasswordForm.addEventListener("submit", async function(event) {
        event.preventDefault();
        
        const email = document.getElementById("email").value;
        const messageElement = document.getElementById("forgotPasswordMessage");
        
        messageElement.textContent = "Sending reset link...";
        
        try {
            const response = await fetch(`${API_BASE_URL}/request-password-reset`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                messageElement.style.color = "green";
                messageElement.textContent = "Reset link sent! Check your email.";
            } else {
                throw new Error(data.detail || "Failed to send reset link.");
            }
        } catch (error) {
            messageElement.style.color = "red";
            messageElement.textContent = error.message;
        }
    });
}

// Handle Reset Password
const resetForm = document.getElementById("resetForm");
if (resetForm) {  // Only add event listener if the reset password form exists on the page
    // Extract token from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    resetForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const newPassword = document.getElementById("newPassword").value;

        try {
            const response = await fetch(`${API_BASE_URL}/reset-password`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token: token,
                    new_password: newPassword,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                alert("Password reset successful!");
                // Redirect to login page if needed
                window.location.href = "login.html";
            } else {
                alert("Error: " + data.detail);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
}

// Check if user is logged in when a page loads (verifyToken function inside a DOMContentLoaded event listener)
async function verifyToken() {
    try {
        const response = await fetch(`${API_BASE_URL}/verify-token`, {
            method: "GET",
            credentials: "include" // Include cookies in the request
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Token verification failed");
        
        console.log("Token is valid:", data);
        return data;
    } catch (error) {
        console.error("Error verifying token:", error);
        return null;
    }
}
