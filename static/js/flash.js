// Auto hide flash messages after 4 seconds

window.addEventListener("DOMContentLoaded", () => {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        setTimeout(() => {

            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);

            bsAlert.close();

        }, 4000);

    });

});