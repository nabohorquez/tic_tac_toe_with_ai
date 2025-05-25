window.onload = function() {
    document.getElementById('trainBtn').onclick = function () {
        this.disabled = true;
        this.textContent = "Entrenando...";
        let swalCharging = Swal.fire({
            title: 'Entrenando agente RL',
            text: 'Esto puede tardar un momento. Por favor, espera.',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
        fetch('/generate_results_train', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                swalCharging.close();
                if (data.status === 'ok') {
                    document.getElementById('rewardPlot').src = '/static/rewards.png?' + new Date().getTime();
                    Swal.fire({
                        icon: 'success',
                        title: 'Éxito',
                        text: 'Entrenamiento terminado',
                    });
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Error',
                        text: 'Error: ' + data.message,
                    });
                }
                document.getElementById('trainBtn').disabled = false;
                document.getElementById('trainBtn').textContent = "Entrenar agente RL";
            }).catch(err => {
                console.error('Error al entrenar el agente:', err);
                document.getElementById('trainBtn').disabled = false;
                document.getElementById('trainBtn').textContent = "Entrenar agente RL";
                swalCharging.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error al entrenar el agente',
                });
            });
    };

    document.getElementById('resetBtn').addEventListener('click', resetGame);
};

function renderBoard(board) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        const row = Math.floor(index / 3);
        const col = index % 3;
        let textContent = '';
        switch (board[row][col]) {
            case 1:
                textContent = 'X';
                break;
            case -1:
                textContent = 'O';
                break;
        }
        cell.textContent = textContent;
    });
}

function updateStatus(done, winner, currentPlayer) {
    const status = document.getElementById('status');
    if (done) {
        if (winner === 1) status.textContent = '¡Ganó X!';
        else if (winner === -1) status.textContent = '¡Ganó O!';
        else if (winner === 0) status.textContent = '¡Empate!';
        Swal.fire({
            icon: 'success',
            title: status.textContent,
        });
        document.querySelectorAll('.cell').forEach(cell => cell.classList.add('disabled'));
    } else {
        status.textContent = `Turno de: ${currentPlayer === 1 ? 'X' : 'O'}`;
        document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('disabled'));
    }
}

function makeMove(row, col) {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row: parseInt(row), col: parseInt(col) })
    })
        .then(res => res.json())
        .then(data => {
            renderBoard(data.board);
            updateStatus(data.done, data.winner, data.current_player);
        })
        .catch(error => {
            console.error("Error en el movimiento de la IA", error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error en el movimiento de la IA',
            });
        })
}

function resetGame() {
    fetch('/reset', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            renderBoard(data.board);
            updateStatus(false, null, data.current_player);
        })
        .catch(err => {
            console.error("Error al reiniciar el juego", error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error al reiniciar el juego',
            });
        });
}