"""
數獨生成器模組
用於生成不同難度的數獨謎題
"""

import random
from typing import List
from .sudoku_solver import SudokuSolver


class SudokuGenerator:
    """數獨謎題生成器類"""
    
    # 難度等級對應的移除格數
    DIFFICULTY_LEVELS = {
        'easy': 40,      # 簡單：移除40個格子
        'medium': 50,    # 中等：移除50個格子
        'hard': 60       # 困難：移除60個格子
    }
    
    def __init__(self):
        """初始化生成器"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
    
    def generate_puzzle(self, difficulty: str = 'medium') -> List[List[int]]:
        """
        生成指定難度的數獨謎題
        
        Args:
            difficulty: 難度等級 ('easy', 'medium', 'hard')
            
        Returns:
            List[List[int]]: 9x9的數獨謎題，0表示空格
        """
        if difficulty not in self.DIFFICULTY_LEVELS:
            raise ValueError(f"不支持的難度等級: {difficulty}")
        
        # 生成完整的數獨棋盤
        self._generate_complete_board()
        
        # 根據難度移除數字
        cells_to_remove = self.DIFFICULTY_LEVELS[difficulty]
        self._remove_numbers(cells_to_remove)
        
        return [row[:] for row in self.board]
    
    def _generate_complete_board(self) -> None:
        """生成完整的已解決數獨棋盤"""
        # 重置棋盤
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # 填充對角線的3x3子網格（它們互不影響）
        self._fill_diagonal_boxes()
        
        # 使用求解器填充其餘格子
        solver = SudokuSolver(self.board)
        solver.solve()
        self.board = solver.get_solution()
    
    def _fill_diagonal_boxes(self) -> None:
        """填充對角線上的3x3子網格"""
        for box in range(0, 9, 3):
            self._fill_box(box, box)
    
    def _fill_box(self, start_row: int, start_col: int) -> None:
        """
        填充指定的3x3子網格
        
        Args:
            start_row: 子網格起始行
            start_col: 子網格起始列
        """
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        index = 0
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                self.board[row][col] = numbers[index]
                index += 1
    
    def _remove_numbers(self, count: int) -> None:
        """
        隨機移除指定數量的數字，確保謎題仍有唯一解
        
        Args:
            count: 要移除的數字數量
        """
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= count:
                break
            
            # 保存原始值
            original_value = self.board[row][col]
            self.board[row][col] = 0
            
            # 檢查是否仍有唯一解
            solver = SudokuSolver(self.board)
            if solver.has_unique_solution():
                removed += 1
            else:
                # 恢復原值
                self.board[row][col] = original_value
    
    def is_valid_puzzle(self, board: List[List[int]]) -> bool:
        """
        檢查謎題是否有效（有唯一解）
        
        Args:
            board: 要檢查的9x9棋盤
            
        Returns:
            bool: 如果謎題有效返回True，否則返回False
        """
        solver = SudokuSolver(board)
        return solver.has_unique_solution()
    
    @staticmethod
    def get_difficulty_info() -> dict:
        """
        獲取難度等級信息
        
        Returns:
            dict: 包含各難度等級信息的字典
        """
        return {
            'easy': {
                'name': '簡單',
                'description': '適合初學者，較多提示',
                'empty_cells': SudokuGenerator.DIFFICULTY_LEVELS['easy']
            },
            'medium': {
                'name': '中等', 
                'description': '中等難度，平衡的挑戰',
                'empty_cells': SudokuGenerator.DIFFICULTY_LEVELS['medium']
            },
            'hard': {
                'name': '困難',
                'description': '高難度，較少提示',
                'empty_cells': SudokuGenerator.DIFFICULTY_LEVELS['hard']
            }
        }