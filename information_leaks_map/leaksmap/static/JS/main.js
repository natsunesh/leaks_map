// Main JavaScript for Leak Map Application

// Bootstrap form validation
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation');

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
document.addEventListener('DOMContentLoaded', function() {
    // Check leaks form
    const checkLeaksForm = document.getElementById('check-leaks-form');
    if (checkLeaksForm) {
        checkLeaksForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add AJAX submission logic here
            showNotification('Checking for leaks...', 'info');
        });
    }

    // Export report form
    const exportReportForm = document.getElementById('export-report-form');
    if (exportReportForm) {
        exportReportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add AJAX submission logic here
            showNotification('Exporting report...', 'info');
        });
    }
});
