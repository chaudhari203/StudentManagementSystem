const barCanvas = document.getElementById("barChart");

if (barCanvas) {

    const courseLabels = JSON.parse(barCanvas.dataset.labels);
    const courseCounts = JSON.parse(barCanvas.dataset.counts);

    // Bar Chart
    new Chart(barCanvas, {

        type: "bar",

        data: {

            labels: courseLabels,

            datasets: [{

                label: "Students",

                data: courseCounts,

                backgroundColor: [
                    "#0d6efd",
                    "#198754",
                    "#ffc107",
                    "#dc3545",
                    "#6f42c1",
                    "#20c997"
                ],

                borderWidth: 1

            }]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

    // Pie Chart

    new Chart(document.getElementById("pieChart"), {

        type: "pie",

        data: {

            labels: courseLabels,

            datasets: [{

                data: courseCounts,

                backgroundColor: [
                    "#0d6efd",
                    "#198754",
                    "#ffc107",
                    "#dc3545",
                    "#6f42c1",
                    "#20c997"
                ]

            }]

        },

        options: {

            responsive: true

        }

    });

}