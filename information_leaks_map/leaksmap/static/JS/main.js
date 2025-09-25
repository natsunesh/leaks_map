// Main JavaScript for Leak Map Application

// Bootstrap form validation
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
});

// Additional utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.role = 'alert';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    document.body.appendChild(notification);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Form submission handlers
// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    // Check leaks form
    const checkLeaksForm = document.getElementById('check-leaks-form');
    if (checkLeaksForm) {
        checkLeaksForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add AJAX submission logic here
            showNotification('Checking for leaks...', 'info');

            // Get the email from the form
            const email = document.getElementById('email').value;

            // Send AJAX request to the server
            fetch('/check_leaks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `email=${encodeURIComponent(email)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.breaches) {
                    showNotification('Breaches found!', 'warning');
                } else {
                    showNotification('No breaches found.', 'success');
                }
            })
            .catch(error => {
                showNotification('Error checking for leaks.', 'danger');
                console.error('Error:', error);
            });
        });
    }

    // Export report form
    const exportReportForm = document.getElementById('export-report-form');
    if (exportReportForm) {
        exportReportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add AJAX submission logic here
            showNotification('Exporting report...', 'info');

            // Get the email and format from the form
            const email = document.getElementById('export-email').value;
            const format = document.getElementById('format').value;

            // Send AJAX request to the server
            fetch('/export_report/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `email=${encodeURIComponent(email)}&format=${encodeURIComponent(format)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    showNotification(data.message, 'success');
                } else {
                    showNotification('Report exported successfully!', 'success');
                }
            })
            .catch(error => {
                showNotification('Error exporting report.', 'danger');
                console.error('Error:', error);
            });
        });
    }
});
