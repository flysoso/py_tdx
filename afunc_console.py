"""
    examples:
        date 5000
        daterev 20100503
"""

import tdx2

def func1(a):
    print tdx2.parse_time_reverse( int(a[4:]) )

def func2(a):
    print tdx2.parse_time(a[4:].strip())

print 'input h for help, q for quit'

while 1:
    print 'afunc_console_cmd:'
    a = raw_input()
    if a[0:4] == 'date':
        func1(a)
    if a[0:7] == 'daterev':
        func2(a)
    if a=='q':
        print 'bye~'
        break
    if a=='h':
        print __doc__