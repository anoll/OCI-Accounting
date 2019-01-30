import time

def generateTableHeader(htmlFile, resource_table, function_name, tableID):
    htmlFile.write('<table id=\"'+tableID+'\">\n')
    htmlFile.write('  <tr>\n')
    table_header = resource_table.header
    htmlFile.write('    <th onclick=\"'+function_name+'(' + str(0) + ')\">' + table_header.type + '</th>\n')
    htmlFile.write('    <th onclick=\"'+function_name+'(' + str(1) + ')\">' + table_header.region + '</th>\n')
    htmlFile.write('    <th onclick=\"'+function_name+'(' + str(2) + ')\">' + table_header.compartment + '</th>\n')
    htmlFile.write('    <th onclick=\"'+function_name+'(' + str(3) + ')\">' + table_header.state + '</th>\n')
    htmlFile.write('    <th onclick=\"'+function_name+'(' + str(4) + ')\">' + table_header.time_created + '</th>\n')
    htmlFile.write('    <th onclick=\"'+function_name+'(' + str(5) + ')\">' + table_header.shape + '</th>\n')
    htmlFile.write('  </tr>\n')

def generateTable(htmlFile, resource_table, tableID, function_name):
    generateTableHeader(htmlFile, resource_table, function_name, tableID)
    for entry in resource_table.entries:
        htmlFile.write('  <tr>\n')
        htmlFile.write('    <td>' + entry.type + '</td>\n')
        htmlFile.write('    <td>' + entry.region + '</td>\n')
        htmlFile.write('    <td>' + entry.compartment + '</td>\n')
        htmlFile.write('    <td>' + entry.state + '</td>\n')
        htmlFile.write('    <td>' + entry.time_created + '</td>\n')
        htmlFile.write('    <td>' + entry.shape + '</td>\n')
        htmlFile.write('  </tr>\n')
    htmlFile.write('</table>\n')



def generateHtmlTable(file, resource_table):
    lines = file.read().split('\n')
    htmlFile = open('consumption.html','w')

    for line in lines:
        htmlFile.write(line + '\n')
        if '<!-- insert table here -->' in line:
            htmlFile.write('<h3>Total number of services: ' + str(len(resource_table.entries)) + ' </h3>\n')
            htmlFile.write('<h3>Last executed at: ' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())) + ' </h3>\n')
            generateTable(htmlFile, resource_table, 'myTable', 'sortTable')

    htmlFile.close()

def generateHtmlSuffix(file):
    file.write('</body>\n')
    file.write('</html>\n')
