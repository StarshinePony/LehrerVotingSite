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
    const deleteTeacherButtons = document.querySelectorAll('.delete-teacher');
    deleteTeacherButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Sind Sie sicher, dass Sie diesen Lehrer löschen möchten? Diese Aktion kann nicht rückgängig gemacht werden.')) {
                e.preventDefault();
            }
        });
    });
    
    // Confirm delete action for ratings/comments
    const deleteRatingButtons = document.querySelectorAll('.delete-rating');
    deleteRatingButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Sind Sie sicher, dass Sie diese Bewertung/diesen Kommentar löschen möchten? Diese Aktion kann nicht rückgängig gemacht werden.')) {
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
    
    // Modern animation for cards on scroll
    function animateOnScroll() {
        const cards = document.querySelectorAll('.teacher-card');
        cards.forEach((card, index) => {
            const delay = index * 100; // staggered animation
            setTimeout(() => {
                card.classList.add('show');
            }, delay);
        });
    }

    // Run animation when page loads
    if (document.querySelectorAll('.teacher-card').length > 0) {
        animateOnScroll();
    }
    
    // Apply appropriate chart theme based on current mode
    window.updateChartTheme = function(chart) {
        const isDarkMode = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        
        if (chart) {
            const textColor = isDarkMode ? '#f8f9fa' : '#212529';
            const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
            
            chart.options.scales.x.grid.color = gridColor;
            chart.options.scales.y.grid.color = gridColor;
            chart.options.scales.x.ticks.color = textColor;
            chart.options.scales.y.ticks.color = textColor;
            chart.options.plugins.title.color = textColor;
            
            chart.update();
        }
    };
});
