function loadAdminPageContent(){
    const contentDiv = document.getElementById("adminContent"); // Get the content div
    contentDiv.style.display = "block"; // Ensure the content div is visible

    const adminPageMessageElement = document.createElement('h1');
    adminPageMessageElement.textContent = messages.adminPageMessage;
    contentDiv.appendChild(adminPageMessageElement);
 
};