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
        '$group': {
            '_id': {
                'regiao': '$regiao', 
                'pais': '$local_epoca.pais', 
                'estado': '$local_epoca.estado'
            }, 
            'artigos': {
                '$sum': 1
            }, 
            'pesquisadores': {
                '$addToSet': '$nome_completo'
            }
        }
    }, {
        '$group': {
            '_id': None, 
            'total_geral': {
                '$sum': '$artigos'
            }, 
            'grupos': {
                '$push': '$$ROOT'
            }
        }
    }, {
        '$unwind': '$grupos'
    }, {
        '$replaceWith': {
            '$mergeObjects': [
                '$grupos', {
                    'total_geral': '$total_geral'
                }
            ]
        }
    }, {
        '$set': {
            'percentual': {
                '$round': [
                    {
                        '$multiply': [
                            {
                                '$divide': [
                                    '$artigos', '$total_geral'
                                ]
                            }, 100
                        ]
                    }, 2
                ]
            }, 
            'qtd_pesquisadores': {
                '$size': '$pesquisadores'
            }
        }
    }, {
        '$sort': {
            'artigos': -1
        }
    }
]