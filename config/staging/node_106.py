name = 'MSB319 "Environmentals"'
location = '319 Marine Sciences Building, UH Manoa'
note = ''
public_key = ''


conf = [
    {
        'dbtag':'ts',
        'dbtype':'DOUBLE NOT NULL',
        'description':'Time of sampling',
        'plot':True,
    },
    {
        'dbtag':'Ta',
        'unit':'Deg.C',
        'description':'Air temperature',
        'lb':5,
        'ub':40,
    },
]


if '__main__' == __name__:
    for c in conf:
        print('- - -')
        for k, v in c.items():
            print(k, ':', v)

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_', '-'))
