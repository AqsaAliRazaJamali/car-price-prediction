document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const themeBtn = document.getElementById('themeToggle');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsPanel = document.getElementById('resultsPanel');
    const errorAlert = document.getElementById('errorAlert');

    themeBtn.addEventListener('click', () => {
        const activeTheme = document.documentElement.getAttribute('data-theme');
        const nextTheme = activeTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', nextTheme);
        themeBtn.textContent = nextTheme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
    });

    window.resetForm = function() {
        if(form) {
            form.reset();
            resultsPanel.style.display = 'none';
            errorAlert.style.display = 'none';
        }
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorAlert.style.display = 'none';
            resultsPanel.style.display = 'none';
            loadingSpinner.style.display = 'block';

            const payload = {
                brand: document.getElementById('brand').value,
                year: parseInt(document.getElementById('year').value),
                present_price: parseFloat(document.getElementById('present_price').value),
                kms_driven: parseInt(document.getElementById('kms_driven').value),
                fuel_type: document.getElementById('fuel_type').value,
                seller_type: document.getElementById('seller_type').value,
                transmission: document.getElementById('transmission').value,
                owner: parseInt(document.getElementById('owner').value)
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    document.getElementById('calcPrice').textContent = `$${result.predicted_price.toLocaleString()} Lakhs`;
                    document.getElementById('calcEngine').textContent = result.model_used;
                    document.getElementById('calcConf').textContent = result.accuracy_metric;
                    
                    loadingSpinner.style.display = 'none';
                    resultsPanel.style.display = 'block';
                } else {
                    showError(result.error || "Prediction processing crashed.");
                }
            } catch (err) {
                showError("Could not reach backend. Is Flask running?");
            }
        });
    }

    function showError(msg) {
        loadingSpinner.style.display = 'none';
        errorAlert.textContent = msg;
        errorAlert.style.display = 'block';
    }
});