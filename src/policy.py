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
            if sub['type'] == sc.attrib['type'] and res['type'] == rc.attrib['type']:
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
            if sub['type'] == sc.attrib['type'] and res['type'] == rc.attrib['type']:
                ru = rule.find('resourceUpdate')
                if ru != None:
                    for attr in ru.attrib:
                        if attr not in const.KEY_ATTRS:
                            res_attrs.add(attr)
        return res_attrs

    def resolve_expr(self, attr_value, sub, res):
        value = None
        if attr_value.find('$') == 0:
            item, key = attr_value[1:].split('.')
            if item == 'resource':
                value = res[key]
            elif item == 'subject':
                value = sub[key]
        return value

    def check_sub_cond(self, sc, sub, res):

        if sub['type'] != sc['type']:
            return False

        # print('subject condition', sc)
        for attr in sc:
            if attr in const.KEY_ATTRS:
                continue

            value = self.resolve_expr(sc[attr], sub, res)
            if value is not None:
                sc[attr] = value

            if sc[attr] == 'empty' and sub['attr'][attr] == '':
                continue

            if sc[attr] == '' and sub['attr'][attr] == '':
                continue

            if sc[attr] != sub['attr'][attr]:
                return False

        return True

    def check_res_cond(self, rc, sub, res):
        if res['type'] != rc['type']:
            return False
        for attr in rc:
            if attr in const.KEY_ATTRS:
                continue
            if rc[attr].find('<') > -1:
                if res['attr'][attr] >= int(rc[attr][1:]):
                    return False
            elif rc[attr].find('>') > -1:
                if res['attr'][attr] <= int(rc[attr][1:]):
                    return False
            else:
                if res['attr'][attr] != int(rc[attr]):
                    return False

        return True

    def update_sub_attr(self, su, sub, res):
        # updating history
        # print('updating subject attr')
        sub_attr = sub['attr']
        for attr in su:
            value = self.resolve_expr(su[attr], sub, res)
            if value is None:
                sub_attr[attr] = su[attr]
            else:
                sub_attr[attr] = value
        return sub_attr

    def update_res_attr(self, ru, sub, res):
        # updating view count
        res_attr = res['attr']
        for attr in ru:
            if ru[attr] == '++':
                res_attr[attr] += 1
            elif ru[attr] == '--':
                res_attr[attr] -= 1
            else:
                res_attr[attr] = ru[attr]
        return res_attr

    def evaluate(self, sub, res, act):
        status = False
        # sub, res should contain some attrs from db
        # print('evaluate', sub, res, act)
        for rule in self.root.iter('rule'):
            sc=rule.find('subjectCondition')
            if not self.check_sub_cond(sc.attrib, sub, res):
                continue
            rc=rule.find('resourceCondition')
            if not self.check_res_cond(rc.attrib, sub, res):
                continue

            ac=rule.find('action')
            if act['type'] != ac.attrib['type']:
                continue
            # All the conditions passed
            status = True
            # Do updates if there are any
            su=rule.find('subjectUpdate')
            if su != None:
                # Updating attributes to the received request
                sub['attr'] = self.update_sub_attr(su.attrib, sub, res)

            ru=rule.find('resourceUpdate')
            if ru != None:
                res['attr'] = self.update_res_attr(ru.attrib, sub, res)

        return status, sub, res, act

    def parse(self):
        for rule in self.root.iter('rule'):
            print('rule', rule.attrib['type'])
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
# sub = {'type':'customer', 'attr': {}, 'id':'2'}
# res = {'type':'song', 'attr': {'viewCount': 9}, 'id':'1' }
# act = {'type': 'listen'}
# print(p.evaluate(sub, res, act))
# sub = {'type':'employee', 'attr': {'history': 'bank C'}}
# res = {'type':'bank', 'id': 'bank B', 'attr': {}}
# act = {'type': 'read'}
# update res attrs only if the status is True
# print(p.evaluate(sub, res, act))
