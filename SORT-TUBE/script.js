
document.getElementById('authButton').addEventListener('click', function() {
    // Make an AJAX request to the authentication endpoint
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/authenticate', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the server
            var response = JSON.parse(xhr.responseText);
            // Perform actions based on the response
            console.log(response);
        }
    };
    xhr.send();
});

