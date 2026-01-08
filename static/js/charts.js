let vitalsChart;

function initChart() {
    const ctx = document.getElementById("vitalsChart");
    if (!ctx) return;

    vitalsChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [
                "Age","Sex","Chest Pain","BP","Cholesterol",
                "Sugar","ECG","Max HR","Angina",
                "Oldpeak","Slope","CA","Thal"
            ],
            datasets: [{
                label: "Patient Clinical Inputs",
                data: Array(13).fill(0),
                backgroundColor: [
                    "#ff4b5c","#ffd84d","#4da6ff","#ff4b5c","#ffd84d",
                    "#4da6ff","#ff4b5c","#ffd84d","#4da6ff",
                    "#ff4b5c","#ffd84d","#4da6ff","#ff4b5c"
                ]
            }]
        },
        options: {
            responsive: true,
            animation: { duration: 900 },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateChartFromInputs(valuesArray){
    if (!vitalsChart) return;
    vitalsChart.data.datasets[0].data = valuesArray;
    vitalsChart.update();
}
