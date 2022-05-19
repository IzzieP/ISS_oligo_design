# Dictionary of the dye number and corresponding sequence
code_to_seq = {'0': 'GATTAGTCCGTCAACATCGG', '1': 'CGACGAGCGTATATGTATCC', '2': 'GTCCGACTGTTTATCCACAG', '3': 'GCGGACGACCTAAATATGAA', '4': 'TGGAAACGACTCGAAACACT', '5': 'CTTGTCGACATGCGATAACC', '6': 'AATGCGACGTGTCGAGTTTA'}

# Define code_2_seq variable - will translate reed solomon code into corresponding dye probe binding sequences
def code_2_seq(rs_code):
    seq = []  # Will contain seq versions of letters
    for r in rs_code:
        if r in code_to_seq:
            seq.append(code_to_seq[r])
    return ",".join(seq)