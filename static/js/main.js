// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize popovers and tooltips if Bootstrap JS is loaded
    if (typeof bootstrap !== 'undefined') {
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
        
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Confirm delete action for teachers
    const deleteButtons = document.querySelectorAll('.delete-teacher');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this teacher? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-important)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Star rating hover effect - for future enhancement
    const ratingInputs = document.querySelectorAll('.rating-input');
    if (ratingInputs.length) {
        ratingInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Update visual representation if needed
            });
        });
    }
});
