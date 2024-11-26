const API_BASE_URL = "https://coral-app-3m7bi.ondigitalocean.app"; // For production

// Load Forgot Password Page Content
function loadForgotPasswordPageContent() {
    const forgotPasswordForm = document.getElementById("forgotPasswordForm");
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("forgotEmail").value;
            const messageElement = document.getElementById("forgotPasswordMessage");
            messageElement.textContent = messages.sendingResetLink;

            // Validate email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert(messages.emailFormatError);
                return; // Stop submission
            }
            
            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/request-password-reset`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email }),
                });

                const data = await response.json();
                if (response.ok) {
                    messageElement.style.color = "green";
                    messageElement.textContent = messages.resetLinkSent;
                } else {
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
            
            const newPassword = document.getElementById("resetNewPassword").value;

             // Validate password
             if (newPassword.length < 3) {
                alert(messages.passwordFormatError);
                return;
            }


            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/reset-password`, {
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
                    alert(messages.resetPasswordSuccess);
                    window.location.href = "login.html";
                } else {
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

    if (pathname.endsWith("forgot-password.html")) {
        loadForgotPasswordPageContent();
    } else if (pathname.endsWith("reset-password.html")) {
        loadResetPasswordPageContent();
    }
});
