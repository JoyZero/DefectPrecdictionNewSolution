from functools import cmp_to_key
import os


SIM_EUCL = "eucidean"
SIM_COS = "cos"


def read_tera_all_csv(dirpath):
    file_list = []
    files = os.listdir(dirpath)
    for file in files:
        filepath = dirpath + '/' + file
        if os.path.isfile(filepath) and file.endswith('.csv'):
            file_list.append(filepath)
    file_list.sort(key=cmp_to_key(compare_str_tera))
    return file_list


def compare_str_tera(str1, str2):
    tag1 = str1.split('-')[1][:-4]
    tag2 = str2.split('-')[1][:-4]
    parts1 = tag1.split('.')
    parts2 = tag2.split('.')
    index = 0
    while index < parts1.__len__() and index < parts2.__len__():
        if not parts1[index].isdigit():
            return -1
        elif not parts2[index].isdigit():
            return 1
        diff = int(parts1[index]) - int(parts2[index])
        if not diff == 0:
            return diff
        index += 1
    return parts1.__len__() - parts2.__len__()


def read_metric_all_csv(dirpath):
    file_list = []
    files = os.listdir(dirpath)
    for file in files:
        filepath = dirpath + file
        if os.path.isfile(filepath) and file.endswith('.csv'):
            file_list.append(filepath)
    file_list.sort(key=cmp_to_key(compare_str_metrics))
    return file_list


def compare_str_metrics(str1, str2):
    tag1 = str1.split('_')[3][:-4]
    tag2 = str2.split('_')[3][:-4]
    parts1 = tag1.split('.')
    parts2 = tag2.split('.')
    index = 0
    while index < parts1.__len__() and index < parts2.__len__():
        if not parts1[index].isdigit():
            return -1
        elif not parts2[index].isdigit():
            return 1
        diff = int(parts1[index]) - int(parts2[index])
        if not diff == 0:
            return diff
        index += 1
    return parts1.__len__() - parts2.__len__()


def get_l_path(filename, sim_type, target=False):
    parts = filename.split('/')
    suffix = parts[parts.__len__()-1]
    pre = filename[0:-suffix.__len__()]
    folder = ""
    if sim_type == SIM_EUCL:
        folder = "L/"
    elif sim_type == SIM_COS:
        folder = "L1/"
    if target:
        suffix = suffix[:-4] + "-L-exist.txt"
    else:
        suffix = suffix[:-4] + "-L.txt"
    res = pre + folder + suffix
    return res


def get_exist_path(filename):
    parts = filename.split('/')
    suffix = parts[parts.__len__() -1 ]
    pre = filename[:-suffix.__len__()]
    suffix = suffix[:-4] + '-exist.csv'
    return pre + 'splited/' + suffix


def get_y_path(filename):
    parts = filename.split('/')
    suffix = parts[parts.__len__() - 1]
    pre = filename[0:-suffix.__len__()]
    folder = "y/"
    suffix = suffix[:-4] + "-y.txt"
    res = pre + folder + suffix
    return res


def get_i_path(file1, file2):
    tag1 = file1[:-4].split('-')[1]
    tag2 = file2[:-4].split('-')[1]
    parts1 = file1.split('/')
    suffix1 = parts1[parts1.__len__()-1]
    pre = file1[:-suffix1.__len__()]
    name = suffix1.split('-')[0]
    res = pre + 'I/' + name + '_' +  tag1 + '_' + tag2 + '.txt'
    return res


def get_allfile_path(dir, name):
    return dir + name + '/' + name + '-allFileIndex.txt'


def get_result_fpath(dir, name):
    return dir + name +'/' + name + '-f.txt'


def get_result_wpath(dir, name):
    return dir + name + '/' + name + '-w.txt'


def get_existfile_path(filename):
    parts = filename.split('/')
    suffix = parts[parts.__len__() - 1]
    pre = filename[0:-suffix.__len__()]
    folder = "splited/"
    suffix = suffix[:-4] + "-exist.csv"
    return pre + folder + suffix


def get_evalution_result_path(dir, name):
    filepath = dir + name + '/' + name + '-eval_res.txt'
    return filepath


def write_file(filename, content):
    with open(filename, 'w') as f:
        f.writelines(content)


def write_eval_result(dir, name, params_list, eval_res_list):
    content = []
    index = 0
    while index < params_list.__len__():
        params = params_list[index]
        param_str = str(params[0]) + ',' + str(params[1]) + ',' + str(params[2])
        eval_res = eval_res_list[index]
        eval_str = str(eval_res[0]) + ',' + str(eval_res[1]) + ',' + str(params[3])
        content.append(param_str + ' : ' + eval_str)
        index += 1
    file_path = get_evalution_result_path(dir, name)
    write_file(file_path, content)




if __name__ == '__main__':
    dir1 = 'C:/Users/1/Desktop/tera/xerces/xerces-1.2.csv'
    dir2 = 'C:/Users/1/Desktop/tera/xerces/xerces-1.3.csv'
    print(get_i_path(dir1, dir2))
    # testStr = 'add/1.2.3.csv'
    # tag = testStr.split('/')[1][:-4]
    # parts = tag.split('.')
    # print(parts)
