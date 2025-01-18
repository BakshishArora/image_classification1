document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const imageUrl = document.getElementById('image_url').value;

    // Add username and password to the form data
    formData.append('username', username);
    formData.append('password', password);
    formData.append('image_url', image_url);

    // Clear previous result
    document.getElementById('classification-result').style.display = 'none';
    document.getElementById('result-text').textContent = '';

    // Send data to the Flask API
    fetch('http://127.0.0.1:5000/classify', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data =>{
        if (data.Classification) {
            // Display the prediction result
            document.getElementById('result-text').textContent = 'Class ${data.Classification}';
            document.getElementById('prediction-result').style.display = 'block';
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});
