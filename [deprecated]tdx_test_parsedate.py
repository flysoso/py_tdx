import tdx2

dline = tdx2.get_dayline_by_fid()

strDateRange = str(tdx2.parse_time_reverse( dline[0].ftime )) + '-' + \
    str(tdx2.parse_time_reverse( dline[-1].ftime ))
    
print strDateRange