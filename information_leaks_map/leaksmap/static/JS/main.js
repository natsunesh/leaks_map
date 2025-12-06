// Main JavaScript for Leak Map Application
document.addEventListener('DOMContentLoaded', function() {
    // Filters form (GET)
    const filtersForm = document.getElementById('filters-form');
    const resultsDiv = document.getElementById('leaks-results');

    if (filtersForm && resultsDiv) {
        filtersForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // GET параметры из формы
            const formData = new FormData(filtersForm);
            const params = new URLSearchParams(formData).toString();
            
            fetch(`/visualize_breaches/?${params}`, {
                method: 'GET',
                credentials: 'same-origin' 
            })
            .then(response => response.json())
            .then(data => {
                if (data.breaches && Array.isArray(data.breaches)) {
                    resultsDiv.innerHTML = data.breaches.map(breach => `
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">${escapeHtml(breach.service_name || '')}</h5>
                                <p class="card-text">${escapeHtml(breach.description || '')}</p>
                                <small class="text-muted">${escapeHtml(breach.breach_date || '')} - ${escapeHtml(breach.location || '')}</small>
                            </div>
                        </div>
                    `).join('');
                } else {
                    resultsDiv.innerHTML = '<div class="alert alert-info">Нет данных для визуализации. Проверьте фильтры или добавьте данные об утечках.</div>';
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
                resultsDiv.innerHTML = '<div class="alert alert-danger">Ошибка при загрузке данных. Пожалуйста, попробуйте снова.</div>';
            });
        });
    }

    // Check leaks form (POST)
    const checkLeaksForm = document.getElementById('check-leaks-form');
    if (checkLeaksForm) {
        checkLeaksForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('email')?.value?.trim();
            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                showNotification('Пожалуйста, введите корректный email.', 'danger');
                return;
            }

            showNotification('Проверка утечек...', 'info');

            const formData = new FormData();
            formData.append('email', email);

            fetch('/check_leaks/', {
                method: 'POST',
                credentials: 'same-origin',  
                body: formData 
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.breaches && data.breaches.length > 0) {
                    showNotification('Утечки найдены!', 'warning');
                    displayBreaches(data.breaches);
                    if (data.redirect_url) {
                        setTimeout(() => window.location.href = data.redirect_url, 1500);
                    }
                } else {
                    showNotification('Утечек не найдено.', 'success');
                }
            })
            .catch(error => {
                showNotification('Ошибка при проверке утечек: ' + error.message, 'danger');
                console.error('Error:', error);
            });
        });
    }

    // Export report form (POST)
    const exportReportForm = document.getElementById('export-report-form');
    if (exportReportForm) {
        exportReportForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('export-email')?.value?.trim();
            const format = document.getElementById('format')?.value || 'pdf';
            
            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                showNotification('Пожалуйста, введите корректный email.', 'danger');
                return;
            }

            showNotification('Экспорт отчета...', 'info');

            const formData = new FormData();
            formData.append('email', email);
            formData.append('format', format);

            fetch('/export_report/', {
                method: 'POST',
                credentials: 'same-origin', 
                body: formData 
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                showNotification(data.message || 'Отчет успешно экспортирован!', 'success');
            })
            .catch(error => {
                showNotification('Ошибка при экспорте: ' + error.message, 'danger');
                console.error('Error:', error);
            });
        });
    }
});

// Bootstrap form validation
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split('; ');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
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
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.role = 'alert';
    notification.innerHTML = `
        ${escapeHtml(message)}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

function displayBreaches(breaches) {
    const resultsContainer = document.getElementById('leaks-results');
    if (!resultsContainer) return;

    if (!Array.isArray(breaches) || breaches.length === 0) {
        resultsContainer.innerHTML = '<div class="alert alert-info">Утечек не найдено.</div>';
        return;
    }

    let html = '<div class="alert alert-warning"><h4>Найденные утечки:</h4><ul class="list-group list-group-flush">';
    breaches.forEach(breach => {
        if (breach && breach.service_name) {
            html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${escapeHtml(breach.service_name)}</strong>: 
                        ${escapeHtml(breach.description || '')} 
                        <small class="text-muted">(${escapeHtml(breach.breach_date || '')})</small>
                    </div>
                </li>
            `;
        }
    });
    html += '</ul></div>';
    resultsContainer.innerHTML = html;
}

// XSS защита
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
