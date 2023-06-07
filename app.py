from flask import Flask, render_template, request

app = Flask(__name__)

# 定義初始狀態
initial_board = [['', '', ''], ['', '', ''], ['', '', '']]#初始的遊戲棋盤
current_player = 'X' #玩家 'X' 先下
winner = None #檢測是否有贏家
game_over = False #檢測遊戲是否結束
board = initial_board.copy() #用於存儲目前的棋盤狀態(不會影響初始棋盤)

score1=0
score2=0

#變數傳遞給模板
@app.route('/')
def index():
    
    return render_template('index.html', board=board, current_player=current_player, winner=winner, game_over=game_over,score1=score1,score2=score2)

@app.route('/play', methods=['POST']) #指定了路徑 /play 的處理函式，並限定了該處理函式只能處理 POST 請求。
def play():
    global board, current_player, winner, game_over,score1,score2
    
    row = int(request.form['row'])
    col = int(request.form['col'])
    
    # 檢查該位置是否已經有棋子
    if board[row][col] == '':#檢查位置是否為空

        board[row][col] = current_player #將當前位置設為玩家符號

        # 切換玩家
        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'

        # 檢查遊戲結束條件
        if check_winner():
            winner = current_player
            if winner=='X':
                score1+=1
            elif winner=='O':
                score2+=1
            game_over = True
        elif check_board_full():
            game_over = True

      #返回更新後的遊戲狀態到前端
    return render_template('index.html', board=board, current_player=current_player, winner=winner, game_over=game_over,score1=score1,score2=score2)
@app.route('/next', methods=['POST'])
def next():
    global board, current_player, winner, game_over
    
    
    board = initial_board.copy() #將initial_board(初始棋盤)複製到board中
    current_player = 'X'
    winner = None
    game_over = False
   
    
    return render_template('index.html', board=board, current_player=current_player, winner=winner, game_over=game_over,score1=score1,score2=score2)
@app.route('/restart', methods=['POST'])
# 重設遊戲狀態
def restart():
    global board, current_player, winner, game_over,score1,score2
    
    
    board = initial_board.copy() #將initial_board(初始棋盤)複製到board中
    current_player = 'X'
    winner = None
    game_over = False
    score1=0
    score2=0
    
    return render_template('index.html', board=board, current_player=current_player, winner=winner, game_over=game_over,score1=score1,score2=score2)


#檢查遊戲是否有玩家獲勝
def check_winner():
    # 檢查行
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return True

    # 檢查列
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return True

    # 檢查對角線
    if board[0][0] == board[1][1] == board[2][2] != '':
        return True
    if board[0][2] == board[1][1] == board[2][0] != '':
        return True

    return False

#檢查棋盤是否已滿
def check_board_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                return False
    return True


if __name__ == '__main__':
    app.run(debug=True)#顯示詳細的錯誤訊息
