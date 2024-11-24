//const API_BASE_URL = "http://127.0.0.1:8000"; // For local testing
const API_BASE_URL = "https://coral-app-3m7bi.ondigitalocean.app"; // For production



// Load Login Page Content
function loadLoginPageContent() {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;
            const loginMessage = document.getElementById("loginMessage");

            loginMessage.textContent = messages.loggingIn;

            try {
                const response = await fetch(`${API_BASE_URL}/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    credentials: "include", // Include cookies in the request
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();
                if (!response.ok) throw new Error(data.detail || messages.loginFailure);

                loginMessage.style.color = "green";
                loginMessage.textContent = messages.loginSuccess;

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
}

// Load Register Page Content
function loadRegisterPageContent() {
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const firstName = document.getElementById("firstName").value;
            const email = document.getElementById("registerEmail").value;
            const password = document.getElementById("registerPassword").value;
            const registerMessage = document.getElementById("registerMessage");

            registerMessage.textContent = messages.registering;

            try {
                const response = await fetch(`${API_BASE_URL}/register`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    body: JSON.stringify({ first_name: firstName, email, password }),
                });

                const data = await response.json();
                if (!response.ok) throw new Error(data.detail || messages.registerFailure);

                registerMessage.style.color = "green";
                registerMessage.textContent = messages.registerSuccess;
                setTimeout(() => {
                    window.location.href = "login.html";
                }, 500);
            } catch (error) {
                registerMessage.style.color = "red";
                registerMessage.textContent = error.message;
            }
        });
    }
}

// Define navigateTo globally
window.navigateTo = function (page) {
    window.location.href = page;
};



// On Page Load: Check URL and Load Relevant Page Content
document.addEventListener("DOMContentLoaded", () => {
     
    const pathname = window.location.pathname;

    if (pathname.endsWith("login.html")) {
        loadLoginPageContent();
    } else if (pathname.endsWith("register.html")) {
        loadRegisterPageContent();
    } 
    
});
