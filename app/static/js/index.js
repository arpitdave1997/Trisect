
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
var session_details = {};
var base_url = 'http://127.0.0.1:8000'
var register_path = '/users/details'
var update_path = '/users/activity/'
var websocket_path = '/gameplay'

document.getElementById('play-now').addEventListener('click', async function () {
    document.getElementById('menu').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    await initiateGameplay();

    document.getElementById('loading').style.display = 'none';
    document.getElementById('game').style.display = 'block';
});

async function initiateGameplay(url) {
    return new Promise((resolve, reject) => {
        url = base_url.concat(websocket_path)

        const socket = new WebSocket(url);
        const initiateGameplayBody = JSON.stringify({
            "case": "initiate_session",
            "user_id": user_details.user_id
        });

        socket.addEventListener('open', function () {
            socket.send(initiateGameplayBody);
        });

        socket.addEventListener('message', function (event) {
            session_details = JSON.parse(event.data)[1]
            resolve(event.data);
        });

        socket.addEventListener('error', function (error) {
            console.error('WebSocket error: ', error);
            reject(error);
        });
    });
}


async function registerUser() {
    const url = base_url.concat(register_path);
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        user_details = data;
        document.getElementById('menu').style.display = 'block';
        document.getElementById('loading').style.display = 'none';

        return user_details;
    } catch (error) {
        console.error('There was a problem with the registration request:', error);
        throw error;
    }
}

async function updateUserActivity(user_id) {
    const url = base_url.concat(update_path, user_id)
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.status;
    } catch (error) {
        console.error('There was a problem with the registration request:', error);
        throw error;
    }
}

async function onloadActions() {
    while (true) {
        if (!user_details.user_id) {
            await registerUser()
        } 
        await new Promise(r => setTimeout(r, 5000));
        await updateUserActivity(user_details.user_id)
    }
}

window.onload = onloadActions;