import pickle_util

'''
varname = ['ID', 'd5', 'd10','d15',
            'd1', 'ma20', 'last_cl','wattIndex',
           'rd1','lastTime', 'name', 'd30',\
            'variance', 'd180', 'fast_grow', 'fast_fall', 
            'tdx_delta']
'''
def turnArrayToFile(arr):
    
    # get max day num
    maxd = 0
    for k in range(0,50):
        maxd = max(maxd, arr[k][9])
    
    # write to file
    f = open('arr'+ str(maxd)+'.txt', 'w')
    for k in range(0,500):
        sstr = str(arr[k][10])+'\t'+ str(arr[k][7])+'\t'+ str(arr[k][14])+'\t'+ str(arr[k][15])
        f.write(sstr+'\n')
    f.close()

if __name__=='__main__':
    arr = pickle_util.load_arr_from_file('temp0331.arr')
    turnArrayToFile(arr)

