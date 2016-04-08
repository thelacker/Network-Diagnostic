import pickle

def get_constructions():
    with open('data.pickle', 'rb') as f:
        constructions = pickle.load(f)
    return constructions
