// toasts.js
let notificationToast;
let toastBody;

document.addEventListener('DOMContentLoaded', (event) => {
    notificationToast = new bootstrap.Toast(document.getElementById('notificationToast'));
    toastBody = document.getElementById('toastBody');

    // Signup Form toasts
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {  // Check if signupForm exists
        const usernameInput = document.getElementById('signupUsername');
        const emailInput = document.getElementById('signupEmail');
        const password1Input = document.getElementById('signupPassword');
        const password2Input = document.getElementById('signupPassword2');

        signupForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent form from submitting immediately

            // Check if the username is between 3 and 20 characters
            if (usernameInput.value.length < 3 || usernameInput.value.length > 20) {
                toastBody.textContent = 'Username must be between 3 and 20 characters.';
                notificationToast.show();
                return;
            }

            // Check if the email includes an '@'
            if (!emailInput.value.includes('@')) {
                toastBody.textContent = 'Please include an "@" in the email address.';
                notificationToast.show();
                return;
            }

            // Check if the password is at least 8 characters and includes a digit and a special character
            const password1 = password1Input.value;
            if (password1.length < 8 || !/\d/.test(password1) || !/[!@#$%^&*]/.test(password1)) {
                toastBody.textContent = 'Password must be at least 8 characters and include at least one digit and one special character.';
                notificationToast.show();
                return;
            }

            // Check if the passwords match
            if (password1 !== password2Input.value) {
                toastBody.textContent = 'Passwords do not match.';
                notificationToast.show();
                return;
            }

            // Get the CSRF token
            const csrftoken = getCookie('csrftoken');

            // Check if the username or email is already taken
            fetch('/check_username_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    username: usernameInput.value,
                    email: emailInput.value
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.username_taken) {
                        toastBody.textContent = 'Username is already taken.';
                        notificationToast.show();
                    } else if (data.email_taken) {
                        toastBody.textContent = 'Email is already taken.';
                        notificationToast.show();
                    } else {
                        // If username and email are not taken, submit the form
                        fetch('/signup/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrftoken
                            },
                            body: JSON.stringify({
                                username: usernameInput.value,
                                email: emailInput.value,
                                password1: password1Input.value,
                                password2: password2Input.value
                            })
                        })
                            .then(response => {
                                if (!response.ok) {
                                    // Handle error
                                    toastBody.textContent = 'There was an error during the signup process. Please try again.';
                                    notificationToast.show();
                                } else {
                                    // Handle success
                                    toastBody.textContent = 'Signup successful! Redirecting to home page...';
                                    notificationToast.show();
                                    setTimeout(() => {
                                        window.location.href = '/'; // Redirect to home page
                                    }, 2000); // Redirect after 2 seconds
                                }
                            })
                            .catch(error => {
                                // Handle the error
                                toastBody.textContent = 'There was an error during the signup process. Please try again.';
                                notificationToast.show();
                            });
                    }
                })
                .catch(error => {
                    // Handle the error
                    toastBody.textContent = 'There was an error checking the username and email. Please try again.';
                    notificationToast.show();
                });
        });
    }
    // Login Form toasts
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {  // Check if loginForm exists
        const usernameInput = document.getElementById('id_username');
        const passwordInput = document.getElementById('id_password');

        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent form from submitting immediately

            // Get the CSRF token
            const csrftoken = getCookie('csrftoken');

            // Prepare the form data
            const formData = new URLSearchParams();
            formData.append('username', usernameInput.value);
            formData.append('password', passwordInput.value);

            // Submit the form
            fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        // Handle success
                        toastBody.textContent = data.message;
                        notificationToast.show();
                        setTimeout(() => {
                            window.location.href = '/'; // Redirect to home page
                        }, 2000); // Redirect after 2 seconds
                    } else {
                        // Handle error
                        toastBody.textContent = data.message;
                        notificationToast.show();
                    }
                })
                .catch(error => {
                    // Handle the error
                    toastBody.textContent = 'There was an error during the login process. Please try again.';
                    notificationToast.show();
                });
        });
    }
});