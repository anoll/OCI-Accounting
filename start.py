import os
import json
import generateHtml
import sys
'Compartment','Region','Type','Shape','Name','State','Time Created'

class ResourceEntry:
    def __init__(self, compartment, region, type, shape, name, state, time_created):
        self.type = type
        self.region = region
        self.compartment = compartment
        self.name = name
        self.state = state
        self.time_created = time_created
        self.shape = shape


class ResourceTable:
    def __init__(self, header):
        self.header = header
        self.entries = []


#regions = ['eu-frankfurt-1', 'uk-london-1', 'us-ashburn-1', 'us-phoenix-1', 'ca-toronto-1']
regions = ['eu-frankfurt-1']
query_commands = ['compute instance',
                  'db autonomous-data-warehouse',
                  'db autonomous-database',
                  'db system '
                  ]
result = []

resourceTable = ResourceTable(ResourceEntry('Compartment','Region','Type','Shape','Name','State','Time Created'))

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
                    element['region']      = region
                    element['compartment'] = compartment['name']
                    element['type']        = query_command


                result.append(parsed_result)



#Entry point of the code
compartments = os.popen("oci iam compartment list --all --compartment-id-in-subtree true").read()
parsed_json = json.loads(compartments)
data = parsed_json['data']

for compartment in data:
    if compartment['lifecycle-state'] != 'DELETED':
        scan_compartment(compartment)
        if len(result) > 0:
           break



for r in result:
    for e in r:
        type = ''
        name = ''
        region = ''
        compartment = ''
        state = ''
        created = ''
        shape = ''

        if 'type' in e:
            type = e['type']
            if (type == 'db autonomous-data-warehouse') or type == 'db autonomous-database':
                cpu_count = e['cpu-core-count']
                memory_tb = e['data-storage-size-in-tbs']
                shape = '#cpu: ' + str(cpu_count) + ', size: ' + str(memory_tb) + '[TB]'

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
            created = created[:10] # yyyy-mm-dd
        if 'shape' in e:
            shape =     e['shape']

        resourceTable.entries.append(ResourceEntry(compartment, region, type, shape, name, state, created))

full_file_path= sys.argv[1] + '/consumption.html'
if os.path.isfile(full_file_path):
    os.remove(full_file_path)

html_template = open('consumption-source.html', 'r')

generateHtml.generateHtmlTable(html_template, full_file_path, resourceTable)
html_template.close()
