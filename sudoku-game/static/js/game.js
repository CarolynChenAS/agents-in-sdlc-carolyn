/**
 * 數獨遊戲前端邏輯
 * 處理用戶交互和遊戲狀態管理
 */

class SudokuGameUI {
    constructor() {
        this.selectedCell = null;
        this.selectedNumber = null;
        this.timerInterval = null;
        this.gameState = null;
        
        this.initializeGame();
        this.bindEvents();
    }

    /**
     * 初始化遊戲
     */
    async initializeGame() {
        try {
            await this.startNewGame();
            this.showMessage('遊戲已準備就緒！選擇一個格子開始填數字。', 'info');
        } catch (error) {
            this.showMessage('初始化遊戲失敗: ' + error.message, 'error');
        }
    }

    /**
     * 綁定事件監聽器
     */
    bindEvents() {
        // 控制按鈕事件
        document.getElementById('new-game-btn').addEventListener('click', () => this.startNewGame());
        document.getElementById('reset-btn').addEventListener('click', () => this.resetGame());
        document.getElementById('hint-btn').addEventListener('click', () => this.getHint());
        document.getElementById('validate-btn').addEventListener('click', () => this.validateBoard());
        
        // 數字按鈕事件
        document.querySelectorAll('.number-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const number = parseInt(e.target.dataset.number);
                this.selectNumber(number);
            });
        });
        
        // 清除按鈕事件
        document.getElementById('clear-btn').addEventListener('click', () => this.clearCell());
        
        // 模態框事件
        document.getElementById('new-game-modal-btn').addEventListener('click', () => {
            this.closeModal();
            this.startNewGame();
        });
        document.getElementById('close-modal-btn').addEventListener('click', () => this.closeModal());
        
        // 鍵盤事件
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // 點擊模態框背景關閉
        document.getElementById('completion-modal').addEventListener('click', (e) => {
            if (e.target.id === 'completion-modal') {
                this.closeModal();
            }
        });
    }

    /**
     * 生成數獨棋盤
     */
    generateBoard() {
        const board = document.getElementById('sudoku-board');
        board.innerHTML = '';
        
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                const cell = document.createElement('div');
                cell.className = 'sudoku-cell';
                cell.dataset.row = row;
                cell.dataset.col = col;
                
                cell.addEventListener('click', () => this.selectCell(row, col));
                
                board.appendChild(cell);
            }
        }
    }

    /**
     * 更新棋盤顯示
     */
    updateBoard() {
        if (!this.gameState) return;
        
        const cells = document.querySelectorAll('.sudoku-cell');
        
        cells.forEach((cell, index) => {
            const row = Math.floor(index / 9);
            const col = index % 9;
            const value = this.gameState.board[row][col];
            const originalValue = this.gameState.original_board[row][col];
            
            // 清除所有樣式類
            cell.classList.remove('original', 'hint', 'error');
            
            // 設置值
            cell.textContent = value === 0 ? '' : value;
            
            // 設置樣式
            if (originalValue !== 0) {
                cell.classList.add('original');
            }
        });
    }

    /**
     * 選擇格子
     */
    selectCell(row, col) {
        // 移除之前選中的格子
        document.querySelectorAll('.sudoku-cell.selected').forEach(cell => {
            cell.classList.remove('selected');
        });
        
        // 選中新格子
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        if (cell) {
            cell.classList.add('selected');
            this.selectedCell = { row, col };
        }
    }

    /**
     * 選擇數字
     */
    selectNumber(number) {
        // 移除之前選中的數字
        document.querySelectorAll('.number-btn.selected').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        // 選中新數字
        const btn = document.querySelector(`[data-number="${number}"]`);
        if (btn) {
            btn.classList.add('selected');
            this.selectedNumber = number;
            
            // 如果有選中的格子，直接填入數字
            if (this.selectedCell) {
                this.makeMove(this.selectedCell.row, this.selectedCell.col, number);
            }
        }
    }

    /**
     * 進行移動
     */
    async makeMove(row, col, value) {
        try {
            const response = await fetch('/api/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ row, col, value })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.gameState = result.game_state;
                this.updateBoard();
                this.updateGameInfo();
                
                if (result.is_completed) {
                    this.showCompletionModal();
                } else {
                    this.showMessage(result.message, 'success');
                }
            } else {
                this.showMessage(result.message, 'error');
                if (result.game_over) {
                    this.stopTimer();
                }
            }
        } catch (error) {
            this.showMessage('移動失敗: ' + error.message, 'error');
        }
    }

    /**
     * 清除格子
     */
    async clearCell() {
        if (!this.selectedCell) {
            this.showMessage('請先選擇一個格子', 'error');
            return;
        }
        
        try {
            const response = await fetch('/api/clear_cell', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    row: this.selectedCell.row,
                    col: this.selectedCell.col
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.gameState = result.game_state;
                this.updateBoard();
                this.updateGameInfo();
                this.showMessage(result.message, 'success');
            } else {
                this.showMessage(result.message, 'error');
            }
        } catch (error) {
            this.showMessage('清除失敗: ' + error.message, 'error');
        }
    }

    /**
     * 獲取提示
     */
    async getHint() {
        try {
            const response = await fetch('/api/get_hint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                const [row, col] = result.hint_position;
                const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
                
                if (cell) {
                    cell.classList.add('hint');
                    setTimeout(() => cell.classList.remove('hint'), 3000);
                }
                
                this.gameState = result.game_state;
                this.updateGameInfo();
                this.showMessage(result.message, 'info');
            } else {
                this.showMessage(result.message, 'error');
            }
        } catch (error) {
            this.showMessage('獲取提示失敗: ' + error.message, 'error');
        }
    }

    /**
     * 開始新遊戲
     */
    async startNewGame() {
        const difficulty = document.getElementById('difficulty').value;
        
        try {
            const response = await fetch('/api/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ difficulty })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.gameState = result.data;
                this.generateBoard();
                this.updateBoard();
                this.updateGameInfo();
                this.startTimer();
                this.showMessage('新遊戲開始！', 'success');
            } else {
                this.showMessage('創建新遊戲失敗: ' + result.message, 'error');
            }
        } catch (error) {
            this.showMessage('創建新遊戲失敗: ' + error.message, 'error');
        }
    }

    /**
     * 重置遊戲
     */
    async resetGame() {
        try {
            const response = await fetch('/api/reset_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.gameState = result.game_state;
                this.updateBoard();
                this.updateGameInfo();
                this.startTimer();
                this.showMessage(result.message, 'success');
            } else {
                this.showMessage('重置遊戲失敗: ' + result.message, 'error');
            }
        } catch (error) {
            this.showMessage('重置遊戲失敗: ' + error.message, 'error');
        }
    }

    /**
     * 驗證棋盤
     */
    async validateBoard() {
        try {
            const response = await fetch('/api/validate_board', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                const validation = result.data;
                if (validation.is_valid) {
                    this.showMessage('棋盤目前沒有錯誤！', 'success');
                } else {
                    this.showMessage('發現錯誤: ' + validation.errors.join(', '), 'error');
                }
            } else {
                this.showMessage('驗證失敗: ' + result.message, 'error');
            }
        } catch (error) {
            this.showMessage('驗證失敗: ' + error.message, 'error');
        }
    }

    /**
     * 更新遊戲信息顯示
     */
    updateGameInfo() {
        if (!this.gameState) return;
        
        document.getElementById('mistakes').textContent = 
            `${this.gameState.mistakes}/${this.gameState.max_mistakes}`;
        document.getElementById('hints').textContent = 
            `${this.gameState.max_hints - this.gameState.hints_used}/${this.gameState.max_hints}`;
        document.getElementById('progress').textContent = 
            `${this.gameState.completion_percentage}%`;
    }

    /**
     * 開始計時器
     */
    startTimer() {
        this.stopTimer();
        this.timerInterval = setInterval(() => {
            if (this.gameState) {
                this.gameState.elapsed_time++;
                this.updateTimer();
            }
        }, 1000);
    }

    /**
     * 停止計時器
     */
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    /**
     * 更新計時器顯示
     */
    updateTimer() {
        if (!this.gameState) return;
        
        const time = this.gameState.elapsed_time;
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        document.getElementById('timer').textContent = timeString;
    }

    /**
     * 顯示完成模態框
     */
    showCompletionModal() {
        this.stopTimer();
        
        const time = this.gameState.elapsed_time;
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        const timeString = `${minutes}分${seconds}秒`;
        
        document.getElementById('final-time').textContent = timeString;
        document.getElementById('final-mistakes').textContent = this.gameState.mistakes;
        document.getElementById('final-hints').textContent = this.gameState.hints_used;
        document.getElementById('final-difficulty').textContent = this.getDifficultyName(this.gameState.difficulty);
        
        document.getElementById('completion-modal').style.display = 'block';
    }

    /**
     * 關閉模態框
     */
    closeModal() {
        document.getElementById('completion-modal').style.display = 'none';
    }

    /**
     * 獲取難度名稱
     */
    getDifficultyName(difficulty) {
        const names = {
            'easy': '簡單',
            'medium': '中等',
            'hard': '困難'
        };
        return names[difficulty] || difficulty;
    }

    /**
     * 處理鍵盤輸入
     */
    handleKeyboard(e) {
        // 數字鍵 1-9
        if (e.key >= '1' && e.key <= '9' && this.selectedCell) {
            const number = parseInt(e.key);
            this.selectNumber(number);
        }
        
        // 刪除鍵
        if ((e.key === 'Delete' || e.key === 'Backspace') && this.selectedCell) {
            this.clearCell();
        }
        
        // 方向鍵
        if (this.selectedCell) {
            let newRow = this.selectedCell.row;
            let newCol = this.selectedCell.col;
            
            switch (e.key) {
                case 'ArrowUp':
                    newRow = Math.max(0, newRow - 1);
                    break;
                case 'ArrowDown':
                    newRow = Math.min(8, newRow + 1);
                    break;
                case 'ArrowLeft':
                    newCol = Math.max(0, newCol - 1);
                    break;
                case 'ArrowRight':
                    newCol = Math.min(8, newCol + 1);
                    break;
            }
            
            if (newRow !== this.selectedCell.row || newCol !== this.selectedCell.col) {
                this.selectCell(newRow, newCol);
                e.preventDefault();
            }
        }
    }

    /**
     * 顯示消息
     */
    showMessage(message, type = 'info') {
        const messageArea = document.getElementById('message-area');
        messageArea.textContent = message;
        messageArea.className = `message-area ${type}`;
        
        // 3秒後清除消息
        setTimeout(() => {
            messageArea.textContent = '';
            messageArea.className = 'message-area';
        }, 3000);
    }
}

// 頁面加載完成後初始化遊戲
document.addEventListener('DOMContentLoaded', () => {
    new SudokuGameUI();
});