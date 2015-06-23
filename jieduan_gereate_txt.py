import tdx2
import afunc


#tdx2.change_path("Z:\\tdxdata")

def generate_stlist(flist):
    print "stlist gen start"
    stlist = []
    i = 0
    for k in flist:
        # console show process percentage
        i+=1;
        if i % 100 == 0: print i, len(flist)
        # write function
        try:
            dline = tdx2.get_dayline_by_fid(k)
            delta_rate = afunc.delta_rate(dline, 3)
            dr = int(delta_rate * 10000) / 100.0
            stlist.append([k, dr])
        except:
            pass
    stlist.sort(key = lambda x: -x[1])
    print "stlist generated"
    return stlist

def write_to_file(stlist):
    print "write to file start"
    '''
    Write k to file
    k = ['sh000001', 1, 2, 3, 4, ....]
    infile: sh00001 \t 1 \t 2 \t3 \t 4 \t \n ...
    '''
    f = open('period.txt', 'w')
    for k in stlist:
        f.write(    k[0]  + '\t')
        for m in k[1:]:
            f.write(    str(m) + '\t')
        f.write('\n')
    print "write to file finished"
    
if __name__ == '__main__':
    flist = tdx2.get_file_list()
    stlist = generate_stlist(flist)
    write_to_file(stlist)