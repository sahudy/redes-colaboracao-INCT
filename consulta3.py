[
    {
        '$match': {
            '_id': {
                '$in': [
                    '0038936541518854', '0309287112277751', '0391758954520783', '0422652925722673', '0461451015026948', '0616238673458322', '0677617028146410', '0769819544839146', '0920196032137472', '0987355219242506', '1413071683140519', '1624091546521389', '1705430650855494', '1957942090126269', '2870655742911951', '2896049826673626', '3486202914688351', '3532058764024942', '3687551763124327', '4579286987089372', '4706525645223041', '4746829076971556', '4990968421738051', '5119417295487126', '5185829124608696', '5212303626376503', '5236549058240153', '5321313558714462', '5333709865535244', '5444380855577045', '5449448657729439', '5839043594908917', '6446047463034654', '6652079760634274', '6743301470746932', '6847311664433673', '6881990637613409', '6923877786371495', '7020467292690112', '7287108960864123', '7570230588831120', '7670383899259509', '7952918513827867', '8251270609012225', '8498467320034486', '8516223928904348', '8528111459865939', '9170893104155674', '9403804691367376', '9542083518570573', '9632409046763256', '9754332336954137', '9933650905615452'
                ]
            }
        }
    }, {
        '$unwind': '$listaPB'
    }, {
        '$match': {
            'listaPB.doi': {
                '$nin': [
                    None, ''
                ]
            }, 
            'listaPB.ano': {
                '$ne': None
            }
        }
    }, {
        '$set': {
            'local_epoca': {
                '$first': {
                    '$filter': {
                        'input': {
                            '$ifNull': [
                                '$locais_georreferenciamento', []
                            ]
                        }, 
                        'as': 'l', 
                        'cond': {
                            '$and': [
                                {
                                    '$ne': [
                                        '$$l.ano_inicio', None
                                    ]
                                }, {
                                    '$lte': [
                                        '$$l.ano_inicio', '$listaPB.ano'
                                    ]
                                }, {
                                    '$or': [
                                        {
                                            '$eq': [
                                                '$$l.ano_fim', 'Atual'
                                            ]
                                        }, {
                                            '$gte': [
                                                '$$l.ano_fim', '$listaPB.ano'
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }
    }, {
        '$set': {
            'regiao': {
                '$switch': {
                    'branches': [
                        {
                            'case': {
                                '$eq': [
                                    {
                                        '$type': '$local_epoca'
                                    }, 'missing'
                                ]
                            }, 
                            'then': 'Desconhecido'
                        }, {
                            'case': {
                                '$ne': [
                                    '$local_epoca.pais', 'Brasil'
                                ]
                            }, 
                            'then': 'Exterior'
                        }, {
                            'case': {
                                '$in': [
                                    '$local_epoca.estado', [
                                        'SP', 'RJ', 'MG', 'ES'
                                    ]
                                ]
                            }, 
                            'then': 'Sudeste'
                        }, {
                            'case': {
                                '$in': [
                                    '$local_epoca.estado', [
                                        'PR', 'SC', 'RS'
                                    ]
                                ]
                            }, 
                            'then': 'Sul'
                        }, {
                            'case': {
                                '$in': [
                                    '$local_epoca.estado', [
                                        'DF', 'GO', 'MT', 'MS'
                                    ]
                                ]
                            }, 
                            'then': 'Centro-Oeste'
                        }, {
                            'case': {
                                '$in': [
                                    '$local_epoca.estado', [
                                        'BA', 'PE', 'CE', 'PB', 'RN', 'AL', 'SE', 'PI', 'MA'
                                    ]
                                ]
                            }, 
                            'then': 'Nordeste'
                        }, {
                            'case': {
                                '$in': [
                                    '$local_epoca.estado', [
                                        'AM', 'PA', 'AC', 'RO', 'RR', 'AP', 'TO'
                                    ]
                                ]
                            }, 
                            'then': 'Norte'
                        }
                    ], 
                    'default': 'Desconhecido'
                }
            }
        }
    }, {
        '$set': {
            'uf': {
                '$switch': {
                    'branches': [
                        {
                            'case': {
                                '$eq': [
                                    '$regiao', 'Desconhecido'
                                ]
                            }, 
                            'then': '?'
                        }, {
                            'case': {
                                '$eq': [
                                    '$regiao', 'Exterior'
                                ]
                            }, 
                            'then': {
                                '$ifNull': [
                                    '$local_epoca.pais', '?'
                                ]
                            }
                        }
                    ], 
                    'default': '$local_epoca.estado'
                }
            }
        }
    }, {
        '$group': {
            '_id': {
                'doi': '$listaPB.doi', 
                'id': '$_id'
            }, 
            'nome': {
                '$first': '$nome_completo'
            }, 
            'regiao': {
                '$first': '$regiao'
            }, 
            'uf': {
                '$first': '$uf'
            }
        }
    }, {
        '$group': {
            '_id': '$_id.doi', 
            'pesquisadores': {
                '$push': {
                    'id': '$_id.id', 
                    'nome': '$nome', 
                    'regiao': '$regiao', 
                    'uf': '$uf'
                }
            }
        }
    }, {
        '$match': {
            'pesquisadores.1': {
                '$exists': True
            }
        }
    }, {
        '$set': {
            'tipo': {
                '$switch': {
                    'branches': [
                        {
                            'case': {
                                '$in': [
                                    'Desconhecido', '$pesquisadores.regiao'
                                ]
                            }, 
                            'then': 'indeterminado'
                        }, {
                            'case': {
                                '$in': [
                                    'Exterior', '$pesquisadores.regiao'
                                ]
                            }, 
                            'then': 'internacional'
                        }, {
                            'case': {
                                '$gt': [
                                    {
                                        '$size': {
                                            '$setUnion': [
                                                '$pesquisadores.regiao'
                                            ]
                                        }
                                    }, 1
                                ]
                            }, 
                            'then': 'inter-regional'
                        }, {
                            'case': {
                                '$gt': [
                                    {
                                        '$size': {
                                            '$setUnion': [
                                                '$pesquisadores.uf'
                                            ]
                                        }
                                    }, 1
                                ]
                            }, 
                            'then': 'interestadual'
                        }
                    ], 
                    'default': 'intraestadual'
                }
            }, 
            'pares': {
                '$reduce': {
                    'input': {
                        '$range': [
                            0, {
                                '$size': '$pesquisadores'
                            }
                        ]
                    }, 
                    'initialValue': [], 
                    'in': {
                        '$concatArrays': [
                            '$$value', {
                                '$map': {
                                    'input': {
                                        '$range': [
                                            {
                                                '$add': [
                                                    '$$this', 1
                                                ]
                                            }, {
                                                '$size': '$pesquisadores'
                                            }
                                        ]
                                    }, 
                                    'as': 'j', 
                                    'in': {
                                        'a': {
                                            '$arrayElemAt': [
                                                '$pesquisadores', '$$this'
                                            ]
                                        }, 
                                        'b': {
                                            '$arrayElemAt': [
                                                '$pesquisadores', '$$j'
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }, {
        '$facet': {
            'por_tipo': [
                {
                    '$group': {
                        '_id': '$tipo', 
                        'total': {
                            '$sum': 1
                        }, 
                        'dois': {
                            '$push': '$_id'
                        }
                    }
                }, {
                    '$sort': {
                        'total': -1
                    }
                }
            ], 
            'matriz_regioes': [
                {
                    '$unwind': '$pares'
                }, {
                    '$group': {
                        '_id': {
                            'regiao_a': {
                                '$min': [
                                    '$pares.a.regiao', '$pares.b.regiao'
                                ]
                            }, 
                            'regiao_b': {
                                '$max': [
                                    '$pares.a.regiao', '$pares.b.regiao'
                                ]
                            }
                        }, 
                        'colaboracoes': {
                            '$sum': 1
                        }
                    }
                }, {
                    '$sort': {
                        'colaboracoes': -1
                    }
                }
            ], 
            'matriz_estados': [
                {
                    '$unwind': '$pares'
                }, {
                    '$group': {
                        '_id': {
                            'uf_a': {
                                '$min': [
                                    '$pares.a.uf', '$pares.b.uf'
                                ]
                            }, 
                            'uf_b': {
                                '$max': [
                                    '$pares.a.uf', '$pares.b.uf'
                                ]
                            }
                        }, 
                        'colaboracoes': {
                            '$sum': 1
                        }, 
                        'dois': {
                            '$addToSet': '$_id'
                        }, 
                        'pesquisadores': {
                            '$addToSet': {
                                '$concatArrays': [
                                    [
                                        '$pares.a.nome'
                                    ], [
                                        '$pares.b.nome'
                                    ]
                                ]
                            }
                        }
                    }
                }, {
                    '$set': {
                        'tipo': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$_id.uf_a', '$_id.uf_b'
                                    ]
                                }, 'intraestadual', 'interestadual'
                            ]
                        }
                    }
                }, {
                    '$sort': {
                        'colaboracoes': -1
                    }
                }
            ]
        }
    }
]