// const API_BASE_URL = "http://127.0.0.1:8000"; // For local testing
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

            // loginMessage.textContent = "Logging in...";
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
                // if (!response.ok) throw new Error(data.detail || "Login failed");
                if (!response.ok) throw new Error(data.detail || messages.loginFailure);

                loginMessage.style.color = "green";
                // loginMessage.textContent = "Login successful!";
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

            // registerMessage.textContent = "Registering...";
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
                // registerMessage.textContent = "Registration successful!";
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

// Load Forgot Password Page Content
function loadForgotPasswordPageContent() {
    const forgotPasswordForm = document.getElementById("forgotPasswordForm");
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("forgotEmail").value;
            const messageElement = document.getElementById("forgotPasswordMessage");

            // messageElement.textContent = "Sending reset link...";
            messageElement.textContent = messages.sendingResetLink;

            try {
                const response = await fetch(`${API_BASE_URL}/request-password-reset`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email }),
                });

                const data = await response.json();
                if (response.ok) {
                    messageElement.style.color = "green";
                    // messageElement.textContent = "Reset link sent! Check your email.";
                    messageElement.textContent = messages.resetLinkSent;
                } else {
                    // throw new Error(data.detail || "Failed to send reset link.");
                    throw new Error(data.detail || messages.resetLinkFailure);
                }
            } catch (error) {
                messageElement.style.color = "red";
                messageElement.textContent = error.message;
            }
        });
    }
}

// Load Reset Password Page Content
function loadResetPasswordPageContent() {
    const resetForm = document.getElementById("resetForm");
    if (resetForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get("token");

        resetForm.addEventListener("submit", async (event) => {
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
                    // alert("Password reset successful!");
                    alert(messages.resetPasswordSuccess);
                    window.location.href = "login.html";
                } else {
                    // alert("Error: " + data.detail);
                    alert(messages.genericErrorMessage(data.detail));
                }
            } catch (error) {
                console.error("Error:", error);
            }
        });
    }
}



// On Page Load: Check URL and Load Relevant Page Content
document.addEventListener("DOMContentLoaded", () => {
     
    const pathname = window.location.pathname;

    if (pathname.endsWith("login.html")) {
        loadLoginPageContent();
    } else if (pathname.endsWith("register.html")) {
        loadRegisterPageContent();
    } else if (pathname.endsWith("forgot-password.html")) {
        loadForgotPasswordPageContent();
    } else if (pathname.endsWith("reset-password.html")) {
        loadResetPasswordPageContent();
    }
    
});
