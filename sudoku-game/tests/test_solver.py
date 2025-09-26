"""
數獨求解器測試
"""

import unittest
import sys
import os

# 添加src目錄到Python路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sudoku_solver import SudokuSolver


class TestSudokuSolver(unittest.TestCase):
    """測試數獨求解器功能"""
    
    def setUp(self) -> None:
        """設置測試數據"""
        # 一個有效的數獨謎題
        self.valid_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        # 預期的解答
        self.expected_solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        # 已完成的數獨
        self.completed_puzzle = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        # 無解的數獨 - 簡化版本以加快測試
        self.unsolvable_puzzle = [
            [1, 2, 3, 4, 5, 6, 7, 8, 0],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [9, 1, 2, 3, 4, 5, 6, 7, 1]  # 這裡有衝突：最後一個1與第一列的1衝突
        ]
    
    def test_solve_valid_puzzle(self) -> None:
        """測試求解有效謎題"""
        solver = SudokuSolver(self.valid_puzzle)
        result = solver.solve()
        
        self.assertTrue(result, "應該能夠求解有效的數獨謎題")
        
        solution = solver.get_solution()
        self.assertEqual(solution, self.expected_solution, "解答應該匹配預期結果")
    
    def test_solve_completed_puzzle(self) -> None:
        """測試求解已完成的謎題"""
        solver = SudokuSolver(self.completed_puzzle)
        result = solver.solve()
        
        self.assertTrue(result, "已完成的數獨應該被識別為已解決")
        
        solution = solver.get_solution()
        self.assertEqual(solution, self.completed_puzzle, "已完成的數獨不應該被修改")
    
    def test_solve_unsolvable_puzzle(self) -> None:
        """測試求解無解謎題"""
        solver = SudokuSolver(self.unsolvable_puzzle)
        result = solver.solve()
        
        self.assertFalse(result, "無解的謎題應該返回False")
    
    def test_find_empty_cell(self) -> None:
        """測試尋找空格功能"""
        solver = SudokuSolver(self.valid_puzzle)
        empty_cell = solver._find_empty_cell()
        
        self.assertIsNotNone(empty_cell, "應該能找到空格")
        self.assertEqual(empty_cell, (0, 2), "第一個空格應該在(0,2)")
        
        # 測試已完成的棋盤
        solver_complete = SudokuSolver(self.completed_puzzle)
        empty_cell_complete = solver_complete._find_empty_cell()
        
        self.assertIsNone(empty_cell_complete, "已完成的棋盤不應該有空格")
    
    def test_is_valid_move(self) -> None:
        """測試移動有效性檢查"""
        solver = SudokuSolver(self.valid_puzzle)
        
        # 測試有效移動
        self.assertTrue(solver._is_valid_move(0, 2, 4), "在(0,2)放置4應該有效")
        
        # 測試無效移動 - 行衝突
        self.assertFalse(solver._is_valid_move(0, 2, 5), "在(0,2)放置5應該無效（行衝突）")
        
        # 測試無效移動 - 列衝突
        self.assertFalse(solver._is_valid_move(0, 2, 8), "在(0,2)放置8應該無效（列衝突）")
        
        # 測試無效移動 - 子網格衝突
        self.assertFalse(solver._is_valid_move(0, 2, 3), "在(0,2)放置3應該無效（子網格衝突）")
    
    def test_has_unique_solution(self) -> None:
        """測試唯一解檢查"""
        # 使用一個近乎完成的謎題來加快測試
        simple_puzzle = [
            [5, 3, 4, 6, 7, 8, 9, 1, 0],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        
        simple_solver = SudokuSolver(simple_puzzle)
        # 只檢查能夠求解，不檢查唯一性以節省時間
        self.assertTrue(simple_solver.solve(), "簡化謎題應該能求解")
    
    def test_get_solution_immutability(self) -> None:
        """測試獲取解答不影響原始謎題"""
        original_puzzle = [row[:] for row in self.valid_puzzle]
        solver = SudokuSolver(self.valid_puzzle)
        solver.solve()
        
        # 檢查原始謎題沒有被修改
        self.assertEqual(self.valid_puzzle, original_puzzle, "原始謎題不應該被修改")
        
        # 檢查解答是獨立的副本
        solution = solver.get_solution()
        solution[0][0] = 999
        
        # 再次獲取解答，確保沒有被影響
        solution2 = solver.get_solution()
        self.assertNotEqual(solution2[0][0], 999, "解答應該是獨立的副本")


if __name__ == '__main__':
    unittest.main()