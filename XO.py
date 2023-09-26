print('*' * 10, ' Игра Крестики-нолики ', '*' * 10)
print()

board = [[' ', '0', '1', '2'],
         ['0', '-', '-', '-'],
         ['1', '-', '-', '-'],
         ['2', '-', '-', '-']]
#Двумерная матрица для поля

def draw_board(board):
    print('-' * 17)
    for i in range(4):
        print('|', board[0][0 + i],
              '|', board[1][0 + i],
              '|', board[2][0 + i],
              '|', board[3][0 + i], '|')
        print('-' * 17)
    print()
#Отрисовываем поле

def take_input(player_token):
    valid = False
    while not valid:
        player_answer = list(input('Введите координаты клетки для ' + player_token + '?(например 01) '))
        #Запрашиваем от клиента координаты клетки для постановки знака
        try:
            player_answer = list(map(int, player_answer))
        except:
            print('Некорректный ввод. Вы уверены, что ввели числа?')
            continue
        #Проверяем что клиент закинул нам цифры
        i, j = player_answer[0], player_answer[1]
        if i >= 0 and i <= 2 and j >= 0 and j <= 2:
            if str(board[j + 1][i + 1]) not in 'XO':
                board[j + 1][i + 1] = player_token
                valid = True
            else:
                print('Эта клетка уже занята!')
        #Проверяем и подставляем знак в board
        else:
            print('Некорректный ввод. Введите координаты клетки, например - 01.')
#Процесс игры

def check_win(board):
    for row in range(1, 4):
        if board[row][1] == board[row][2] == board[row][3] and board[row][1] != '-':
            return board[row][1]
    for col in range(1, 4):
        if board[1][col] == board[2][col] == board[3][col] and board[1] != '-':
            return board[1][col]
    if board[1][1] == board[2][2] == board[3][3] and board[1][1] != '-':
        return board[1][1]
    if board[1][3] == board[2][2] == board[3][1] and board[1][3] != '-':
        return board[1][3]
    return None
#Проверка выигрыша

def main(board):
    counter = 0
    win = False
    while not win:
        draw_board(board)
        if counter % 2 == 0:
            take_input('X')
        else:
            take_input('O')
        counter += 1
        if counter > 4:
            tmp = check_win(board)
            if tmp:
                print(tmp, 'выиграл!')
                win = True
                break
        if counter == 9:
            print('Ничья!')
            break
    draw_board(board)
#Сама игра
main(board)

input('Нажмите Enter для выхода!')