# sample code for reading a policy.  CSE 535, Fall 2016, Scott Stoller.

import xml.etree.ElementTree as ET
import da

def main():
    tree = ET.parse('../config/policy-list.xml')
    root = tree.getroot()
    for rule in root.iter('rule'):
        print('rule', rule.attrib['name'])
        sc=rule.find('subjectCondition')
        print('subject condition', sc.attrib)
        rc=rule.find('resourceCondition')
        print('resource condition', rc.attrib)
        act=rule.find('action')
        print('action', act.attrib)
        su=rule.find('subjectUpdate')
        if su != None:
            print('subject update', su.attrib)
        ru=rule.find('resourceUpdate')
        if ru != None:
            print('resource update', ru.attrib)
        print()
        
main()
