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

// Function to display breaches
function displayBreaches(breaches) {
    const resultsContainer = document.getElementById('leaks-results');
    if (!resultsContainer) return;

    if (!Array.isArray(breaches) || breaches.length === 0) {
        resultsContainer.innerHTML = '<div class="alert alert-info">Утечек не найдено.</div>';
        return;
    }

    let html = '<div class="alert alert-info"><h4>Найденные утечки:</h4><ul>';
    breaches.forEach(breach => {
        if (breach && breach.service_name && breach.description && breach.breach_date) {
            html += `<li><strong>${breach.service_name}</strong>: ${breach.description} (${breach.breach_date})</li>`;
        }
    });
    html += '</ul></div>';
    resultsContainer.innerHTML = html;
}

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    // Check leaks form
    const checkLeaksForm = document.getElementById('check-leaks-form');
    if (checkLeaksForm) {
        checkLeaksForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add AJAX submission logic here
            showNotification('Проверка утечек...', 'info');

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
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.breaches && data.breaches.length > 0) {
                    showNotification('Утечки найдены!', 'warning');
                    displayBreaches(data.breaches);
                } else {
                    showNotification('Утечек не найдено.', 'success');
                }
            })
            .catch(error => {
                showNotification('Ошибка при проверке утечек.', 'danger');
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
            showNotification('Экспорт отчета...', 'info');

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
                    showNotification('Отчет успешно экспортирован!', 'success');
                }
            })
            .catch(error => {
                showNotification('Ошибка при экспорте отчета.', 'danger');
                console.error('Error:', error);
            });
        });
    }
});
