import pickle

def ip_dict_write(ip, status):
    ip_dict = {}
    with open('ip_dict.txt', 'rb') as f:
        try:
            ip_dict = pickle.load(f)
        except:
            pass
    if status == 0:
        ip_dict[ip] = 0
    elif status == 1:
        ip_dict[ip] = 1
    elif status == 2:
        ip_dict[ip] = 2
    else:
        ip_dict[ip] = 3
    with open('ip_dict.txt', 'wb') as f:
        pickle.dump(ip_dict, f)


def ip_dict_read(ip = None):
    ip_dict = {}
    with open('ip_dict.txt', 'rb') as f:
        try:
            ip_dict = pickle.load(f)
        except:
            pass
    if ip == None:
        return ip_dict
    else:
        try:
            if ip_dict[ip]:
                return ip_dict[ip]
            else:
                return 0
        except:
            return 0