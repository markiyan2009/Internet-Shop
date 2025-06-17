document.addEventListener('DOMContentLoaded', () => {
    const reviewAddButton = document.getElementById('add-review');
    console.log(reviewAddButton)
    if (reviewAddButton) {
        const checkPermUrl = reviewAddButton.dataset.checkPermUrl;
        const reviewFormUrl = reviewAddButton.dataset.reviewUrl;

        reviewAddButton.addEventListener('click', () => {
            fetch(checkPermUrl, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.has_perm) {
                    // перенаправити користувача на форму додавання відгуку
                    window.location.href = reviewFormUrl;
                } else {
                    alert("У вас немає прав на додавання відгуку.");
                }
            })
            .catch(error => {
                console.error("Помилка при перевірці дозволу:", error);
            });
        });
    }
});