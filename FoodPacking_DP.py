import random
import time

def Simple_DP(w,T):
    #変数定義・初期化
    n = len(w)
    W = sum(w)
    w_max = max(w)

    #行列数設定
    # num_rows = T + w_max
    num_columns = n
    num_rows = min(T + w_max - 1,W) #計算範囲の短縮(Lexico_FDP)

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
    num_rows = min(T + w_max - 1,W) #計算範囲の短縮(Lexico_FDP)
    
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
    return x

def FoodPacking(repete_times,n,T,rand_min_w,rand_max_w):
    #袋付め回数ごとに変化する変数
    w = [random.randint(rand_min_w,rand_max_w) for i in range(n)]
    priority = [0 for i in range(n)]
    I = list(range(n))

    #評価用パラメータ記憶変数
    Item_num = n
    Item_weight = [w[i] for i in range(n)]
    Item_remain_times =[0 for i in range(n)]
    f = [] #f[i]: i回目の最適解の合計重量
    Match_cnt = 0

    start = time.time()
    for N in range(repete_times):
        #最適解を求める
        x = Lexico_DP(w,priority,T)
        #アイテムの追加・残留によるパラメータ更新
        opt_weight = 0
        for i in range(n):
            if x[i] == 1: 
                opt_weight += w[i]
                #品が選ばれたので新しく追加する
                Item_num += 1
                I[i] = Item_num - 1 #index番号の形式上-1
                #重さをランダムに決定
                Item_weight.append(random.randint(rand_min_w,rand_max_w))
                w[i] = Item_weight[I[i]]
                #残留回数のリストの枠を増やす
                Item_remain_times.append(0)
            else:
                Item_remain_times[I[i]] += 1
                priority[i] = Item_remain_times[I[i]]
        f.append(opt_weight)
        if opt_weight == T:
            Match_cnt += 1

    elapsed_time = time.time() - start
    
    Match_rate = Match_cnt / repete_times #最適解の合計重量 = Tだった割合
    f_mean = sum(f)/len(f) #合計重量平均
    ave_rememain = sum(Item_remain_times)/len(Item_remain_times) #平均残留回数
    max_remain = max(Item_remain_times) #最大残留回数
    
    print("-条件-")
    print("ホッパ数: "+str(n))
    print("目的重量: "+str(T))
    print("袋詰め回数: "+str(repete_times))
    print("重量範囲: "+str(rand_min_w)+" ~ "+str(rand_max_w))

    print("\n-結果-")
    print("合計重量平均: "+str(f_mean))
    print("最大残留回数: "+str(max_remain))
    print("平均残留回数: "+str(ave_rememain))
    print("最適解の重量=目的重量だった割合: "+str(Match_rate))
    print("実行時間: "+str(elapsed_time))

    #表作成(あまり重要な処理じゃないです)
    # blank_I = len(str(max(I))) + 4
    # blank_w = len(str(max(Item_weight))) + 4
    # blank_r = len(str(max(Item_remain_times))) + 4
    # print("N"+" "*(blank_I-1)+"w"+" "*(blank_w-1)+"C"+" "*(blank_r-1))
    # for i in range(Item_num):
    #     print(str(i)+" "*(blank_I-len(str(i)))+str(Item_weight[i])+" "*(blank_w-len(str(Item_weight[i])))+str(Item_remain_times[i])+" "*(blank_r-len(str(Item_remain_times[i]))))

if __name__ == '__main__':
    repete_times = 10000
    n = 10
    T = 180 
    rand_min_w = 35
    rand_max_w = 55
    FoodPacking(repete_times,n,T,rand_min_w,rand_max_w)


    w = [3,7,5,8,2] #重さリスト
    priority = [5,5,1,1,3] #優先度リスト
    T = 9 #目的重量

    # Simple_FDP_result = Simple_DP(w,T)
    # print(Simple_FDP_result)
    # Lexico_FDP_result = Lexico_DP(w,priority,T)
    # print(Lexico_FDP_result)