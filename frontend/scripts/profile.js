import auth from './auth.js';

// Initialize profile page
document.addEventListener('DOMContentLoaded', async () => {
    const spinner = document.getElementById('loading-spinner');
    const profileContainer = document.getElementById('profile-container');

    try {
        
        // Show spinner and hide profile container
        spinner.style.display = 'flex';
        profileContainer.style.display = 'none';

        // Verify token and fetch user data
        const userData = await auth.verifyTokenAndRoute('user');
        if (!userData) return;

        // Populate profile data
        document.getElementById('user-name').textContent = userData.first_name;
        document.getElementById('user-email').textContent = userData.user;

         // Hide spinner and show profile container
         spinner.style.display = 'none';
         profileContainer.style.display = 'block';

        // Set up event listeners
        setupEventListeners();
    } catch (error) {
        spinner.style.display = 'none';
        console.error('Error initializing profile:', error);
    }
});

// Function to set up event listeners for profile actions
function setupEventListeners() {
    // Update Name Button
    const updateNameButton = document.getElementById('update-name-button');
    updateNameButton.addEventListener('click', async () => {
        const newNameInput = document.getElementById('new-name');
        const newName = newNameInput.value.trim();

        // Frontend validation: Check if the name contains only letters and spaces
        if (!/^[A-Za-z\s]+$/.test(newName)) {
            alert(messages.invalidNameFormat);
            return;
        }

        if (!newName) {
            alert(messages.invalidNameError);
            return;
        }

        const updated = await auth.updateName(newName);
        if (updated) {
            document.getElementById('user-name').textContent = newName;
            alert(messages.updateNameSuccess);
        }
    });
}

        // Delete Account Button
        const deleteAccountButton = document.getElementById('delete-account-button');
        deleteAccountButton.addEventListener('click', async () => {
            if (confirm(messages.deleteAccountConfirmation)) {
                const success = await auth.deleteAccount();
                if (success) {
                    alert(messages.deleteAccountSuccess);
                }
            }
        });
    