from mygene import MyGeneInfo


def get_uid(name):
    mg = MyGeneInfo()
    res = mg.query(name, scopes='symbol, alias',
                   fields='uniprot, symbol', species='human')
    symbol = []
    uid = []
    for hit in res['hits']:
        uid.append(hit['uniprot']['Swiss-Prot'])
        symbol.append(hit['symbol'])
    dict = {s:i for s,i in zip(symbol, uid)}
    try:
        uid = dict[name]
        out = uid
    except KeyError:
        out = dict
    return out

    


    