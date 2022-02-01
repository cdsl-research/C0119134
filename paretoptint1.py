import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
def plot_pareto_front(f1, f2):
    """
    パレートフロントを描画する

    引数
     f1: 評価関数1の値（type:numpy.ndarray, shape:1xN）
     f2: 評価関数2の値（type:numpy.ndarray, shape:1xN）
    """

    '''パレートフロントの抽出'''
    # データをN×2行列に
    f1 = f1.reshape(-1,1)
    f2 = f2.reshape(-1,1)
    f  = np.hstack((f1,f2))

    # f1を基準に昇順ソート
    f_sorted_by_f1 = f[np.argsort(f[:,0])]
    # f2が小さいペアをパレートフロントに順次追加
    pareto_front = [f_sorted_by_f1[0]]
    for pair in f_sorted_by_f1[1:]:
        print(pair)
        if pair[1] <= pareto_front[-1][1]:
            pareto_front = np.vstack((pareto_front,pair))
    pareto_front = np.array(pareto_front)

    '''パレートフロントの折れ線作成'''
    pareto_zigzag = pareto_front[0]
    for idx in range(pareto_front.shape[0]-1):
        via_point = np.array([pareto_front[idx+1,0],pareto_front[idx,1]])
        pareto_zigzag = np.vstack((pareto_zigzag,via_point))
        pareto_zigzag = np.vstack((pareto_zigzag,pareto_front[idx+1]))

    f2_max_point  = np.array([pareto_front[0,0],max(f[:,1])])
    f1_max_point  = np.array([max(f[:,0]),pareto_front[-1,1]])

    pareto_zigzag = np.vstack((f2_max_point,pareto_zigzag))
    pareto_zigzag = np.vstack((pareto_zigzag,f1_max_point))

    '''プロット'''
    fig = plt.figure(figsize=(6, 6))
    res = fig.add_subplot(111, xlabel="response time", ylabel="used memory")
    res.scatter(f1,f2)
    res.plot(pareto_front[:,0],pareto_front[:,1],'or')
    res.plot(pareto_zigzag[:,0],pareto_zigzag[:,1],'r')
    res.grid(axis='x')
    res.grid(axis='y')
    fig.savefig("kd_pareto_front")
    return pareto_front, pareto_zigzag, f

def logmem(name, label):
    #logファイルの読み込み
    mem_avr = []
    for num in label:
        print("log:",num)
        with open(f"{name}/log{num}.txt", "r", encoding="utf-8") as f:
            x = f.readlines()
        log_list = []
        for k in range(len(x)):
            if "root" in x[k]:
                log_list.append(k)
        for j in reversed(log_list):
            x.pop(j)
        memplit = []
        for i in x:
            memplit.append(i.split())
        mem = []
        for i in memplit:
            mem.append(int(i[5]))
        mem = np.array(mem)
        mem_avr.append(np.average(mem))
    return mem_avr

def csvres(name, label):
    #csvファイルの読み込み
    res_avr = []
    for num in label:
        print("example:",num)
        df = pd.read_csv(f"{name}/example{num}_stats.csv")
        res_avr.append(df["Average Response Time"][0])
    return res_avr

def senkei(f_1, f_2):
    #近似直線
    sen = np.polyfit(f_1, f_2, 1)
    func = np.poly1d(sen)
    return func


def plot(mem_avr, res_avr, label):
    res_avr_list = [res_avr, label]
    mem_avr_list = [mem_avr, label]
    #Numpyで配列にする
    mem_avr_list = np.array(mem_avr_list)
    res_avr_list = np.array(res_avr_list)
    func = senkei(res_avr_list[1], res_avr_list[0])
    y1 = func(res_avr_list[1])
    func = senkei(mem_avr_list[1], mem_avr_list[0])
    y2 = func(mem_avr_list[1])
    #図の作成
    fig1 = plt.figure(figsize=(5.0, 5.0))
    fig2 = plt.figure(figsize=(5.0, 5.0))
    #図の形を指定
    axy = fig1.add_subplot(111, xlim=(0, 110), xlabel="keepalive_timeout", ylabel="used memory")
    res = fig2.add_subplot(111, xlim=(0, 110), xlabel="keepalive_timeout", ylabel="response time")
    axy.grid(axis='x')
    axy.grid(axis='y')
    res.grid(axis='x')
    res.grid(axis='y')
    #scatterの部分を変更すると他のグラフができる調べて
    axy.scatter(mem_avr_list[1],mem_avr_list[0], c="blue")
    res.scatter(res_avr_list[1],res_avr_list[0], c="red")
    res.plot(res_avr_list[1], y1)
    axy.plot(mem_avr_list[1], y2)
    fig1.savefig("kd_mem")
    fig2.savefig("kd_res")

def x1(mem_avr, res_avr, label, tf):
    plot(mem_avr, res_avr, label)
    a, b, f = plot_pareto_front(mem_avr, res_avr)
    #take keep alive time out at pareto front
    if tf:
        paretofront = []
        for i in a:
            paretofront.append((np.where(f==i)[0][0]+1)*5)
        print(paretofront)
        np.savetxt("paretofront.txt",paretofront, fmt='%d')

def x2(kkl2_avr_list, kkc2_avr_list, label2):
    lis = []
    print(type(label2), label2)
    c=0
    for i in label2:
        lis.append(kkl2_avr_list[c]+kkc2_avr_list[c])
        c += 1
    return (lis.index(np.amin(lis))+1)*5



def main():
    fech = None
    label1 = [5, 10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    kkl1_mem_avr = logmem("kkl1", label1)
    kkc1_res_avr = csvres("kkc1", label1)
    #get pareto front list
    kkl1_mem_avr = np.array(kkl1_mem_avr)
    kkc1_res_avr = np.array(kkc1_res_avr)
    try:
        with open("paretofront.txt", "r", encoding="utf-8") as f:
            label2 = f.read().split()
        print(label2)
        tf = False
        kkl2_mem_avr = logmem("kkl2", label2)
        kkc2_res_avr = csvres("kkc2", label2)
        kkl2_mem_avr = np.array(kkl2_mem_avr)
        kkc2_res_avr = np.array(kkc2_res_avr)
        fech = x2(kkl2_mem_avr, kkc2_res_avr, label2)
        print(fech)
        with open("paretofront.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{fech}")
    except Exception as e:
        print(e)
        tf = True
        x1(kkl1_mem_avr, kkc1_res_avr, label1, tf)


if __name__ == "__main__":
    main()
