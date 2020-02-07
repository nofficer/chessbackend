def conv_nums_to_fen(item):
    bf = []
    for num in item:
        if num == 4:
            bf.append('r')
        elif num == 2:
            bf.append('n')
        elif num == 3:
            bf.append('b')
        elif num == 5:
            bf.append('q')
        elif num == 6:
            bf.append('k')
        elif num == 1:
            bf.append('p')
        elif num == 0:
            bf.append(1)
        elif num == 7:
            bf.append('P')
        elif num == 10:
            bf.append('R')
        elif num == 8:
            bf.append("N")
        elif num == 9:
            bf.append("B")
        elif num ==11:
            bf.append("Q")
        elif num == 12:
            bf.append('K')
    return bf


def insert_slash(bf):
    count = -1
    start_at = -1
    for item in bf:
        count+= 1
        start_at += 1
        bfin = bf.index(item, start_at)
        if count == 8:
            bf.insert(bfin,"/")
            count = -1
        else:
            None
    return bf

def agg_blank(bf):
    newbf = ''
    counter = 0
    for item in bf:
        if item == 1:
            counter +=1
        elif item != 1:
            if counter != 0:
                newbf = newbf + str(counter)
                counter = 0
                newbf = newbf + item
            else:
                newbf = newbf + item
    if counter != 0:
        return(newbf+str(counter))
    else:
        return (newbf)


arr = [4, 2, 3, 0, 6, 3, 2, 4, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 5, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 9, 7, 8, 0, 10, 7, 7, 7, 7, 0, 7, 7, 0, 10, 8, 9, 11, 12, 0, 0, 0]
arr2 = [4, 2, 3, 0, 6, 3, 2, 4, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 5, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 9, 7, 8, 0, 10, 7, 7, 7, 7, 0, 7, 7, 0, 10, 8, 9, 11, 12, 11, 11, 11]


beforeagg =  insert_slash(conv_nums_to_fen(arr))
boardfen_converted = agg_blank(insert_slash(conv_nums_to_fen(arr)))
print(boardfen_converted)
print(beforeagg)
beforeagg2 =  insert_slash(conv_nums_to_fen(arr2))
boardfen_converted2 = agg_blank(insert_slash(conv_nums_to_fen(arr2)))
print(boardfen_converted2)
print(beforeagg2)
