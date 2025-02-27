// Form validation for required fields
document.addEventListener('DOMContentLoaded', function() {
    // Only run on pages with a signup form
    const form = document.getElementById('signup-form');
    if (!form) return;
    
    const nextButton = document.getElementById('next-button');
    const requiredFields = form.querySelectorAll('[required]');
    let hasAttemptedSubmit = false;
    
    // Function to check if all fields are valid
    function validateForm(showErrors = false) {
        let valid = true;
        
        requiredFields.forEach(field => {
            // Check if field has a value
            if (!field.value.trim()) {
                valid = false;
                
                // Only show error message if user has attempted to submit
                const errorElement = document.getElementById(field.id + '-error');
                if (errorElement) {
                    if (showErrors || hasAttemptedSubmit) {
                        errorElement.classList.remove('hidden');
                    } else {
                        errorElement.classList.add('hidden');
                    }
                }
                
                // Add invalid styling only if showing errors
                if (showErrors || hasAttemptedSubmit) {
                    field.classList.add('input-error');
                } else {
                    field.classList.remove('input-error');
                }
            } else {
                // Hide error message
                const errorElement = document.getElementById(field.id + '-error');
                if (errorElement) {
                    errorElement.classList.add('hidden');
                }
                
                // Remove invalid styling
                field.classList.remove('input-error');
            }
        });
        
        // Enable/disable the next button based on validity
        if (nextButton) {
            nextButton.disabled = !valid;
        }
        
        return valid;
    }
    
    // Do initial validation without showing errors
    validateForm(false);
    
    // Validate on input, but don't show errors
    requiredFields.forEach(field => {
        field.addEventListener('input', () => validateForm(false));
        field.addEventListener('change', () => validateForm(false));
    });
    
    // Prevent form submission if invalid and show errors
    form.addEventListener('submit', function(event) {
        hasAttemptedSubmit = true;
        if (!validateForm(true)) {
            event.preventDefault();
        }
    });
    
    // If next button is clicked but form is invalid, show errors
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            hasAttemptedSubmit = true;
            validateForm(true);
        });
    }
}); 