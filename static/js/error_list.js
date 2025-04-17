

    document.addEventListener('DOMContentLoaded', function () {
        let errorMessages = document.querySelectorAll('.errorlist , .text-danger');

        errorMessages.forEach(function (message) {
            message.classList.remove('hidden');

            setTimeout(function () {
                message.classList.add('hidden');
            }, 5000);
        });
    });
