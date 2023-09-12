#!/usr/bin/python
import sys
import time
import os

def root(sym):
    # Get root of a symbol
    if sym[-3] == '-':
        return sym[:-5]
    else:
        return sym[:-2] 
 
def two_digit_year_to_one_digit(s):
    if s[-2:].isdigit():
        return s[:-2] + s[-1]
	else:
		return s
 
def symbols_and_roots(filename):
    """
    Get list of symbols and roots for a symbol list
    Input: 
        filename (str): name of the file with list of symbols
    Output:
        symbols (list<string>): list of symbols
        roots (list<string>): list of roots
    """
    roots = []
    symbols = []
    f = open(filename,'rU')
    fl = f.readlines()
    for sym in fl:
        sym = sym.replace('\n','')
        symbols.append(sym)
        r = root(sym)
        if r not in roots:
            roots.append(r)
    f.close()
    
    return symbols, roots

def symbols_roots_dict(filename):
    """
    Using list of symbols files get 2 dictionaries: with roots and with symbols.
    """
    f = open(filename, 'rU')
    losf = f.readlines()
    symbols_dict = {}
    roots_dict = {}
    for symbol_file in losf:
        sf = symbol_file[:-1]
        symbols_dict[str(sf)], roots_dict[str(sf)] = symbols_and_roots(sf)
    f.close()
 
    return symbols_dict, roots_dict

def distribute_symbols(input_file, losf):
    """
    Distributes symbols to appropriate files in losf and saves to new files.
    Input:
        input_file (str): List of symbols from Actimize
        losf (str): List of symbol files to be processed
    Output:
        symbols_dict (dict): dictionary with exchanges (file names) as keys and lists of symbols as values
        idn_sf (list<string>): list of strings 
    """
    symbols_dict, roots_dict = symbols_roots_dict(losf)
    idn_sf = [] # list for IDN_SELECTFEED
    f = open(input_file,'rU')
    fl = f.readlines()
    for sym in fl:
        sym = sym.replace('\n','')
        in_file = False
        for exch in symbols_dict.keys():
            if sym not in symbols_dict[exch]:
                if root(sym) in roots_dict[exch]:
                    sym = str(two_digit_year_to_one_digit(sym))
                    symbols_dict[exch].append(sym)
                    in_file = True
                    break
        if not in_file:
            idn_sf.append(sym)
     
    return symbols_dict, idn_sf 

def write_dict(dict, ending='', dirname=''):
    # Write dictionary to files where filename=key, contents=values of the dictionary.
    # 'Ending' argument allows to append some endings to new files (for examle, '_new.txt')
    # 'dirname' is an output directory path relative to the location of this script, it is dependent on keys of the file
    for key in dict.keys():
        # key is '/dir1/dir2/symbols.txt', so we split on '/' and on '.'
        dir = '/'.join(key.split('/')[:-1]) + '/' + dirname
        filename = dir + '/' + key.split('/')[-1].split('.')[0] + ending
        if not os.path.exists(dir):
            os.mkdir(dirname)
        f = open(filename, 'w+')
        for sym in dict[key]:
            f.write(sym + '\n')
        f.close()

def write_list(list, filename, dirname=''):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    filename = dirname + '/' + filename
    f = open(filename, 'w+')
    for item in list:
        f.write(item + '\n')
    f.close()

 
def main():
    args = sys.argv[1:]
    if len(args) != 6:
        print 'Error: wrong number of parameters. Usage: ./create_symbol_lists.py --actimize_file file --list_of_symbol_files losf --output_dir dir_rel_to_dir_in_lsof'    
        sys.exit(1) 
    
    actimize_file = args[1]
    losf = args[3]
    output_dir = args[5]
    idn_output_dir = '/app/th/pkgs/omd/rates/client_data/config/CME_RMDS/ivan/new_symbol_files' 
    
    #symbols_dict, roots_dict = symbols_roots_dict(losf) # get all symbols and roots for all files in 'losf' into a dictionary
    
    symbols_dict, idn_sf = distribute_symbols(actimize_file, losf)
    write_dict(symbols_dict, '_new.txt', output_dir)
    write_list(idn_sf, 'cme_rmds_symbols_to_collect_3.txt', idn_output_dir)    

    # Tests
	#filename = 'cme_rmds_symbols_to_collect_1.txt'    
    #filename = 'test.txt'    
    #all_symbols, all_roots = symbols_and_roots(filename)
    #print(all_symbols[:100])

    #losf = 'losf.txt'
    #losf = 'losf_cme_prism.txt'
    #actimize_file = 'actimize_symbols.txt'
    #symbols_dict, roots_dict = symbols_roots_dict(losf) # get all symbols and roots for all files in 'losf' into a dictionary
    #print(roots_dict)    
    #print(symbols_dict)

    #write_dict(roots_dict, '_new.txt', 'symbol_files/new_symbol_files')
 
    

if __name__ == '__main__':
    t0 = time.time()
    main()
    print "Running time: ", round(time.time()-t0,5)
