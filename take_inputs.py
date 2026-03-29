import argparse
import pandas as pd
import sys
import os
import time


def read_inputs():

      def read_policy_file(file_path):
            if not os.path.exists(file_path):
                  print(f"File not found: {file_path}")
                  sys.exit(1)

            try:
                  if file_path.endswith(".csv"):
                        df = pd.read_csv(file_path)
                  elif file_path.endswith(".xlsx"):
                        df = pd.read_excel(file_path)
                  else:
                        print("Unsupported file format. Use csv/xlsx")
                        sys.exit(1)
            except Exception as e:
                  print(f"Error reading file: {e}")
                  sys.exit(1)

            if "policy_id" not in df.columns:
                  print("Please keep the column name as 'policy_id'.")
                  sys.exit(1)

            return df["policy_id"].dropna().astype(str).tolist()

      parser = argparse.ArgumentParser(description="Process policy IDs")

      parser.add_argument("-p", "--policy", nargs="?", help="Single policy ID")
      parser.add_argument("-s", "--source", help="Input file (csv/xlsx)")
      parser.add_argument("-o", action="store_true", help="Output flag")
      parser.add_argument(
            "-f",
            "--format",
            required=True,
            choices=["csv", "xlsx"],
            help="Output file format"
      )

      parser.add_argument(
            "-n",
            "--name",
            help="Output file name (without extension)"
      )

      args = parser.parse_args()

      policy_ids = []
      output_file_format = args.format

      if args.policy and not args.source:
            policy_ids = [args.policy]

      elif args.source:
            policy_ids = read_policy_file(args.source)

      else:
            print("Invalid input. Provide either a policy ID or a source file.")
            sys.exit(1)

      if args.name:
            output_file_name = os.path.splitext(args.name)[0]
      else:
            timestamp = int(time.time())
            output_file_name = f"ALERT_INFO_{timestamp}"

      final_output_file = f"{output_file_name}.{output_file_format}"
      return policy_ids, output_file_format, final_output_file