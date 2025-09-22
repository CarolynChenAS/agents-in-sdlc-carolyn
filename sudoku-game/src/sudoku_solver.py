"""
數獨求解器模組
提供數獨謎題的求解算法
"""

from typing import List, Optional, Tuple


class SudokuSolver:
    """數獨求解器類，使用回溯算法求解數獨謎題"""
    
    def __init__(self, board: List[List[int]]):
        """
        初始化求解器
        
        Args:
            board: 9x9的數獨棋盤，0表示空格
        """
        self.board = [row[:] for row in board]  # 深拷貝棋盤
    
    def solve(self) -> bool:
        """
        求解數獨謎題
        
        Returns:
            bool: 如果找到解返回True，否則返回False
        """
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return True  # 沒有空格，謎題已解決
        
        row, col = empty_cell
        
        for num in range(1, 10):
            if self._is_valid_move(row, col, num):
                self.board[row][col] = num
                
                if self.solve():
                    return True
                
                # 回溯
                self.board[row][col] = 0
        
        return False
    
    def _find_empty_cell(self) -> Optional[Tuple[int, int]]:
        """
        尋找第一個空格
        
        Returns:
            Optional[Tuple[int, int]]: 空格的(行, 列)座標，如果沒有空格返回None
        """
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None
    
    def _is_valid_move(self, row: int, col: int, num: int) -> bool:
        """
        檢查在指定位置放置數字是否有效
        
        Args:
            row: 行索引
            col: 列索引  
            num: 要放置的數字
            
        Returns:
            bool: 如果移動有效返回True，否則返回False
        """
        # 檢查行
        for c in range(9):
            if self.board[row][c] == num:
                return False
        
        # 檢查列
        for r in range(9):
            if self.board[r][col] == num:
                return False
        
        # 檢查3x3子網格
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False
        
        return True
    
    def get_solution(self) -> List[List[int]]:
        """
        獲取求解後的棋盤
        
        Returns:
            List[List[int]]: 求解後的9x9棋盤
        """
        return [row[:] for row in self.board]
    
    def has_unique_solution(self) -> bool:
        """
        檢查謎題是否有唯一解
        
        Returns:
            bool: 如果有唯一解返回True，否則返回False
        """
        solutions = []
        self._find_all_solutions(solutions, max_solutions=2)
        return len(solutions) == 1
    
    def _find_all_solutions(self, solutions: List[List[List[int]]], max_solutions: int = 2) -> None:
        """
        尋找所有可能的解（最多找到max_solutions個）
        
        Args:
            solutions: 用於存儲解的列表
            max_solutions: 最大解的數量
        """
        if len(solutions) >= max_solutions:
            return
        
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            solutions.append([row[:] for row in self.board])
            return
        
        row, col = empty_cell
        
        for num in range(1, 10):
            if self._is_valid_move(row, col, num):
                self.board[row][col] = num
                self._find_all_solutions(solutions, max_solutions)
                self.board[row][col] = 0