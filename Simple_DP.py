def Simple_DP(w,T):
    #変数定義・初期化
    n = len(w)
    W = sum(w)ｓ
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

    #インデックスを元に最適解を求める
    x = [0 for i in range(n)]
    searchIDX = ansIDX
    for i in reversed(range(0,n)):
        if(DP_LIST[searchIDX][i-1]) == 0:
            x[i] = 1
            searchIDX -= w[i]
    #最適解xを出力
    return x

    #debug 
    # for j in range(num_rows):
    #     for i in range(num_columns):
    #         print(DP_LIST[j][i],end ='')
    #         if(i != num_columns-1):
    #             print(" ",end ='')
    #     print(" \n")
            
w = [3,7,5,8,2] #重さリスト
T = 9 #目的重量
x = Simple_DP(w,T)
print(x)