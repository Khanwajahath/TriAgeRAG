import pandas as pd
from agent import triage
import time
INPUT  = '../support_tickets/support_tickets.csv'
OUTPUT = '../support_tickets/output.csv'
 
df = pd.read_csv(INPUT)
# print(df.head(5))
results = []
 
for i, row in df.iterrows():
    print(f'Processing ticket {i+1}/{len(df)}...')
    try:
        result = triage(
            issue=str(row.get('Issue', '')),
            subject=str(row.get('Subject', '')),
            company=str(row.get('Company', 'None'))
        )
        time.sleep(30)
        results.append({
            'status':        result.get('status', 'escalated'),
            'product_area':  result.get('product_area', 'Unknown'),
            'response':      result.get('response', ''),
            'justification': result.get('justification', ''),
            'request_type':  result.get('request_type', 'invalid'),
        })
    except Exception as e:
        print(f'  Error on row {i}: {e}')
        results.append({
            'status': 'escalated',
            'product_area': 'Unknown',
            'response': 'An error occurred. Escalating for manual review.',
            'justification': f'Processing error: {e}',
            'request_type': 'invalid',
        })
 
out_df = pd.DataFrame(results)
out_df.to_csv(OUTPUT, index=False)
print(f'Done! Results written to {OUTPUT}')
