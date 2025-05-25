window.onload = function() {
    document.getElementById('trainBtn').onclick = function () {
        this.disabled = true;
        this.textContent = "Entrenando...";
        fetch('/generate_results_train', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    document.getElementById('rewardPlot').src = '/static/rewards.png?' + new Date().getTime();
                    alert('Entrenamiento terminado');
                } else {
                    alert('Error: ' + data.message);
                }
                document.getElementById('trainBtn').disabled = false;
                document.getElementById('trainBtn').textContent = "Entrenar agente RL";
            }).catch(err => {
                console.error('Error al entrenar el agente:', err);
                alert('Error al entrenar el agente');
                document.getElementById('trainBtn').disabled = false;
                document.getElementById('trainBtn').textContent = "Entrenar agente RL";
            });
    };

    document.getElementById('resetBtn').addEventListener('click', resetGame);
};

function renderBoard(board) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        const row = Math.floor(index / 3);
        const col = index % 3;
        cell.textContent = board[row][col] === 1 ? 'X' : board[row][col] === -1 ? 'O' : '';
    });
}

function updateStatus(done, winner, currentPlayer) {
    const status = document.getElementById('status');
    if (done) {
        if (winner === 1) status.textContent = '¡Ganó X!';
        else if (winner === -1) status.textContent = '¡Ganó O!';
        else status.textContent = '¡Empate!';
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

            // Opcional: resalta el movimiento de la IA
            if (data.ia_move) {
                let cell = document.querySelector(`.cell[data-row="${data.ia_move.row}"][data-col="${data.ia_move.col}"]`);
                if (cell) cell.classList.add('table-warning');
            }
        });
}

function resetGame() {
    fetch('/reset', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            renderBoard(data.board);
            updateStatus(false, null, data.current_player);
        })
        .catch(err => {
            alert('Error al reiniciar el juego: ' + err.message);
        });
}