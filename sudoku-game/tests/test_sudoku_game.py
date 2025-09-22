"""
數獨遊戲主類測試
"""

import unittest
import sys
import os
from unittest.mock import patch
import time

# 添加src目錄到Python路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sudoku_game import SudokuGame


class TestSudokuGame(unittest.TestCase):
    """測試數獨遊戲主類功能"""
    
    def setUp(self) -> None:
        """設置測試數據"""
        self.game = SudokuGame()
        
        # 設置一個已知的測試謎題
        self.test_puzzle = [
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
        
        self.test_solution = [
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
    
    def test_new_game(self) -> None:
        """測試開始新遊戲"""
        result = self.game.new_game('easy')
        
        # 檢查返回結果
        self.assertIsInstance(result, dict, "應該返回字典")
        self.assertIn('board', result, "應該包含棋盤")
        self.assertIn('difficulty', result, "應該包含難度")
        self.assertEqual(result['difficulty'], 'easy', "難度應該是easy")
        
        # 檢查遊戲狀態
        self.assertEqual(self.game.difficulty, 'easy', "遊戲難度應該被設置")
        self.assertIsNotNone(self.game.original_board, "原始棋盤應該被設置")
        self.assertIsNotNone(self.game.current_board, "當前棋盤應該被設置")
        self.assertIsNotNone(self.game.solution, "解答應該被設置")
        self.assertEqual(self.game.mistakes, 0, "錯誤次數應該為0")
        self.assertFalse(self.game.is_completed, "遊戲不應該完成")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_make_move_correct(self, mock_generate) -> None:
        """測試正確移動"""
        # 模擬生成已知謎題
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 進行正確移動 (0, 2) -> 4
        result = self.game.make_move(0, 2, 4)
        
        self.assertTrue(result['success'], "正確移動應該成功")
        self.assertEqual(result['message'], '正確！', "應該顯示正確消息")
        self.assertEqual(self.game.current_board[0][2], 4, "棋盤應該被更新")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_make_move_incorrect(self, mock_generate) -> None:
        """測試錯誤移動"""
        # 模擬生成已知謎題
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 進行錯誤移動 (0, 2) -> 1
        result = self.game.make_move(0, 2, 1)
        
        self.assertFalse(result['success'], "錯誤移動應該失敗")
        self.assertIn('錯誤', result['message'], "應該顯示錯誤消息")
        self.assertEqual(self.game.mistakes, 1, "錯誤次數應該增加")
        self.assertEqual(self.game.current_board[0][2], 0, "棋盤不應該被更新")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_make_move_invalid_position(self, mock_generate) -> None:
        """測試無效位置移動"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 嘗試在無效位置移動
        result = self.game.make_move(-1, 0, 1)
        self.assertFalse(result['success'], "無效位置應該失敗")
        
        result = self.game.make_move(10, 0, 1)
        self.assertFalse(result['success'], "無效位置應該失敗")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_make_move_original_cell(self, mock_generate) -> None:
        """測試修改原始數字"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 嘗試修改原始數字 (0, 0) = 5
        result = self.game.make_move(0, 0, 1)
        
        self.assertFalse(result['success'], "不應該能修改原始數字")
        self.assertIn('不能修改原始數字', result['message'], "應該顯示相應錯誤消息")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_clear_cell(self, mock_generate) -> None:
        """測試清除格子"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 先放置一個數字
        self.game.make_move(0, 2, 4)
        
        # 清除該格子
        result = self.game.clear_cell(0, 2)
        
        self.assertTrue(result['success'], "清除應該成功")
        self.assertEqual(self.game.current_board[0][2], 0, "格子應該被清空")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_clear_original_cell(self, mock_generate) -> None:
        """測試清除原始數字"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 嘗試清除原始數字
        result = self.game.clear_cell(0, 0)
        
        self.assertFalse(result['success'], "不應該能清除原始數字")
        self.assertIn('不能清除原始數字', result['message'], "應該顯示相應錯誤消息")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_get_hint(self, mock_generate) -> None:
        """測試獲取提示"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 獲取提示
        result = self.game.get_hint()
        
        self.assertTrue(result['success'], "獲取提示應該成功")
        self.assertIn('hint_position', result, "應該包含提示位置")
        self.assertIn('hint_value', result, "應該包含提示值")
        self.assertEqual(self.game.hints_used, 1, "使用的提示次數應該增加")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_get_hint_exhausted(self, mock_generate) -> None:
        """測試提示用完的情況"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 用完所有提示
        for _ in range(self.game.max_hints):
            self.game.get_hint()
        
        # 嘗試再次獲取提示
        result = self.game.get_hint()
        
        self.assertFalse(result['success'], "提示用完後應該失敗")
        self.assertIn('已用完所有提示', result['message'], "應該顯示相應消息")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_reset_game(self, mock_generate) -> None:
        """測試重置遊戲"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 進行一些移動
        self.game.make_move(0, 2, 1)  # 錯誤移動
        self.game.get_hint()
        
        # 重置遊戲
        result = self.game.reset_game()
        
        self.assertTrue(result['success'], "重置應該成功")
        self.assertEqual(self.game.mistakes, 0, "錯誤次數應該重置")
        self.assertEqual(self.game.hints_used, 0, "使用的提示應該重置")
        self.assertEqual(self.game.current_board, self.game.original_board, "棋盤應該重置到原始狀態")
    
    def test_get_game_state(self) -> None:
        """測試獲取遊戲狀態"""
        state = self.game.get_game_state()
        
        self.assertIsInstance(state, dict, "應該返回字典")
        required_fields = [
            'board', 'original_board', 'difficulty', 'elapsed_time',
            'mistakes', 'max_mistakes', 'hints_used', 'max_hints',
            'is_completed', 'completion_percentage'
        ]
        
        for field in required_fields:
            self.assertIn(field, state, f"應該包含{field}字段")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_validate_board(self, mock_generate) -> None:
        """測試棋盤驗證"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 驗證初始狀態（應該有效）
        result = self.game.validate_board()
        self.assertTrue(result['is_valid'], "初始棋盤應該有效")
        
        # 製造衝突
        self.game.current_board[0][2] = 5  # 與同行的5衝突
        
        result = self.game.validate_board()
        self.assertFalse(result['is_valid'], "有衝突的棋盤應該無效")
        self.assertGreater(len(result['errors']), 0, "應該報告錯誤")
    
    def test_is_valid_position(self) -> None:
        """測試位置有效性檢查"""
        # 測試有效位置
        self.assertTrue(self.game._is_valid_position(0, 0), "(0,0)應該有效")
        self.assertTrue(self.game._is_valid_position(8, 8), "(8,8)應該有效")
        self.assertTrue(self.game._is_valid_position(4, 4), "(4,4)應該有效")
        
        # 測試無效位置
        self.assertFalse(self.game._is_valid_position(-1, 0), "(-1,0)應該無效")
        self.assertFalse(self.game._is_valid_position(0, -1), "(0,-1)應該無效")
        self.assertFalse(self.game._is_valid_position(9, 0), "(9,0)應該無效")
        self.assertFalse(self.game._is_valid_position(0, 9), "(0,9)應該無效")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_completion_percentage(self, mock_generate) -> None:
        """測試完成百分比計算"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 計算初始完成度
        initial_percentage = self.game._get_completion_percentage()
        self.assertGreater(initial_percentage, 0, "初始完成度應該大於0")
        self.assertLess(initial_percentage, 100, "初始完成度應該小於100")
        
        # 填入一些正確答案，檢查完成度是否增加
        self.game.make_move(0, 2, 4)
        increased_percentage = self.game._get_completion_percentage()
        self.assertGreater(increased_percentage, initial_percentage, "完成度應該增加")
    
    @patch('sudoku_game.SudokuGenerator.generate_puzzle')
    def test_max_mistakes(self, mock_generate) -> None:
        """測試最大錯誤次數限制"""
        mock_generate.return_value = self.test_puzzle
        
        self.game.new_game('easy')
        
        # 犯錯直到達到最大次數
        for i in range(self.game.max_mistakes - 1):
            result = self.game.make_move(0, 2, 1)  # 錯誤移動
            self.assertFalse(result['success'], f"第{i+1}次錯誤移動應該失敗")
            self.assertNotIn('game_over', result, "遊戲還不應該結束")
        
        # 最後一次錯誤
        result = self.game.make_move(0, 2, 1)
        self.assertFalse(result['success'], "最後一次錯誤移動應該失敗")
        self.assertTrue(result.get('game_over', False), "遊戲應該結束")


if __name__ == '__main__':
    unittest.main()