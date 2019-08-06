import datetime


LSH_CONFIG = {
    'num_permutation': 192,
    'b': 50,
    'r': 2,
    'storage_config':{
        'type': 'redis',
        'redis': {'host': 'localhost', 'port': 6379}
   },
    'similarity_threshold': 0.25
}

MINHASH_CONFIG = {
    'num_permutation': LSH_CONFIG['num_permutation'],
    'seed': datetime.datetime.now().microsecond
}

SHINGLE_CONFIG = {
    'k': 1
}