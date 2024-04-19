document.addEventListener('DOMContentLoaded', function() {
   
    /*
    this script is responsible for updating the gem chart data. 
    The data is updated by fetching the gemVisitedFrequency and gemDistribution data from the server.
    The gemVisitedFrequency data is used to update the line chart, while the gemDistribution data is used to update the pie chart.
    Good luck trying to debug this if it ever breaks.
    */
    const ctx = document.getElementById('gem-chart').getContext('2d');
    const data = gemVisitedFrequency;
    const monthOrder = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const sortedKeys = monthOrder.filter(month => Object.keys(data).includes(month));
    const chartLabels = sortedKeys;
    const chartData = sortedKeys.map(key => data[key]);

    function interpolateColors(startColor, endColor, n) {
        const lerp = (start, end, t) => start + (end - start) * t;
        let colors = [];
        for (let i = 0; i < n; i++) {
            const t = i / (n - 1);
            const interpolatedColor = `rgb(${
                Math.round(lerp(startColor[0], endColor[0], t))
            },${
                Math.round(lerp(startColor[1], endColor[1], t))
            },${
                Math.round(lerp(startColor[2], endColor[2], t))
            })`;
            colors.push(interpolatedColor);
        }
        return colors;
    }

    const startColor = [77, 111, 63];
    const endColor = [163, 230, 134];
    const backgroundColors = interpolateColors(startColor, endColor, chartLabels.length);

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Gem Visit Frequency',
                data: chartData,
                backgroundColor: 'rgb(127,179,105)',
                borderColor: 'rgba(0,0,0,0.1)',
            }]
        },
        options: {
            maintainAspectRatio: true,
            legend: { display: false },
            scales: {
                xAxes: [{ ticks: { fontStyle: 'normal' } }],
                yAxes: [{ ticks: { beginAtZero: true, fontStyle: 'normal' } }]
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('gem-pie-chart').getContext('2d');
    const data = gemDistribution;

    function interpolateColors(startColor, endColor, n) {
        const lerp = (start, end, t) => start + (end - start) * t;
        let colors = [];
        for (let i = 0; i < n; i++) {
            const t = i / (n - 1);
            const interpolatedColor = `rgb(${
                Math.round(lerp(startColor[0], endColor[0], t))
            },${
                Math.round(lerp(startColor[1], endColor[1], t))
            },${
                Math.round(lerp(startColor[2], endColor[2], t))
            })`;
            colors.push(interpolatedColor);
        }
        return colors;
    }

    const chartLabels = Object.keys(data);
    const chartData = Object.values(data);
    const startColor = [77, 111, 63];
    const endColor = [163, 230, 134];
    const backgroundColors = interpolateColors(startColor, endColor, chartLabels.length);

    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Gem Variety',
                data: chartData,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(0,0,0,0.1)',
            }]
        },
        options: {
            maintainAspectRatio: true,
            legend: {
                display: true,
                labels: {
                    fontStyle: 'normal'
                }
            },
            title: {
                display: true,
                text: 'Gem Details',
                fontStyle: 'bold'
            }
        }
    });
});
