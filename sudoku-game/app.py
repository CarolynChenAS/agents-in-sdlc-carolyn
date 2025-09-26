"""
數獨遊戲 Flask 應用
提供 Web 界面和 API 端點
"""

from flask import Flask, render_template, request, jsonify
from src.sudoku_game import SudokuGame
from src.sudoku_generator import SudokuGenerator

app = Flask(__name__)

# 遊戲實例（在生產環境中應該使用會話管理）
game = SudokuGame()


@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """開始新遊戲"""
    try:
        data = request.get_json() or {}
        difficulty = data.get('difficulty', 'medium')
        
        result = game.new_game(difficulty)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'創建新遊戲失敗: {str(e)}'
        }), 500


@app.route('/api/make_move', methods=['POST'])
def make_move():
    """進行移動"""
    try:
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')
        value = data.get('value')
        
        if row is None or col is None or value is None:
            return jsonify({
                'success': False,
                'message': '缺少必要參數'
            }), 400
        
        result = game.make_move(int(row), int(col), int(value))
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'移動失敗: {str(e)}'
        }), 500


@app.route('/api/clear_cell', methods=['POST'])
def clear_cell():
    """清除格子"""
    try:
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')
        
        if row is None or col is None:
            return jsonify({
                'success': False,
                'message': '缺少必要參數'
            }), 400
        
        result = game.clear_cell(int(row), int(col))
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'清除失敗: {str(e)}'
        }), 500


@app.route('/api/get_hint', methods=['POST'])
def get_hint():
    """獲取提示"""
    try:
        result = game.get_hint()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取提示失敗: {str(e)}'
        }), 500


@app.route('/api/reset_game', methods=['POST'])
def reset_game():
    """重置遊戲"""
    try:
        result = game.reset_game()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'重置失敗: {str(e)}'
        }), 500


@app.route('/api/game_state', methods=['GET'])
def get_game_state():
    """獲取遊戲狀態"""
    try:
        state = game.get_game_state()
        return jsonify({
            'success': True,
            'data': state
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取狀態失敗: {str(e)}'
        }), 500


@app.route('/api/validate_board', methods=['POST'])
def validate_board():
    """驗證棋盤"""
    try:
        result = game.validate_board()
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'驗證失敗: {str(e)}'
        }), 500


@app.route('/api/difficulty_info', methods=['GET'])
def get_difficulty_info():
    """獲取難度信息"""
    try:
        info = SudokuGenerator.get_difficulty_info()
        return jsonify({
            'success': True,
            'data': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取難度信息失敗: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("🎮 數獨遊戲服務器啟動中...")
    print("📱 打開瀏覽器訪問: http://localhost:5001")
    print("🎯 開始享受數獨遊戲！")
    app.run(debug=True, host='0.0.0.0', port=5001)