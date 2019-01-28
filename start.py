import os
import json
import generateHtml
from prettytable import PrettyTable


regions = ['eu-frankfurt-1', 'uk-london-1', 'us-ashburn-1', 'us-phoenix-1', 'ca-toronto-1']
#regions = ['eu-frankfurt-1']
query_commands = ['compute instance',
                  'db autonomous-data-warehouse',
                  'db autonomous-database',
                  'db system '
                  ]
result = []

output = {}

def add_result(compartment, cmd, res):
    #No result, returning immediately
    if res == '':
        return


def scan_compartment(compartment):
    compartment_id = compartment['id']
    for region in regions:
        for query_command in query_commands:
            cmd = 'oci --region ' + region + ' ' + query_command + ' list --all --compartment-id ' + compartment_id
            print(cmd)
            res = os.popen(cmd).read();
            if res != '':
                parsed_result = json.loads(res)['data'];
                for element in parsed_result:
                    element['region'] = region
                    element['compartment'] = compartment['name']


                result.append(parsed_result)



#Entry point of the code
compartments = os.popen("oci iam compartment list --all --compartment-id-in-subtree true").read()
parsed_json = json.loads(compartments)
data = parsed_json['data']

for compartment in data:
    if compartment['lifecycle-state'] != 'DELETED':
        scan_compartment(compartment)
#        if len(result) > 0:
#            break


# Write result to file
f = open('interim_result.txt','w')

for r in result:
    f.write(str(r) + '\n')


f.close()

output = PrettyTable(['Name', 'Region', 'Compartment', 'State','Time Created', 'Shape'])

count = 0

for r in result:
    for e in r:
        name = ''
        region = ''
        compartment = ''
        state = ''
        created = ''
        shape = ''

        if 'display-name' in e:
            name =      e['display-name']
        if 'region' in e:
            region =    e['region']
        if 'compartment' in e:
            compartment = e['compartment']
        if 'lifecycle-state' in e:
            state =     e['lifecycle-state']
        if 'time-created' in e:
            created =   e['time-created']
        if 'shape' in e:
            shape =     e['shape']

        new_item = (name,region,compartment,state,created,shape)
        output.add_row(new_item)
        count = count + 1


#f = open('consumption.html','w')
f = open('/SEAdmDisk/seadm/www/html/consumption.html','w')


generateHtml.generateHtmlPrefix(f, count)
generateHtml.generateHtmlTable(f, output)
generateHtml.generateHtmlSuffix(f)
f.close()
