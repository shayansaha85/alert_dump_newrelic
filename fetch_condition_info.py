
import configparser
import requests
import json

def load_config():
      config = configparser.ConfigParser()
      config.read('config.ini')
      
      api_key = config.get('newrelic', 'user_api_key')
      url = config.get('newrelic', 'graphql_url')
      account_id = config.get('newrelic', 'account_id')
      
      return api_key, url, account_id


def call_nerdgraph(api_key, url, query):
      headers = {
            "Content-Type": "application/json",
            "API-Key": api_key
      }

      payload = {
            "query": query
      }

      try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()
      
      except requests.exceptions.RequestException as e:
            print(f"Error while calling NerdGraph API: {e}")
            return None


def get_raw_condition_info(policy_id):
      api_key, url, account_id = load_config()

      query = f"""
                  {{
                        actor {{
                        account(id: {account_id}) {{
                              alerts {{
                              nrqlConditionsSearch(searchCriteria: {{policyId: {policy_id}}}) {{
                              nrqlConditions {{
                                    createdAt
                                    createdBy {{
                                    email
                                    }}
                                    enabled
                                    id
                                    name
                                    nrql {{
                                    dataAccountId
                                    query
                                    }}
                                    updatedAt
                                    policyId
                              }}
                              }}
                              }}
                        }}
                        }}
                        }}
      """

      result = call_nerdgraph(api_key, url, query)
      if result:
            return result


# print(type(get_raw_condition_info('1583525')))