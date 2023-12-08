document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    var form = document.forms["register_user_form"];

    // Function to validate the form
    function validateForm() {
        // Reset previous error messages
        clearErrors();

        // Flag to check if the form is valid
        var isValid = true;

        // Validate username
        if (form.username.value.length < 4 || form.username.value.length > 15) {
            displayError(form.username, "Username must be between 4 and 15 characters");
            isValid = false;
        }

        // Validate email
        if (!isValidEmail(form.email.value)) {
            displayError(form.email, "Enter a valid email address");
            isValid = false;
        }

        // Validate password
        if (form.password.value.length < 4 || form.password.value.length > 80) {
            displayError(form.password, "Password must be between 4 and 80 characters");
            isValid = false;
        }

        // Confirm password
        if (form.password.value !== form.password_confirm.value) {
            displayError(form.password_confirm, "Passwords do not match");
            isValid = false;
        }

        return isValid;
    }

    // Function to display error messages
    function displayError(inputField, errorMessage) {
        var errorElement = document.createElement("p");
        errorElement.className = "text-xs italic text-red-500";
        errorElement.textContent = errorMessage;
        inputField.parentNode.appendChild(errorElement);
    }

    // Function to clear previous error messages
    function clearErrors() {
        var errorMessages = form.querySelectorAll(".text-red-500");
        errorMessages.forEach(function (errorMessage) {
            errorMessage.parentNode.removeChild(errorMessage);
        });
    }

    // Function to validate email using a simple regex
    function isValidEmail(email) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Event listener for form submission
    form.addEventListener("submit", function (event) {
        if (!validateForm()) {
            // Prevent form submission if validation fails
            event.preventDefault();
        }
    });
});
