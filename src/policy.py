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
        # print(attr_value)
        if attr_value.find('$') == 0:
            item, key = attr_value[1:].split('.')
            # print('resolve_expr sub', sub)
            if item == 'resource':
                # print('resolve_expr res', res)
                # print(item, key)
                # print(res[key])
                value = res[key]
            elif item == 'subject':
                return sub[key]
        # print ("value -- resolve_expr", value)
        return value

    def check_sub_cond(self, sc, sub, res):
        read_attrs = set()

        # print('subject condition', sc['type'], sub['type'])

        if sub['type'] != sc['type']:
            return False, read_attrs

        for attr in sc:
            if attr in const.KEY_ATTRS:
                continue
            # print(attr)
            read_attrs.add(attr)
            value = self.resolve_expr(sc[attr], sub, res)
            # print ("value -- check_sub_cond", value)
            if value is not None:
                sc[attr] = value

            if sc[attr] == 'empty' and sub['attr'][attr] == '':
                continue

            if sc[attr] == '' and sub['attr'][attr] == '':
                continue

            if sc[attr] != sub['attr'][attr]:
                # print('sc attr', sc[attr])
                # print('sub attr', sub['attr'][attr])
                # print('Returning False')
                return False, read_attrs

        return True, read_attrs

    def check_res_cond(self, rc, sub, res):
        read_attrs = set()

        # print('resource condition', rc['type'], res['type'])

        if res['type'] != rc['type']:
            return False, read_attrs

        for attr in rc:
            if attr in const.KEY_ATTRS:
                continue
            read_attrs.add(attr)
            if rc[attr].find('<') > -1:
                if res['attr'][attr] >= int(rc[attr][1:]):
                    return False, read_attrs
            elif rc[attr].find('>') > -1:
                if res['attr'][attr] <= int(rc[attr][1:]):
                    return False, read_attrs
            else:
                if res['attr'][attr] != int(rc[attr]):
                    return False, read_attrs

        return True, read_attrs

    def update_sub_attr(self, su, sub, res):
        # updating history
        print('updating subject attr')
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
        print('updating resource attr')
        res_attr = res['attr']
        for attr in ru:
            if ru[attr] == '++':
                res_attr[attr] += 1
            elif ru[attr] == '--':
                res_attr[attr] -= 1
            else:
                res_attr[attr] = ru[attr]
        return res_attr

    def get_read_write_map(self, sub, res, act):
        read_write_map = dict()
        for rule in self.root.iter('rule'):
            sc=rule.find('subjectCondition')
            if sub['type'] != sc.attrib['type']:
                continue
            rc=rule.find('resourceCondition')
            if res['type'] != rc.attrib['type']:
                continue
            ac=rule.find('action')
            if act['type'] != ac.attrib['type']:
                continue

            key = (sc.attrib['type'], rc.attrib['type'], ac.attrib['type'])

            su = rule.find('subjectUpdate')
            ru = rule.find('resourceUpdate')
            if su is None and ru is None:
                continue
            elif su is not None and ru is None:
                read_write_map[key] = (res['type'], sub['type'])
            elif ru is not None and su is None:
                read_write_map[key] = (sub['type'], res['type'])

            return read_write_map

    # Assuming subject types and resource types are disjoint
    def get_all_attrs(self, type):
        all_attrs = set()
        for rule in self.root.iter('rule'):
            sc=rule.find('subjectCondition')
            rc=rule.find('resourceCondition')

            su=rule.find('subjectUpdate')
            ru=rule.find('resourceUpdate')

            if sc is not None and sc.attrib['type'] == type:
                all_attrs.update(set(sc.attrib.keys()))
                if su is not None:
                    all_attrs.update(set(su.attrib.keys()))

            elif rc is not None and rc.attrib['type'] == type:
                all_attrs.update(set(rc.attrib.keys()))
                if ru is not None:
                    all_attrs.update(set(ru.attrib.keys()))

        return all_attrs.difference(set(const.KEY_ATTRS))

    def attrs_in_matching_policies(self, r_type, w_type, a_type):
        def_r_attrs = set()
        for rule in self.root.iter('rule'):
            sc=rule.find('subjectCondition')
            rc=rule.find('resourceCondition')
            ac=rule.find('action')

            if ac.attrib['type'] == a_type and (
                sc.attrib['type'] == r_type and rc.attrib['type'] == w_type) or (
                sc.attrib['type'] == w_type and rc.attrib['type'] == r_type):
                if len(def_r_attrs) == 0:
                    def_r_attrs.update(set(sc.attrib.keys()))
                else:
                    def_r_attrs.intersection_update(set(sc.attrib.keys()))

            su=rule.find('subjectUpdate')
            ru=rule.find('resourceUpdate')

        return def_r_attrs.difference(set(const.KEY_ATTRS))

    def execute_policy(self, r_obj, w_obj, act):
        decision = False
        updated_obj = None

        r_type = r_obj['type']
        w_type = w_obj['type']

        decision, updated_obj, read_attrs = self.evaluate(r_obj, w_obj, act)

        w_read_attrs = None

        if updated_obj is None:
            decision, updated_obj, w_read_attrs = self.evaluate(w_obj, r_obj, act)

        # updated_obj['updates'] = dict()
        # print ("????????", read_attrs)
        # print ("????????", w_read_attrs)

        if w_read_attrs is not None:
            read_attrs[r_type].update(w_read_attrs[r_type])
            read_attrs[w_type].update(w_read_attrs[w_type])
        # print("????????", read_attrs)
        result = dict(decision=decision,
                      updated_obj=updated_obj,
                      read_attrs=read_attrs)
        # print(">>>>>>>>>>>>>>", result)
        return result

    def evaluate(self, sub, res, act):
        status = False
        # sub, res should contain some attrs from db
        # print('evaluate', sub, res, act)
        read_attrs = dict()
        read_attrs[sub['type']] = set()
        read_attrs[res['type']] = set()

        updated_obj = None
        for rule in self.root.iter('rule'):
            sc=rule.find('subjectCondition')

            flag, sub_read_attrs = self.check_sub_cond(sc.attrib, sub, res)
            read_attrs[sub['type']].update(sub_read_attrs)
            if not flag:
                continue

            rc=rule.find('resourceCondition')
            flag, res_read_attrs = self.check_res_cond(rc.attrib, sub, res)
            read_attrs[res['type']].update(res_read_attrs)
            if not flag:
                continue

            ac=rule.find('action')
            if act['type'] != ac.attrib['type']:
                continue
            # All the conditions passed

            # print(" evaluate >>>>>>>>>>>>", read_attrs)
            # Do updates if there are any
            su=rule.find('subjectUpdate')
            if su != None:
                # Updating attributes to the received request
                updated_obj = sub
                updated_obj['updates'] = self.update_sub_attr(su.attrib, sub, res)
                read_attrs[sub['type']].update(set(updated_obj['updates'].keys()))
                # print(" subjectUpdate >>>>>>>>>>>>", read_attrs)
                status = True
            else:
                status = True

            ru=rule.find('resourceUpdate')
            if ru != None:
                updated_obj = res
                updated_obj['updates'] = self.update_res_attr(ru.attrib, sub, res)
                read_attrs[res['type']].update(set(updated_obj['updates'].keys()))
                # print(" resourceUpdate >>>>>>>>>>>>", read_attrs)
                status = True
            else:
                status = True
            # print('status', status)
        # print('status after all rules', status)
        # print('updated_obj', updated_obj)
        print("returning read_attrs", read_attrs)
        return status, updated_obj, read_attrs

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
# res = {'type':'song', 'attr': {'listenCount': 2}, 'id':'1' }
# act = {'type': 'listen'}
# print(p.get_read_write_map(sub, res, act))
# sub = {'type':'employee', 'attr': {'history': 'bank B'}}
# res = {'type':'bank', 'id': 'bank B', 'attr': {}}
# act = {'type': 'read'}
# update res attrs only if the status is True
# p.execute_policy(sub, res, act)
