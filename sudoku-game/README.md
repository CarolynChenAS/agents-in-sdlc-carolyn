# 數獨遊戲 (Sudoku Game)

一個功能完整的網頁版數獨遊戲，具有現代化的黑暗主題界面。

## 功能特色

- 🎯 多個難度等級（簡單、中等、困難）
- 🔍 智能提示系統
- ⏱️ 計時器功能
- 💡 輸入驗證和錯誤提示
- 🎨 美觀的響應式設計
- 🌙 黑暗主題界面
- 🎮 完整的遊戲控制（新遊戲、重置、清除）

## 技術棧

- **後端**: Python Flask
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **樣式**: 現代CSS Grid和Flexbox
- **測試**: Python unittest

## 快速開始

### 安裝依賴

```bash
cd sudoku-game
pip install -r requirements.txt
```

### 運行遊戲

```bash
python app.py
```

然後在瀏覽器中打開 `http://localhost:5001`

### 運行測試

```bash
python -m pytest tests/ -v
```

## 遊戲規則

數獨是一個邏輯益智遊戲：

1. 在9×9的網格中填入數字1-9
2. 每行必須包含1-9的所有數字，不能重複
3. 每列必須包含1-9的所有數字，不能重複  
4. 每個3×3的子網格必須包含1-9的所有數字，不能重複

## 項目結構

```
sudoku-game/
├── README.md              # 項目說明
├── requirements.txt       # Python依賴
├── app.py                # Flask主應用
├── src/                  # 核心邏輯
│   ├── sudoku_game.py    # 數獨遊戲類
│   ├── sudoku_generator.py # 數獨生成器
│   └── sudoku_solver.py  # 數獨求解器
├── tests/                # 測試文件
│   ├── test_sudoku_game.py
│   ├── test_generator.py
│   └── test_solver.py
├── templates/            # HTML模板
│   └── index.html
└── static/              # 靜態資源
    ├── css/
    │   └── style.css
    └── js/
        └── game.js
```

## 開發指南

### 添加新功能

1. 在 `src/` 目錄中添加核心邏輯
2. 在 `tests/` 目錄中添加對應測試
3. 在前端文件中添加UI交互
4. 更新此README文檔

### 代碼風格

- Python代碼遵循PEP 8標準
- 使用類型提示
- 編寫完整的文檔字符串
- 保持測試覆蓋率

## 許可證

MIT License