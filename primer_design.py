import pandas as pd
from Bio.Seq import Seq

# Import padlock sequences from excel spreadsheet
df = pd.read_excel(r'/Users/izzie/Desktop/Primer design/73g_pp_seq.xlsx')
# If the /5Phos/ precedes the sequence, this moves it to other columns
df[['Gene', 'Phos', 'Sequence']] = df['Sequence'].str.split('/', expand=True)
# Removes spaces
df['Sequence'] = df['Sequence'].str.replace(" ", "")
# Selects region on padlock that the primer will be designed by
df['Primer_binding_region'] = df['Sequence'].str[5:20]
# Find the reverse complement for the primer binding region and adds to Primer column
primer_seq = []
for s in df['Primer_binding_region']:
    seq = Seq(s)
    rcomp = seq.reverse_complement()
    rcomp_str = str(rcomp)
    primer_seq.append(rcomp_str)
df['Primer'] = primer_seq
# Get rid of unnecessary columns
df.drop(['Gene', 'Phos', 'Primer_binding_region', 'Sequence'], inplace=True, axis=1)
# Save to new excel file
df.to_excel(r'/Users/izzie/Desktop/Primer design/73g_primers.xlsx', index=False)
