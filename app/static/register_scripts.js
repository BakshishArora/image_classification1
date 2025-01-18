document.getElementById('register').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    //add usernam eand password to the formdata
    formData.append(username);
    formData.append(password);

    //send the data to the flask API 
    fetch( 'http://127.0.0.1:5000/register', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .catch(error => {
        alert('Error: ' + error);
    });
    
})
