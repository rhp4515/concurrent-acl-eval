# sample code for reading a policy.  CSE 535, Fall 2016, Scott Stoller.

import xml.etree.ElementTree as ET
import constants as const
class PolicyParser():
    def __init__(self):
        tree = ET.parse('../config/policy-list.xml')
        self.root = tree.getroot()

    def get_sub_attr(self, sub, res):
        sub_attrs = set()
        for rule in self.root.iter('rule'):
            sc = rule.find('subjectCondition')
            rc = rule.find('resourceCondition')
            if sub['name'] == sc.attrib['name'] and res['name'] == rc.attrib['name']:
                su = rule.find('subjectUpdate')
                if su != None:
                    for attr in su.attrib:
                        if attr not in const.KEY_ATTRS:
                            sub_attrs.add(attr)
        return sub_attrs

    def get_res_attr(self, sub, res):
        res_attrs = set()
        for rule in self.root.iter('rule'):
            sc = rule.find('subjectCondition')
            rc = rule.find('resourceCondition')
            if sub['name'] == sc.attrib['name'] and res['name'] == rc.attrib['name']:
                ru = rule.find('resourceUpdate')
                if ru != None:
                    for attr in ru.attrib:
                        if attr not in const.KEY_ATTRS:
                            res_attrs.add(attr)
        return res_attrs

    def check_sub_cond(self, sc, sub):

        if sub['name'] != sc['name']:
            return False

        for attr in sc:
            if attr in const.KEY_ATTRS:
                continue
            if sc[attr] == 'empty' and sub['attr'][attr] == '':
                continue
            if sc[attr] != sub['attr'][attr]:
                return False

        return True

    def check_res_cond(self, rc, res):
        if res['name'] != rc['name']:
            return False

        for attr in rc:
            if attr in const.KEY_ATTRS:
                continue
            if rc[attr].find('<') > -1 and res['attr'][attr] >= int(rc[attr][1:]):
                return False
            elif rc[attr].find('>') > -1 and res['attr'][attr] <= int(rc[attr][1:]):
                return False
            elif rc[attr].find('=') > -1 and res['attr'][attr] != int(rc[attr][1:]):
                return False

        return True

    def update_sub_attr(self, su, sub_attr):
        # updating history
        for attr in su:
            print('update_sub_attr', attr, sub_attr[attr], su[attr])
            sub_attr[attr] = su[attr]
        return sub_attr

    def update_res_attr(self, ru, res_attr):
        # updating view count
        for attr in ru:
            if ru[attr] == '++':
                res_attr[attr] += 1
            elif ru[attr] == '--':
                res_attr[attr] -= 1
        return res_attr

    def evaluate(self, sub, res, act):
        status = False
        # sub, res should contain some attrs from db
        print('evaluate', sub, res, act)
        for rule in self.root.iter('rule'):
            sc=rule.find('subjectCondition')
            if not self.check_sub_cond(sc.attrib, sub):
                continue
            rc=rule.find('resourceCondition')
            if not self.check_res_cond(rc.attrib, res):
                continue

            ac=rule.find('action')
            if act['name'] != ac.attrib['name']:
                continue
            su=rule.find('subjectUpdate')
            if su != None:
                # Updating attributes to the received request
                sub['attr'] = self.update_sub_attr(su.attrib, sub['attr'])
                status = True

            ru=rule.find('resourceUpdate')
            if ru != None:
                res['attr'] = self.update_res_attr(ru.attrib, res['attr'])
                status = True

        return status, sub, res, act

    def parse(self):
        for rule in self.root.iter('rule'):
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

# p = PolicyParser()
# sub = {'name':'customer', 'attr': {}, 'id':'2'}
# res = {'name':'movie', 'attr': {'viewCount': 5}, 'id':'1' }
# act = {'name': 'view'}
# print(p.evaluate(sub, res, act))
# sub = {'name':'employee', 'attr': {'history': ''}, 'id': '3'}
# res = {'name':'bank A', 'attr': {}}
# act = {'name': 'read'}
# # update res attrs only if the status is True
# print(p.evaluate(sub, res, act))
