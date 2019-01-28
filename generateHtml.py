def generateHtmlPrefix(file, len):
    file.write('<!DOCTYPE html>\n')
    file.write('<html\n')
    file.write('head\n')
    file.write('style\n')
    file.write('table { \n')
    file.write('   font-family: arial, sans-serif;\n')
    file.write('   border-collapse: collapse;\n')
    file.write('   width: 100%;\n')
    file.write('}\n')
    file.write('\n')
    file.write('td, th { \n')
    file.write('   border: 1px solid #dddddd;\n')
    file.write('   border: 1px solid #dddddd;\n')
    file.write('   padding: 8px;\n')
    file.write('}\n')
    file.write('\n')
    file.write('tr:nth-child(even) {\n')
    file.write('   background-color: #dddddd;\n')
    file.write('}\n')
    file.write('\n')
    file.write('</style>\n')
    file.write('</head>\n')
    file.write('<body>\n')
    file.write('\n')
    file.write('<h2>Current Consumption</h2>\n')
    file.write('\n')
    file.write('<h3>Total number of services: ' + str(len) + ' </h3>\n')


def generateHtmlTable(file, output):
    file.write(output.get_html_string())

def generateHtmlSuffix(file):
    file.write('</body>\n')
    file.write('</html>\n')