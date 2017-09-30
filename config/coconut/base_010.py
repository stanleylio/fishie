name = 'Wet Lab (rooftop omni)'
location = 'Wet Lab, Coconut Island'
google_earth_link = '#'
note = 'bbb-based'
public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDliv+VuXcO2vI6BFgEjxnpOZ0zDhsg8jGgiWiiQfek2K2zTDJcvdiWh/hfjbjtO/RdnV96qmklTHASyhnGp56nTN0LI5U0AyeDSVa03Kv/ghzo1xQEBO/tAXMBcI4j4C1UJYtnbcsnNPqeEVCdhFZm80+J7fuqmBXE4cz1t5Z6ZiHwiFbvPJ8BBouu9F/hkv1U4qQX1+tOK4lu/p1yFJ2Waop/RNlxk5fFMysfrR6zD91zVu8FqiU8dpjfe5JBYgEwIcLIiAEWRr+r3nWwDcPe5suTvoHvtVF+4SMiS/dhLGWlU4hflM3mYOsF0fBHhvIIzoVmJRiinqEeAQk+1tIh nuc@base-010'


conf = [
    {
        'dbtag':'system_clock',
        'description':'Device clock',
    },
    {
        'dbtag':'uptime_second',
        'description':'Uptime in seconds',
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
