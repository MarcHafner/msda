import subprocess
import pandas as pd
from statsmodels.sandbox.stats.multicomp import multipletests
import os
import time
import shutil


def prune_by_background(library, background):
    bc = open(background).readlines()
    bc_list = [pr.split('\n')[0] for pr in bc]
    terms = open('enrichr_libraries/%s.txt' % library).readlines()
    new_terms = []
    for term in terms:
        gene_list = term.split('\t')[2:-1]
        genes_in_background = [gene for gene in gene_list
                               if gene in bc_list]
        new_term = '\t'.join(term.split('\t')[0: 2] +
                             genes_in_background + ['\n'])
        new_terms.append(new_term)
    return new_terms


def get_enrichment(gene_list, library, background=None,
                   output_file='gser'):
    output_xml = '%s.xml' % output_file
    if background:
        lib_list = prune_by_background(library, background)
        with open('enrichr_libraries_bc/%s.txt' % library, 'wb') as f:
            for term in lib_list:
                f.write('%s\n' % term)
        lib = 'enrichr_libraries_bc/%s.txt' % library
    else:
        lib = 'enrichr_libraries/%s.txt' % library
    subprocess.call(['java', '-jar', 'jars/enrichr.jar',
                     gene_list, lib, output_xml])
    time.sleep(10)    
    if os.path.isfile('%s_%s.tsv' % (output_file, library)):
        df = pd.read_table('%s_%s.tsv' % (output_file, library))
        df = get_adjusted_pvals(df)        
        # os.remove(lib)
    else:
        df = None
    return df


def get_adjusted_pvals(df):
    pvals = df['P-value'].tolist()
    adpvals = multipletests(pvals, 0.1, method='fdr_bh')
    df['Adjusted P-value'] = adpvals[1]
    return df
