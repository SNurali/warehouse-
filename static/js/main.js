document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm before delete
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Toggle password visibility
    var passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            var input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                input.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
    });

    // Dynamic formset handling
    document.querySelectorAll('.formset-container').forEach(function(container) {
        var formsetPrefix = container.dataset.formsetPrefix;
        var totalForms = document.getElementById('id_' + formsetPrefix + '-TOTAL_FORMS');
        var formCount = parseInt(totalForms.value);

        // Add new form
        container.querySelector('.add-form').addEventListener('click', function() {
            var template = container.querySelector('.empty-form').cloneNode(true);
            template.classList.remove('empty-form');
            template.classList.add('formset-form');
            template.style.display = '';

            var newForm = template.cloneNode(true);
            var newFormHtml = newForm.innerHTML.replace(/__prefix__/g, formCount);
            newForm.innerHTML = newFormHtml;

            container.querySelector('.formset-forms').appendChild(newForm);
            formCount++;
            totalForms.value = formCount;
        });

        // Delete form
        container.addEventListener('click', function(e) {
            if (e.target.classList.contains('delete-form')) {
                e.preventDefault();
                var form = e.target.closest('.formset-form');
                if (form) {
                    // If this is not a new form, mark it for deletion
                    var deleteInput = form.querySelector('input[id$="-DELETE"]');
                    if (deleteInput) {
                        deleteInput.value = 'on';
                        form.style.display = 'none';
                    } else {
                        form.remove();
                        formCount--;
                        totalForms.value = formCount;
                    }
                }
            }
        });
    });
});