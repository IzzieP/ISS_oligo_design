# Install: pandas, openpyxl, xlsxwriter
# Need: excel file with gene and reed solomon code info, excel file with gene and padlock info
# Change: file names 

import pandas as pd
from code_2_seq import code_2_seq

# Import padlock sequences from excel spreadsheet - 2 columns (Gene + Code)
df = pd.read_excel(r'C:\Users\Izzie\Desktop\bridgeprobe_design\73g_codebook.xlsx')

# Excel often doesn't save 0 in r0 so this ensures that the numbers are treated as a string
cor_code = []
for c in df['Code']:
    cs = str(c)
    if len(cs) == 6:
        correct = '0'+ cs
        cor_code.append(correct)
    else:
        cor_code.append(cs)
df['Code'] = cor_code

# Dictionary of the dye number and corresponding sequence
code_to_seq = {'0': 'GATTAGTCCGTCAACATCGG', '1': 'CGACGAGCGTATATGTATCC', '2': 'GTCCGACTGTTTATCCACAG', '3': 'GCGGACGACCTAAATATGAA', '4': 'TGGAAACGACTCGAAACACT', '5': 'CTTGTCGACATGCGATAACC', '6': 'AATGCGACGTGTCGAGTTTA'}

# Translate reed solomon code using function code_2_seq and add to a new column
db_seq_all_r = []
for c in df['Code']:
    all_r = code_2_seq(c)
    db_seq_all_r.append(all_r)
df['Code_2_seq'] = db_seq_all_r

# Split the Code_2_seq column by commas, and save in 7 different columns - one for each round
df[['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6']] = df['Code_2_seq'].str.split(',', expand=True)

# Delete Code_2_seq column
df.drop(['Code_2_seq', 'Code'], inplace=True, axis=1)

# Read in padlock probe sequences = 2 columns (Gene + Sequence) - make sure all sequences are 80bp - otherwise will be incorrect
pp_df = pd.read_excel(r'C:\Users\Izzie\Desktop\bridgeprobe_design\73g_pp_seq.xlsx')

# Use if sequences have /5Phos/ in front 
pp_df[['Gene', 'Phos','Sequence']] = pp_df['Sequence'].str.split('/', expand=True)
pp_df['Sequence'] = pp_df['Sequence'].str.replace(" ", "")
pp_df.drop(['Gene', 'Phos'], inplace=True, axis=1)

# Extract barcode sequence and add column to main dataframe - relies on a linker-anchor-barcode-linker structure (bp 40-60)
pp_df['Barcode'] = pp_df['Sequence'].str[40:60]
df['Barcode'] = pp_df['Barcode']

# Add barcode to the front of the dye probe binding sequence for each round and gene
df['r0'] = df['Barcode'] + df['r0']
df['r1'] = df['Barcode'] + df['r1']
df['r2'] = df['Barcode'] + df['r2']
df['r3'] = df['Barcode'] + df['r3']
df['r4'] = df['Barcode'] + df['r4']
df['r5'] = df['Barcode'] + df['r5']
df['r6'] = df['Barcode'] + df['r6']

# Save each round to a separate sheet of a excel spreadsheet 
ew = pd.ExcelWriter(r'C:\Users\Izzie\Desktop\bridgeprobe_design\73g_bp.xlsx',engine="xlsxwriter")
df.to_excel(ew, sheet_name="r0", index=False, columns = ['Gene', 'r0'])
df.to_excel(ew, sheet_name="r1", index=False, columns = ['Gene', 'r1'])
df.to_excel(ew, sheet_name="r2", index=False, columns = ['Gene', 'r2'])
df.to_excel(ew, sheet_name="r3", index=False, columns = ['Gene', 'r3'])
df.to_excel(ew, sheet_name="r4", index=False, columns = ['Gene', 'r4'])
df.to_excel(ew, sheet_name="r5", index=False, columns = ['Gene', 'r5'])
df.to_excel(ew, sheet_name="r6", index=False, columns = ['Gene', 'r6'])
ew.save()