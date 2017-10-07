name = '(TBD)'
location = '(TBD)'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCyQxlrza6fTfwH4W1HtFsyP8uXRk7g04l4sp/PQ1KgrX92zm8c9pEwGiarMKJAlBaCTl8cMJXlemPmMs4/2WUtkRlgmWfU+HLfw457atOEPgrkJOw8mUb7I26IeAZ8Tz68a3/s4snxE0KGbbvHBidwnjGOztvr3whEYgJJPB3RuB1WTkIreQeIILj0eomyw53PzjT++aleJhmReLyGBzBwetXi8BYwwutn/AfM2nZG4Xso6zvIBidGFaSCPmCWVtsfx1uGiEjxm6/3/Avo/TwXB3+BJ8DyiK8TkzuUBusu9zkR3oRs8llSqngLfLS/GqVd6oBXQuT2ANLqxwQnddIF nuc@base-009'


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
        'interval':60,
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
        'lb':5*60,
        'interval':60,
    },
    {
        'dbtag':'usedMB',
        'unit':'MB',
        'description':'Used disk space',
        'interval':60,
    },
    {
        'dbtag':'freeMB',
        'unit':'MB',
        'description':'Remaining free disk space',
        'lb':800,
        'interval':60,
    },
]


if '__main__' == __name__:
    for c in conf:
        print '- - -'
        for k,v in c.iteritems():
            print k, ':' ,v

    import sys
    sys.path.append('../..')
    from os.path import basename
    from storage.storage2 import create_table
    create_table(conf,basename(__file__).split('.')[0].replace('_','-'))
