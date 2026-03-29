import take_inputs
import fetch_condition_info
import pandas as pd
from datetime import datetime

inputs = take_inputs.read_inputs()
policy_ids, output_file_format, output_file_name = inputs[0], inputs[1], inputs[2]

def epoch_to_datetime(epoch_time):
    if epoch_time > 1e12:
        epoch_time = epoch_time / 1000

    dt = datetime.fromtimestamp(epoch_time)
    return dt.strftime("%d:%m:%Y %H:%M:%S")

output_sheet_object = {
      'policy_id' : [],
      'condition_id' : [],
      'name' : [],
      'query' : [],
      'data_account_id' : [],
      'enabled' : [],
      'created_at' : [],
      'created_by' : [],
      'last_updated' : [],
}

for policy_id in policy_ids:
      raw_conditon_info = fetch_condition_info.get_raw_condition_info(str(policy_id)) 
      condition_details = raw_conditon_info['data']['actor']['account']['alerts']['nrqlConditionsSearch']['nrqlConditions']

      for condition_detail in condition_details:
            output_sheet_object['policy_id'].append(condition_detail.get('policyId', 'NA'))
            output_sheet_object['condition_id'].append(condition_detail.get('id', 'NA'))
            output_sheet_object['name'].append(condition_detail.get('name', 'NA'))
            nrql = condition_detail.get('nrql')
            if nrql:
                output_sheet_object['query'].append(nrql.get('query', 'NA'))
                output_sheet_object['data_account_id'].append(nrql.get('dataAccountId', 'NA'))
            else:
                output_sheet_object['query'].append('NA')
                output_sheet_object['data_account_id'].append('NA')
            output_sheet_object['enabled'].append(condition_detail.get('enabled', 'NA'))
            created_at = condition_detail.get('createdAt')
            if created_at is not None:
                try:
                    output_sheet_object['created_at'].append(epoch_to_datetime(int(created_at)))
                except (ValueError, TypeError):
                    output_sheet_object['created_at'].append('NA')
            else:
                output_sheet_object['created_at'].append('NA')
            created_by = condition_detail.get('createdBy')
            if created_by:
                output_sheet_object['created_by'].append(created_by.get('email', 'NA'))
            else:
                output_sheet_object['created_by'].append('NA')
            updated_at = condition_detail.get('updatedAt')
            if updated_at is not None:
                try:
                    output_sheet_object['last_updated'].append(epoch_to_datetime(int(updated_at)))
                except (ValueError, TypeError):
                    output_sheet_object['last_updated'].append('NA')
            else:
                output_sheet_object['last_updated'].append('NA')
      print(f'*** DATA COLLECTION DONE FOR POLICY ID : {policy_id} ***')

df = pd.DataFrame(output_sheet_object)

if str(output_file_format).lower() == 'csv':
      df.to_csv(output_file_name, index = False)
elif str(output_file_format).lower() == 'xlsx':
      df.to_excel(output_file_name, index = False)

print('WORK COMPLETED')