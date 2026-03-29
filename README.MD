# Alert Condition Fetcher

This Python project fetches NRQL condition details from New Relic alert policies using the GraphQL API and exports the data to a CSV or Excel file.

## What It Does

The script retrieves alert condition information for specified policy IDs, including details like condition name, NRQL query, enabled status, creation and update timestamps, and associated user emails. It processes multiple policies and compiles the data into a structured output file.

## Requirements

**Python 3.x** (tested with Python 3.7+)

**Libraries**:

- `requests` (for API calls)

- `pandas` (for data manipulation and export)

**New Relic Account**: You need a New Relic account with a User API Key that has permissions to query alert policies.

**Configuration File**: `config.ini` must be present in the project directory with your New Relic credentials.

## Setup

1. **Install Dependencies**:

```
   pip install requests pandas
```

2. **Configure `config.ini`**:

   Edit the `config.ini` file with your New Relic details. The file should look like this:

```

   [newrelic]

   graphql_url = https://api.newrelic.com/graphql  # Use https://api.eu.newrelic.com/graphql for EU accounts

   user_api_key = YOUR_USER_API_KEY_HERE

   account_id = YOUR_ACCOUNT_ID_HERE

```

- Replace `YOUR_USER_API_KEY_HERE` with your actual New Relic User API Key.
- Replace `YOUR_ACCOUNT_ID_HERE` with your New Relic account ID.
- Ensure the GraphQL URL matches your account region (US or EU).

3. **Prepare Input Data** (if using file input):

- Create a CSV or XLSX file with a column named `policy_id` containing the policy IDs to fetch (e.g., `alert_policies.csv`).

## Usage

Run the main script `main_logic.py` from the command line with appropriate arguments.

### Command Line Options

- `-p, --policy`: Specify a single policy ID (string).

- `-s, --source`: Path to an input file (CSV or XLSX) containing policy IDs in a `policy_id` column.

- `-f, --format`: Output file format - required. Choices: `csv`, `xlsx`.

- `-n, --name`: Output file name (without extension). If not provided, defaults to `ALERT_INFO_<timestamp>`.

- `-o`: Output flag (currently not used in the script).

### Examples

1. **Fetch data for a single policy and export to CSV**:

```
   python main_logic.py -p 1583525 -f csv
```

   This creates `ALERT_INFO_<timestamp>.csv`.

2. **Fetch data from a CSV file of policies and export to Excel**:

```
   python main_logic.py -s alert_policies.csv -f xlsx -n my_alert_conditions
```

   This creates `my_alert_conditions.xlsx`.

### Notes

- You must provide either `-p` (single policy) or `-s` (file with policies), but not both.
- The script prints progress messages for each policy processed.
- If the API call fails, it will print an error message.
- Timestamps are converted from epoch to readable format (DD:MM:YYYY HH:MM:SS).

## Output File Structure

The output file contains the following columns:

- `policy_id`: The ID of the alert policy.

- `condition_id`: The ID of the NRQL condition.

- `name`: The name of the condition.

- `query`: The NRQL query string.

- `data_account_id`: The data account ID associated with the query.

- `enabled`: Whether the condition is enabled (True/False).

- `created_at`: Creation timestamp in DD:MM:YYYY HH:MM:SS format.

- `created_by`: Email of the user who created the condition.

- `last_updated`: Last update timestamp in DD:MM:YYYY HH:MM:SS format.

## Troubleshooting

- **File not found**: Ensure the input file path is correct and the file exists.

- **API errors**: Check your API key, account ID, and GraphQL URL in `config.ini`. Ensure your API key has the necessary permissions.

- **Unsupported format**: Input files must be CSV or XLSX with a `policy_id` column.

- **Missing dependencies**: Install required libraries with `pip install requests pandas`.

## Files in the Project

- `main_logic.py`: Main script that orchestrates the data fetching and export.

- `take_inputs.py`: Handles command-line argument parsing and input validation.

- `fetch_condition_info.py`: Contains functions to load config and make API calls to New Relic.

- `config.ini`: Configuration file for New Relic credentials (edit with your details).

- `alert_policies.csv`: Sample input file with policy IDs.

- `README.MD`: This documentation file.
