document.getElementById('playNow').addEventListener('click', function () {
    document.getElementById('menu').style.display = 'none';
    document.getElementById('game').style.display = 'block';
});

const cells = document.querySelectorAll('.cell');

cells.forEach(cell => {
    cell.addEventListener('click', function () {
        const index = this.getAttribute('data-index');
        fetch('/api/tictactoe/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ index: index })
        })
        .then(response => response.json())
        .then(data => {
            // Apply transition effect when a cell is clicked
            this.classList.add('clicked');
            this.textContent = data.playerMove;

            // Check if the game is over and handle accordingly
            if (data.isGameOver) {
                setTimeout(() => {
                    alert(data.message);
                    // Optionally, reset the game here
                }, 100);
            }
        });
    });
});

var user_details = {};

function userLogin() {
    const apiUrl = 'http://localhost:8000/get-ip';
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        user_details = data
    })
    .catch(error => {
        console.error('There was a problem with the registration request:', error);
    });
}

window.onload = userLogin;