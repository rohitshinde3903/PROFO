<script>
        var ctx = document.getElementById('clickChart{{ link.id }}').getContext('2d');
        var clickChart{{ link.id }} = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    {% for click in link.daily_clicks %}
                        "{{ click.date }}",
                    {% endfor %}
                ],
                datasets: [{
                    label: "Daily Clicks",
                    data: [
                        {% for click in link.daily_clicks %}
                            {{ click.click_count }},
                        {% endfor %}
                    ],
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 2,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Click Trend for {{ link.platform }}'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Clicks'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    </script>