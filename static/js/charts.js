// Function to initialize the rating distribution chart with theme support
function initRatingChart(teacherId) {
    // Fetch the rating data from the API
    fetch(`/api/teacher/${teacherId}/ratings`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('ratingChart').getContext('2d');
            
            // Get German labels
            const germanLabels = ['1 Stern', '2 Sterne', '3 Sterne', '4 Sterne', '5 Sterne'];
            
            // Determine text and grid colors based on current theme
            const isDarkMode = document.documentElement.getAttribute('data-bs-theme') === 'dark';
            const textColor = isDarkMode ? '#f8f9fa' : '#212529';
            const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
            
            // Create the chart using Chart.js
            const chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: germanLabels,
                    datasets: [{
                        label: 'Anzahl der Bewertungen',
                        data: data.values,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',   // Red for 1 star
                            'rgba(255, 159, 64, 0.7)',   // Orange for 2 stars
                            'rgba(255, 205, 86, 0.7)',   // Yellow for 3 stars
                            'rgba(75, 192, 192, 0.7)',   // Teal for 4 stars
                            'rgba(54, 162, 235, 0.7)'    // Blue for 5 stars
                        ],
                        borderColor: [
                            'rgb(255, 99, 132)',
                            'rgb(255, 159, 64)',
                            'rgb(255, 205, 86)',
                            'rgb(75, 192, 192)',
                            'rgb(54, 162, 235)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0, // Ensure we only show whole numbers
                                color: textColor
                            },
                            grid: {
                                color: gridColor
                            }
                        },
                        x: {
                            ticks: {
                                color: textColor
                            },
                            grid: {
                                color: gridColor
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Bewertungsverteilung',
                            color: textColor,
                            font: {
                                size: 16,
                                weight: 'normal'
                            }
                        },
                        legend: {
                            display: false
                        }
                    }
                }
            });
            
            // Store chart reference for theme updates
            window.ratingChart = chart;
            
            // Listen for theme changes to update chart colors
            document.getElementById('theme-toggle')?.addEventListener('click', function() {
                // Small timeout to let the theme change first
                setTimeout(() => {
                    window.updateChartTheme(window.ratingChart);
                }, 50);
            });
        })
        .catch(error => console.error('Error loading chart data:', error));
}
