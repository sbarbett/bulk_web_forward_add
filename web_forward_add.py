import csv, ultra_rest_client, json, sys, time

if len(sys.argv) == 2 and sys.argv[1].lower() == "help":
    sys.exit("Expected use: python web_forward_add.py username password account_name example.csv [use_http host:port]\nArgument 1:\n\tweb_forward_mod.py -- The name of your python file\nArgument 2:\n\tusername -- Username of the UltraDNS account\nArgument 3:\n\tpassword -- UltraDNS account password\nArgument 4:\n\taccount_name -- The name of your UltraDNS account\nArguments 5 and 6 (optional):\n\tuse_http -- Specify this value as 'True' if you wish to use a test environment\n\thost:port -- The hostname and port of your test environment (Example: test-restapi.ultradns.com:443)\n")
    
if len(sys.argv) != 7 and len(sys.argv) != 5:
    raise Exception("Expected use: python web_forward_add.py username password account_name example.csv [use_http host:port]\n\nType 'python web_forward_mod.py help' for more information.\n")

username = sys.argv[1]
password = sys.argv[2]
account_name = sys.argv[3]
# Check file extension
if sys.argv[4].endswith(".csv") is not True:
    raise Exception("File must be a CSV.")
input_file = csv.reader(open(sys.argv[4], "rb"))
use_http = 'False'
domain = 'restapi.ultradns.com'
# This is for pointing at a test environment
if len(sys.argv) == 7:
    use_http = sys.argv[5]
    domain = sys.argv[6]
  
# Establish an API connection
c = ultra_rest_client.RestApiClient(username, password, 'True' == use_http, domain)

# Add trailing dot
def check_trailing_dot(z):
    if z.endswith(".") is False:
        return z + "."
    else:
        return z
        
output_file = "results_" + str(int(time.time())) + ".csv"
with open(output_file, "w") as csv_output:
    # Set output CSV headers
    writer = csv.DictWriter(csv_output, fieldnames=['Zone', 'Zone create response', 'Apex forward create response', 'WWW forward create response'])
    writer.writeheader()
    # Skip fheader row of input file
    first_row = True
    for row in input_file:
        if first_row:
            first_row = False
            continue
        # Set variables
        if len(row) < 2:
            continue
        # Set variables
        zone = row[0]
        redirect_to = row[1]
        zone_create_msg = None
        apex_create_msg = None
        www_create_msg = None
        
        # Try to create the zone
        zone_create_response = c.create_primary_zone(username, check_trailing_dot(zone))
        print json.dumps(zone_create_response)
        if isinstance(zone_create_response, list) and zone_create_response[0]['errorMessage']:
            zone_create_msg = zone_create_response[0]['errorMessage']
        else:
            zone_create_msg = zone_create_response['message']
        
        # Create apex web forward
        apex_create_response = c.create_web_forward(check_trailing_dot(zone), "http://"+zone, redirect_to, "HTTP_301_REDIRECT")
        print json.dumps(apex_create_response)
        if isinstance(apex_create_response, list) and apex_create_response[0]['errorMessage']:
            apex_create_msg = apex_create_response[0]['errorMessage']
        else:
            apex_create_msg = "Successful, GUID " + apex_create_response['guid']
            
        # Create www web forward
        www_create_response = c.create_web_forward(check_trailing_dot(zone), "http://www."+zone, redirect_to, "HTTP_301_REDIRECT")
        print json.dumps(www_create_response)
        if isinstance(www_create_response, list) and www_create_response[0]['errorMessage']:
            www_create_msg = www_create_response[0]['errorMessage']
        else:
            www_create_msg = "Successful, GUID " + www_create_response['guid']
            
        # Write results to CSV
        writer.writerow({'Zone': zone, 'Zone create response': zone_create_msg, 'Apex forward create response': apex_create_msg, 'WWW forward create response': www_create_msg})
        
    # Close file
    print "Script complete. Saving results to %s" % output_file
    csv_output.close()