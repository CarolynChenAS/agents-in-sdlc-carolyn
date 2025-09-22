#!/bin/bash

# 數獨遊戲啟動腳本
# Sudoku Game Start Script

echo "🎮 正在啟動數獨遊戲..."
echo "🎮 Starting Sudoku Game..."

# 檢查是否在正確的目錄
if [ ! -f "app.py" ]; then
    echo "❌ 錯誤：請在 sudoku-game 目錄中運行此腳本"
    echo "❌ Error: Please run this script from the sudoku-game directory"
    exit 1
fi

# 檢查Python是否可用
if ! command -v python &> /dev/null; then
    echo "❌ 錯誤：未找到Python"
    echo "❌ Error: Python not found"
    exit 1
fi

# 檢查Flask是否已安裝（嘗試導入）
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 安裝依賴..."
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ 錯誤：依賴安裝失敗"
        echo "❌ Error: Dependency installation failed"
        exit 1
    fi
fi

echo "🚀 啟動服務器..."
echo "🚀 Starting server..."
echo "📱 遊戲將在 http://localhost:5001 打開"
echo "📱 Game will be available at http://localhost:5001"
echo "⏹️  按 Ctrl+C 停止服務器"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# 啟動Flask應用
python app.py