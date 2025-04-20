// Function to initialize the rating distribution chart
function initRatingChart(teacherId) {
    // Fetch the rating data from the API
    fetch(`/api/teacher/${teacherId}/ratings`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('ratingChart').getContext('2d');
            
            // Create the chart using Chart.js
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Number of Ratings',
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
                                precision: 0 // Ensure we only show whole numbers
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Rating Distribution',
                            font: {
                                size: 16
                            }
                        },
                        legend: {
                            display: false
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading chart data:', error));
}
