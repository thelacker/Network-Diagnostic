import pickle


def ip_dict_write(ip, status):
    ip_dict = {}
    with open('ip_dict.txt', 'rb') as f:
        try:
            ip_dict = pickle.load(f)
        except:
            pass
    ip_dict[ip] = status
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
                return [0, 0]
        except:
            return [0, 0]