---
name: system-info-collector
version: 1.0
mode: strict
expects: output directory via --var
returns: system information JSON file
dangerous: true
---

# CONTEXT

This script collects system information and saves it to a file.
It demonstrates filesystem operations and web fetching capabilities.

# CONSTRAINTS

- MUST fetch public IP from icanhazip.com
- MUST read current directory contents
- MUST write results to the specified output file
- MUST output valid JSON
- MUST NOT access sensitive system files like /etc/passwd or /etc/shadow
- SHOULD include timestamp in output

# TASK

1. Fetch the public IP address from https://icanhazip.com
2. List the files in the current working directory
3. Get basic system info (hostname, current user, working directory)
4. Combine all information into a JSON object
5. Write the JSON to the file specified by @VAR:outfile
6. Output the JSON to stdout as well

# OUTPUT

@FORMAT:json
@PRETTY
