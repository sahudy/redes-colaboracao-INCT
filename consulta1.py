[
    {
        '$unwind': '$listaPB'
    }, {
        '$match': {
            'listaPB.doi': {
                '$nin': [
                    None, ''
                ]
            }, 
            'listaPB.ano': {
                '$nin': [
                    None, ''
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$listaPB.doi', 
            'ano_publicacao': {
                '$first': '$listaPB.ano'
            }, 
            'autores': {
                '$addToSet': {
                    'id_lattes': '$_id', 
                    'nome': '$nome_completo'
                }
            }
        }
    }, {
        '$match': {
            'autores.1': {
                '$exists': True
            }
        }
    }, {
        '$set': {
            'autores': {
                '$sortArray': {
                    'input': '$autores', 
                    'sortBy': {
                        'id_lattes': 1
                    }
                }
            }
        }
    }, {
        '$group': {
            '_id': {
                'autores': '$autores', 
                'ano': '$ano_publicacao'
            }, 
            'total_colaboracoes_ano': {
                '$sum': 1
            }, 
            'lista_dois_comum': {
                '$addToSet': '$_id'
            }
        }
    }, {
        '$group': {
            '_id': '$_id.autores', 
            'total_colaboracoes_geral': {
                '$sum': '$total_colaboracoes_ano'
            }, 
            'colaboracoes_por_ano': {
                '$push': {
                    'ano': '$_id.ano', 
                    'total_neste_ano': '$total_colaboracoes_ano', 
                    'dois': '$lista_dois_comum'
                }
            }
        }
    }, {
        '$set': {
            'colaboracoes_por_ano': {
                '$sortArray': {
                    'input': '$colaboracoes_por_ano', 
                    'sortBy': {
                        'ano': -1
                    }
                }
            }
        }
    }, {
        '$sort': {
            'total_colaboracoes_geral': -1
        }
    }
]