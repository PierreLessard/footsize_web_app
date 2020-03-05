function search(event, item) {
    event.preventDefault();
    console.log(item)
    window.open('http://127.0.0.1:5000/searchuser/'.concat(item))
}

form = document.getElementById('form');
form.addEventListener('submit', search(event, document.getElementById('item').value))