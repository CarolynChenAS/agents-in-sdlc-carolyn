"""
數獨生成器測試
"""

import unittest
import sys
import os

# 添加src目錄到Python路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver


class TestSudokuGenerator(unittest.TestCase):
    """測試數獨生成器功能"""
    
    def setUp(self) -> None:
        """設置測試數據"""
        self.generator = SudokuGenerator()
    
    def test_generate_puzzle_easy(self) -> None:
        """測試生成簡單難度謎題"""
        puzzle = self.generator.generate_puzzle('easy')
        
        # 檢查棋盤尺寸
        self.assertEqual(len(puzzle), 9, "棋盤應該有9行")
        for row in puzzle:
            self.assertEqual(len(row), 9, "每行應該有9列")
        
        # 檢查空格數量（簡單難度應該有40個空格）
        empty_count = sum(1 for row in puzzle for cell in row if cell == 0)
        self.assertEqual(empty_count, 40, "簡單難度應該有40個空格")
        
        # 檢查謎題是否可解
        solver = SudokuSolver(puzzle)
        self.assertTrue(solver.solve(), "生成的謎題應該可解")
    
    def test_generate_puzzle_medium(self) -> None:
        """測試生成中等難度謎題"""
        puzzle = self.generator.generate_puzzle('medium')
        
        # 檢查空格數量（中等難度應該有50個空格）
        empty_count = sum(1 for row in puzzle for cell in row if cell == 0)
        self.assertEqual(empty_count, 50, "中等難度應該有50個空格")
        
        # 檢查謎題是否可解
        solver = SudokuSolver(puzzle)
        self.assertTrue(solver.solve(), "生成的謎題應該可解")
    
    def test_generate_puzzle_hard(self) -> None:
        """測試生成困難難度謎題"""
        puzzle = self.generator.generate_puzzle('hard')
        
        # 檢查空格數量（困難難度應該有60個空格）
        empty_count = sum(1 for row in puzzle for cell in row if cell == 0)
        self.assertEqual(empty_count, 60, "困難難度應該有60個空格")
        
        # 檢查謎題是否可解
        solver = SudokuSolver(puzzle)
        self.assertTrue(solver.solve(), "生成的謎題應該可解")
    
    def test_generate_puzzle_invalid_difficulty(self) -> None:
        """測試無效難度等級"""
        with self.assertRaises(ValueError):
            self.generator.generate_puzzle('invalid')
    
    def test_fill_diagonal_boxes(self) -> None:
        """測試填充對角線子網格"""
        self.generator._fill_diagonal_boxes()
        
        # 檢查對角線子網格是否被填充
        boxes = [(0, 0), (3, 3), (6, 6)]
        
        for start_row, start_col in boxes:
            numbers_in_box = set()
            for row in range(start_row, start_row + 3):
                for col in range(start_col, start_col + 3):
                    value = self.generator.board[row][col]
                    self.assertNotEqual(value, 0, f"對角線子網格({start_row},{start_col})不應該有空格")
                    self.assertIn(value, range(1, 10), f"值{value}應該在1-9範圍內")
                    self.assertNotIn(value, numbers_in_box, f"子網格中不應該有重複數字{value}")
                    numbers_in_box.add(value)
            
            self.assertEqual(len(numbers_in_box), 9, "每個子網格應該包含9個不同的數字")
    
    def test_fill_box(self) -> None:
        """測試填充單個子網格"""
        # 重置棋盤
        self.generator.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # 填充第一個子網格
        self.generator._fill_box(0, 0)
        
        # 檢查子網格內容
        numbers_in_box = set()
        for row in range(3):
            for col in range(3):
                value = self.generator.board[row][col]
                self.assertNotEqual(value, 0, "子網格不應該有空格")
                self.assertIn(value, range(1, 10), f"值{value}應該在1-9範圍內")
                self.assertNotIn(value, numbers_in_box, f"子網格中不應該有重複數字{value}")
                numbers_in_box.add(value)
        
        self.assertEqual(len(numbers_in_box), 9, "子網格應該包含9個不同的數字")
    
    def test_is_valid_puzzle(self) -> None:
        """測試謎題有效性檢查"""
        # 生成一個有效謎題
        valid_puzzle = self.generator.generate_puzzle('easy')
        self.assertTrue(self.generator.is_valid_puzzle(valid_puzzle), "生成的謎題應該有效")
        
        # 創建一個無效謎題（無解）
        invalid_puzzle = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.assertFalse(self.generator.is_valid_puzzle(invalid_puzzle), "無效謎題應該被識別為無效")
    
    def test_get_difficulty_info(self) -> None:
        """測試獲取難度信息"""
        info = SudokuGenerator.get_difficulty_info()
        
        # 檢查返回的數據結構
        self.assertIsInstance(info, dict, "應該返回字典")
        
        expected_difficulties = ['easy', 'medium', 'hard']
        for difficulty in expected_difficulties:
            self.assertIn(difficulty, info, f"應該包含{difficulty}難度")
            
            difficulty_info = info[difficulty]
            self.assertIn('name', difficulty_info, "應該包含name字段")
            self.assertIn('description', difficulty_info, "應該包含description字段")
            self.assertIn('empty_cells', difficulty_info, "應該包含empty_cells字段")
            
            # 檢查empty_cells值是否正確
            expected_cells = SudokuGenerator.DIFFICULTY_LEVELS[difficulty]
            self.assertEqual(difficulty_info['empty_cells'], expected_cells, 
                           f"{difficulty}難度的空格數量應該是{expected_cells}")
    
    def test_puzzle_uniqueness(self) -> None:
        """測試生成的謎題具有唯一性"""
        # 生成兩個謎題並檢查它們是否不同
        puzzle1 = self.generator.generate_puzzle('easy')
        puzzle2 = self.generator.generate_puzzle('easy')
        
        self.assertNotEqual(puzzle1, puzzle2, "連續生成的謎題應該不同")
    
    def test_generated_puzzle_validity(self) -> None:
        """測試生成謎題的有效性"""
        for difficulty in ['easy', 'medium', 'hard']:
            with self.subTest(difficulty=difficulty):
                puzzle = self.generator.generate_puzzle(difficulty)
                
                # 檢查所有數字都在有效範圍內
                for row in puzzle:
                    for cell in row:
                        self.assertIn(cell, range(0, 10), f"格子值{cell}應該在0-9範圍內")
                
                # 檢查初始狀態沒有衝突
                self.assertTrue(self._check_initial_validity(puzzle), 
                              f"{difficulty}難度的初始謎題應該沒有衝突")
    
    def _check_initial_validity(self, board) -> bool:
        """檢查初始棋盤狀態是否有效（沒有重複數字）"""
        # 檢查行
        for row in range(9):
            seen = set()
            for col in range(9):
                value = board[row][col]
                if value != 0:
                    if value in seen:
                        return False
                    seen.add(value)
        
        # 檢查列
        for col in range(9):
            seen = set()
            for row in range(9):
                value = board[row][col]
                if value != 0:
                    if value in seen:
                        return False
                    seen.add(value)
        
        # 檢查3x3子網格
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = set()
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        value = board[row][col]
                        if value != 0:
                            if value in seen:
                                return False
                            seen.add(value)
        
        return True


if __name__ == '__main__':
    unittest.main()