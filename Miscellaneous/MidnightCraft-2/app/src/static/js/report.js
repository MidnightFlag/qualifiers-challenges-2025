document.getElementById('send-report-btn').addEventListener('click', async () => {
    const responseDiv = document.getElementById('report-response');
    const button = document.getElementById('send-report-btn');

    button.disabled = true;
    button.classList.remove('bg-green-500', 'hover:bg-green-700');
    button.classList.add('bg-red-500', 'hover:bg-red-600', 'cursor-not-allowed');
    responseDiv.textContent = 'Report is being sent...';

    try {
        const response = await fetch('/report', { method: 'GET' });

        if (response.status === 429) {
            responseDiv.textContent = "You have reached the limit of reports. Please wait a few minutes and try again.";
            responseDiv.classList.add('text-red-500');
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP Error : ${response.status}`);
        }

        const data = await response.json();
        responseDiv.textContent = data.report;
        responseDiv.classList.remove('text-red-500');
        responseDiv.classList.add('text-green-500');

    } catch (error) {
        console.error('Error when trying to send the report:', error);
        responseDiv.textContent = 'We are sorry; the report could not be sent. Please retry.';
        responseDiv.classList.add('text-red-500');
    }


    setTimeout(() => {
        button.disabled = false;
        button.classList.remove('bg-red-500', 'hover:bg-red-600', 'cursor-not-allowed');
        button.classList.add('bg-green-500', 'hover:bg-green-700');
        
    }, 5000);
});
