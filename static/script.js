document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var bookName = document.getElementById('bookName').value;
    fetch('/recommend', {
        method: 'POST',
        body: JSON.stringify({ bookName: bookName }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultSection').style.display = 'block';
        var recommendationsList = document.getElementById('recommendationsList');
        recommendationsList.innerHTML = '';
        data.forEach(function(book) {
            var li = document.createElement('li');
            li.textContent = book;
            recommendationsList.appendChild(li);
        });
    });
});