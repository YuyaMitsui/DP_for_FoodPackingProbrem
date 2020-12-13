def Simple_DP(w,T):
    #変数定義・初期化
    n = len(w)
    W = sum(w)
    w_max = max(w)

    #行列数設定
    num_rows = T + w_max
    num_columns = n

    #DPを行う二次元配列初期化
    DP_LIST = [[0 for i in range(num_columns)] for j in range(num_rows)]
    DP_LIST[0] = [1] * num_columns

    #DP実行部
    for k in range(num_columns):
        for p in range(1,num_rows):
            if k == 0 and p == w[0]:
                DP_LIST[p][0] = 1
            elif DP_LIST[p][k-1] == 1 or (p - w[k] >= 0 and DP_LIST[p-w[k]][k-1] == 1):
                DP_LIST[p][k] = 1

    #最適解のインデックスを探す
    ansIDX = 0
    for i in range(T,num_rows):
        if DP_LIST[i][num_columns-1] == 1: #最終列の目的重量を満たす解を見つける
            ansIDX = i
            break

    #バックトラック
    x = [0 for i in range(n)]
    searchIDX = ansIDX
    for i in reversed(range(0,n)):
        if(DP_LIST[searchIDX][i-1]) == 0:
            x[i] = 1
            searchIDX -= w[i]

    #最適解xを出力
    return x

def Lexico_DP(w,priority,T):
    #変数定義・初期化
    n = len(w)
    W = sum(w)
    w_max = max(w)

    #行列数設定
    # num_rows = T + w_max
    num_columns = n
    num_rows = min(T + w_max - 1,W)
    #DPを行う二次元配列初期化
    #y:重さのDP表
    #z:優先度のDP表
    #u,v: 優先度を記憶する補助変数

    DP_LIST_y = [[0 for i in range(num_columns)] for j in range(num_rows)]
    DP_LIST_z = [[-1 for i in range(num_columns)] for j in range(num_rows)]
    priority_u = [[-1 for i in range(num_columns)] for j in range(num_rows)]
    priority_v = [[-1 for i in range(num_columns)] for j in range(num_rows)]

    DP_LIST_y[0] = [1] * num_columns
    DP_LIST_z[0] = [0] * num_columns

    #DP実行部
    for k in range(num_columns):
        for p in range(1,num_rows):
            if k == 0 and p == w[0]:
                DP_LIST_y[p][0] = 1
                priority_v[p][k] = priority[k]
            else:
                if DP_LIST_y[p][k-1] == 1:
                    DP_LIST_y[p][k] = 1
                    priority_u[p][k] = DP_LIST_z[p][k-1]
                if (p - w[k] >= 0 and DP_LIST_y[p-w[k]][k-1] == 1):
                    DP_LIST_y[p][k] = 1
                    priority_v[p][k] = DP_LIST_z[p-w[k]][k-1] + priority[k]
            if DP_LIST_y[p][k] == 1:
                DP_LIST_z[p][k] = max(priority_v[p][k],priority_u[p][k])

    #最適解のインデックスを探す
    ansIDX = 0
    for i in range(T,num_rows):
        if DP_LIST_y[i][num_columns-1] == 1: #最終列の目的重量を満たす解を見つける
            ansIDX = i
            break
    
    #バックトラック
    x = [0 for i in range(n)]
    searchIDX = ansIDX
    for i in reversed(range(0,n)):
        if searchIDX >= w[i]:    
            if priority_v[searchIDX][i] >= priority_u[searchIDX][i]:        
                x[i] = 1
                searchIDX -= w[i]
            else:
                x[i] = 0
    #debug 
    # for j in range(num_rows):
    #     for i in range(num_columns):
    #         print(DP_LIST_y[j][i],end ='')
    #         if(i != num_columns-1):
    #             print(" ",end ='')
    #     print(" \n")
        
    # for j in range(num_rows):
    #     for i in range(num_columns):
    #         print(DP_LIST_z[j][i],end ='')
    #         if(i != num_columns-1):
    #             print(" ",end ='')
    #     print(" \n")

    #最適解xを出力
    return x

#main
w = [3,7,5,8,2] #重さリスト
priority = [5,5,1,1,3] #優先度リスト
T = 9 #目的重量
# x = Simple_DP(w,T)
x = Lexico_DP(w,priority,T)
print(x)