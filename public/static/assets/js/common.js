document.addEventListener("DOMContentLoaded", function () {
    // Common Elements
    const alertContainer = document.getElementById('alert-container');

    // Password visibility toggle
    const passwordFields = document.querySelectorAll('.password-field');
    passwordFields.forEach(passwordField => {
        const togglePassword = passwordField.querySelector('.toggle-password');
        togglePassword.addEventListener('click', function () {
            const field = passwordField.querySelector('input');
            const type = field.type === 'password' ? 'text' : 'password';
            field.type = type;
            this.querySelector('span').classList.toggle('fa-eye');
            this.querySelector('span').classList.toggle('fa-eye-slash');
        });
    });

    // Handle form submissions for both login and register
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the form from submitting the traditional way

            const formId = form.id;
            let data = {};
            let url = '';

            if (formId === 'login-form') {
                // Login Form Submission
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                url = '/account/login/';
                data = { email: email, password: password };
            } else if (formId === 'register-form') {
                // Registration Form Submission
                const name = document.getElementById('name').value;
                const mobile = document.getElementById('mobile').value;
                const email = document.getElementById('email1').value;
                const password = document.getElementById('password1').value;
                const confirmPassword = document.getElementById('confirmPassword').value;

                // Validate if passwords match
                if (password !== confirmPassword) {
                    showAlert('error', 'Passwords do not match!', 'fa-exclamation-triangle');
                    return;
                }

                url = '/account/register/';
                data = { username: name, mobile: mobile, email: email, password: password };
            }

            // CSRF Token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            // Make the fetch request to the server
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // Send CSRF token in the header
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(responseData => {
                console.log('Success:', responseData);
                if (responseData.success) {
                    if (formId === 'login-form') {
                        window.location.href = '/Dashboard';  // Redirect to dashboard after successful login
                    } else if (formId === 'register-form') {
                        showAlert('success', 'Account created successfully!', 'fa-check-circle');
                        setTimeout(() => {
                            window.location.href = '/Dashboard';  // Redirect to dashboard after successful registration
                        }, 3000);
                    }
                } else {
                    showAlert('error', responseData.message || 'An unknown error occurred.', 'fa-exclamation-circle');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                showAlert('error', 'There was an error with the request.', 'fa-times-circle');
            });
        });
    });

    // Function to display alerts
    function showAlert(type, message, icon) {
        const alert = document.createElement('div');
        alert.classList.add('alert', 'alert-dismissible', `alert-${type}`);
        alert.innerHTML = `
            <i class="fas ${icon} mr-2"></i> ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
        alertContainer.appendChild(alert);

        // Automatically dismiss the alert after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
});
