def save_condition(id_list,wait_list,path,type):
    str = ""
    if type == 'Easy':
        str += '0,'
    elif type == 'Normal':
        str += '1,'
    elif type == "Hard":
        str += '2,'
    for i in id_list:
        str += f"{i[0]}"
        str += f",{i[1]},"

    for i in wait_list:
        str += f"{i[0]}"
        str += f",{i[1]},"

    with open(path,"w",encoding = "utf-8") as f:
        f.write(str)
