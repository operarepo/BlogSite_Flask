let page = 1;  // начальная страница

window.addEventListener('scroll', function() {
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
        // Прокрутка до конца страницы
        fetch(`/load_data?page=${page}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.textContent = item.content;
                    document.body.appendChild(div);
                });
                page++;  // Увеличиваем страницу для следующего запроса
            });
    }
});
