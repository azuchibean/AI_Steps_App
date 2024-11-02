
// waiting for the backend endpoints to be created

const API_BASE_URL = "http://127.0.0.1:8000";  // Base URL for the backend API

// Handle Login
const loginForm = document.getElementById("loginForm");
if (loginForm) {  // Only add event listener if the login form exists on the page
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
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();
            
            if (!response.ok) throw new Error(data.detail || "Login failed");

            loginMessage.style.color = "green";
            loginMessage.textContent = "Login successful!";
            
            // Redirect to another page or perform other actions here
            setTimeout(() => {
                window.location.href = "dashboard.html"; // Example redirect after login
            }, 1000);
            
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
            
            // Redirect to login page after successful registration
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1000);
            
        } catch (error) {
            registerMessage.style.color = "red";
            registerMessage.textContent = error.message;
        }
    });
}