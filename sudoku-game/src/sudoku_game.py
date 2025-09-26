"""
數獨遊戲主類
管理遊戲狀態、驗證和用戶交互
"""

import time
from typing import List, Optional, Tuple, Dict, Any
from .sudoku_generator import SudokuGenerator
from .sudoku_solver import SudokuSolver


class SudokuGame:
    """數獨遊戲主類，管理遊戲邏輯和狀態"""
    
    def __init__(self):
        """初始化遊戲"""
        self.generator = SudokuGenerator()
        self.original_board: List[List[int]] = []
        self.current_board: List[List[int]] = []
        self.solution: List[List[int]] = []
        self.start_time: float = 0
        self.difficulty: str = 'medium'
        self.mistakes: int = 0
        self.max_mistakes: int = 3
        self.is_completed: bool = False
        self.hints_used: int = 0
        self.max_hints: int = 3
    
    def new_game(self, difficulty: str = 'medium') -> Dict[str, Any]:
        """
        開始新遊戲
        
        Args:
            difficulty: 難度等級 ('easy', 'medium', 'hard')
            
        Returns:
            Dict[str, Any]: 遊戲狀態信息
        """
        self.difficulty = difficulty
        self.original_board = self.generator.generate_puzzle(difficulty)
        self.current_board = [row[:] for row in self.original_board]
        
        # 獲取解答
        solver = SudokuSolver(self.original_board)
        solver.solve()
        self.solution = solver.get_solution()
        
        # 重置遊戲狀態
        self.start_time = time.time()
        self.mistakes = 0
        self.is_completed = False
        self.hints_used = 0
        
        return self.get_game_state()
    
    def make_move(self, row: int, col: int, value: int) -> Dict[str, Any]:
        """
        在指定位置放置數字
        
        Args:
            row: 行索引 (0-8)
            col: 列索引 (0-8)
            value: 要放置的數字 (1-9)
            
        Returns:
            Dict[str, Any]: 移動結果和遊戲狀態
        """
        if not self._is_valid_position(row, col):
            return {
                'success': False,
                'message': '無效的位置',
                'game_state': self.get_game_state()
            }
        
        if self.original_board[row][col] != 0:
            return {
                'success': False,
                'message': '不能修改原始數字',
                'game_state': self.get_game_state()
            }
        
        if not (1 <= value <= 9):
            return {
                'success': False,
                'message': '數字必須在1-9之間',
                'game_state': self.get_game_state()
            }
        
        # 檢查移動是否正確
        is_correct = self.solution[row][col] == value
        
        if is_correct:
            self.current_board[row][col] = value
            
            # 檢查是否完成遊戲
            if self._is_puzzle_completed():
                self.is_completed = True
                
            return {
                'success': True,
                'message': '正確！' if not self.is_completed else '恭喜完成！',
                'is_completed': self.is_completed,
                'game_state': self.get_game_state()
            }
        else:
            self.mistakes += 1
            
            # 檢查是否超過最大錯誤次數
            if self.mistakes >= self.max_mistakes:
                return {
                    'success': False,
                    'message': f'遊戲結束！超過{self.max_mistakes}次錯誤',
                    'game_over': True,
                    'game_state': self.get_game_state()
                }
            
            return {
                'success': False,
                'message': f'錯誤！剩餘機會：{self.max_mistakes - self.mistakes}',
                'game_state': self.get_game_state()
            }
    
    def clear_cell(self, row: int, col: int) -> Dict[str, Any]:
        """
        清除指定位置的數字
        
        Args:
            row: 行索引
            col: 列索引
            
        Returns:
            Dict[str, Any]: 操作結果
        """
        if not self._is_valid_position(row, col):
            return {
                'success': False,
                'message': '無效的位置'
            }
        
        if self.original_board[row][col] != 0:
            return {
                'success': False,
                'message': '不能清除原始數字'
            }
        
        self.current_board[row][col] = 0
        return {
            'success': True,
            'message': '已清除',
            'game_state': self.get_game_state()
        }
    
    def get_hint(self) -> Dict[str, Any]:
        """
        獲取提示
        
        Returns:
            Dict[str, Any]: 提示信息
        """
        if self.hints_used >= self.max_hints:
            return {
                'success': False,
                'message': '已用完所有提示'
            }
        
        # 尋找空格
        empty_cells = []
        for row in range(9):
            for col in range(9):
                if (self.current_board[row][col] == 0 and 
                    self.original_board[row][col] == 0):
                    empty_cells.append((row, col))
        
        if not empty_cells:
            return {
                'success': False,
                'message': '沒有可提示的位置'
            }
        
        # 隨機選擇一個空格給予提示
        import random
        row, col = random.choice(empty_cells)
        correct_value = self.solution[row][col]
        
        self.hints_used += 1
        
        return {
            'success': True,
            'message': f'提示：第{row+1}行第{col+1}列應該是{correct_value}',
            'hint_position': (row, col),
            'hint_value': correct_value,
            'hints_remaining': self.max_hints - self.hints_used,
            'game_state': self.get_game_state()
        }
    
    def reset_game(self) -> Dict[str, Any]:
        """
        重置當前遊戲到初始狀態
        
        Returns:
            Dict[str, Any]: 重置後的遊戲狀態
        """
        self.current_board = [row[:] for row in self.original_board]
        self.start_time = time.time()
        self.mistakes = 0
        self.is_completed = False
        self.hints_used = 0
        
        return {
            'success': True,
            'message': '遊戲已重置',
            'game_state': self.get_game_state()
        }
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        獲取當前遊戲狀態
        
        Returns:
            Dict[str, Any]: 遊戲狀態信息
        """
        elapsed_time = int(time.time() - self.start_time) if self.start_time > 0 else 0
        
        return {
            'board': self.current_board,
            'original_board': self.original_board,
            'difficulty': self.difficulty,
            'elapsed_time': elapsed_time,
            'mistakes': self.mistakes,
            'max_mistakes': self.max_mistakes,
            'hints_used': self.hints_used,
            'max_hints': self.max_hints,
            'is_completed': self.is_completed,
            'completion_percentage': self._get_completion_percentage()
        }
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """檢查位置是否有效"""
        return 0 <= row < 9 and 0 <= col < 9
    
    def _is_puzzle_completed(self) -> bool:
        """檢查謎題是否完成"""
        for row in range(9):
            for col in range(9):
                if self.current_board[row][col] == 0:
                    return False
        return True
    
    def _get_completion_percentage(self) -> float:
        """計算完成百分比"""
        total_cells = 81
        filled_cells = sum(1 for row in range(9) for col in range(9) 
                          if self.current_board[row][col] != 0)
        return round((filled_cells / total_cells) * 100, 1)
    
    def validate_board(self) -> Dict[str, Any]:
        """
        驗證當前棋盤狀態
        
        Returns:
            Dict[str, Any]: 驗證結果
        """
        errors = []
        
        # 檢查每行
        for row in range(9):
            seen = set()
            for col in range(9):
                value = self.current_board[row][col]
                if value != 0:
                    if value in seen:
                        errors.append(f'第{row+1}行有重複數字: {value}')
                    seen.add(value)
        
        # 檢查每列
        for col in range(9):
            seen = set()
            for row in range(9):
                value = self.current_board[row][col]
                if value != 0:
                    if value in seen:
                        errors.append(f'第{col+1}列有重複數字: {value}')
                    seen.add(value)
        
        # 檢查每個3x3子網格
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = set()
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        value = self.current_board[row][col]
                        if value != 0:
                            if value in seen:
                                errors.append(f'第{box_row//3+1}-{box_col//3+1}子網格有重複數字: {value}')
                            seen.add(value)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }