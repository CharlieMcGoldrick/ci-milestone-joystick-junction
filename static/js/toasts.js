// Signup Form toasts
document.addEventListener('DOMContentLoaded', (event) => {
    const signupForm = document.getElementById('signupForm');
    const usernameInput = document.getElementById('signupUsername');
    const emailInput = document.getElementById('signupEmail');
    const password1Input = document.getElementById('signupPassword');
    const password2Input = document.getElementById('signupPassword2');
    const errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
    const toastBody = document.getElementById('toastBody');

    signupForm.addEventListener('submit', function (event) {
        // Check if the username is between 3 and 20 characters
        if (usernameInput.value.length < 3 || usernameInput.value.length > 20) {
            toastBody.textContent = 'Username must be between 3 and 20 characters.';
            errorToast.show();
            event.preventDefault();
        }

        // Check if the email includes an '@'
        if (!emailInput.value.includes('@')) {
            toastBody.textContent = 'Please include an "@" in the email address.';
            errorToast.show();
            event.preventDefault();
        }

        // Check if the password is at least 8 characters and includes a digit and a special character
        const password1 = password1Input.value;
        if (password1.length < 8 || !/\d/.test(password1) || !/[!@#$%^&*]/.test(password1)) {
            toastBody.textContent = 'Password must be at least 8 characters and include at least one digit and one special character.';
            errorToast.show();
            event.preventDefault();
        }

        // Check if the passwords match
        if (password1 !== password2Input.value) {
            toastBody.textContent = 'Passwords do not match.';
            errorToast.show();
            event.preventDefault();
        }
    });
});