
import da
PatternExpr_571 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_578 = da.pat.FreePattern('p')
PatternExpr_603 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_610 = da.pat.FreePattern('p')
PatternExpr_670 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_677 = da.pat.FreePattern('p')
PatternExpr_686 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_693 = da.pat.FreePattern('p')
PatternExpr_715 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_720 = da.pat.FreePattern('p')
PatternExpr_742 = da.pat.TuplePattern([])
PatternExpr_759 = da.pat.TuplePattern([])
_config_object = {'channel': 'fifo', 'clock': 'Lamport'}
import sys
import csv
import config as cfg
import constants as const
import xmltodict, json
import pandas as pd
import random
import time

class DBEmulator(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_571, sources=[PatternExpr_578], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_570]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_603, sources=[PatternExpr_610], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_602])])

    def setup(self, conf, minLatency, maxLatency):
        self._state.conf = conf
        self._state.minLatency = minLatency
        self._state.maxLatency = maxLatency
        self._state.conf = self._state.conf
        self._state.minLatency = self._state.minLatency
        self._state.maxLatency = self._state.maxLatency
        with open(self._state.conf, 'r') as f:
            db_data = f.read()
        json_content = json.loads(json.dumps(xmltodict.parse(db_data)))['db']
        json_data = json_content['data']
        self._state.employee = pd.read_json(json.dumps(json_data['employee']))
        self._state.customer = pd.read_json(json.dumps(json_data['customer']))
        self._state.bank = pd.read_json(json.dumps(json_data['bank']))
        self._state.movie = pd.read_json(json.dumps(json_data['movie']))
        json_schema = json_content['schema']
        emp_bank_hist_schema = json_schema['emp_bank_hist']['column']
        self._state.emp_bank_hist = pd.DataFrame([], columns=emp_bank_hist_schema)
        cust_movie_hist_schema = json_schema['cust_movie_hist']['column']
        self._state.cust_movie_hist = pd.DataFrame([], columns=emp_bank_hist_schema)

    def run(self):
        super()._label('_st_label_343', block=False)
        _st_label_343 = 0
        while (_st_label_343 == 0):
            _st_label_343 += 1
            if False:
                _st_label_343 += 1
            else:
                super()._label('_st_label_343', block=True)
                _st_label_343 -= 1

    def _read(self, df, data):
        row = df[(df['id'] == data['id'])]
        if (len(row) > 0):
            return row.iloc[0].to_json()
        else:
            df.loc[len(self._state.employee)] = data
            return data

    def _write(self, df, data):
        index = df.loc[(df['id'] == data['id'])].index.tolist()
        print(index)
        print(data)
        if (len(index) > 0):
            for k in data:
                df.ix[(index[0], k)] = data[k]
        else:
            df.loc[len(self._state.employee)] = data
        return data

    def _op(self, fn, data):
        payload = None
        if (data['table'] == 'employee'):
            payload = fn(self._state.employee, data['payload'])
        elif (data['table'] == 'customer'):
            payload = fn(self._state.customer, data['payload'])
        elif (data['table'] == 'bank'):
            payload = fn(self._state.bank, data['payload'])
        elif (data['table'] == 'movie'):
            payload = fn(self._state.movie, data['payload'])
        elif (data['table'] == 'emp_bank_hist'):
            payload = fn(self._state.emp_bank_hist, data['payload'])
        elif (data['table'] == 'cust_movie_hist'):
            payload = fn(self._state.cust_movie_hist, data['payload'])
        if data['delay']:
            time.sleep(random.randint(self._state.minLatency, self._state.maxLatency))
        return payload

    def _DBEmulator_handler_570(self, data, p):
        print(data)
        payload = self._op(self._read, data)
        self._send(('DB_READ_RESPONSE', payload), p)
    _DBEmulator_handler_570._labels = None
    _DBEmulator_handler_570._notlabels = None

    def _DBEmulator_handler_602(self, data, p):
        print(data)
        payload = self._op(self._write, data)
        print(self._state.employee)
        self._send(('DB_WRITE_RESPONSE', payload), p)
    _DBEmulator_handler_602._labels = None
    _DBEmulator_handler_602._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_670, sources=[PatternExpr_677], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_669]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_1', PatternExpr_686, sources=[PatternExpr_693], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_685])])

    def setup(self, coord_ps):
        self._state.coord_ps = coord_ps
        pass

    def run(self):
        self._send(('DB_WRITE', {'table': 'employee', 'payload': {'id': 1, 'name': 'emp10'}, 'delay': True}), self._state.coord_ps)
        super()._label('_st_label_665', block=False)
        _st_label_665 = 0
        while (_st_label_665 == 0):
            _st_label_665 += 1
            if False:
                _st_label_665 += 1
            else:
                super()._label('_st_label_665', block=True)
                _st_label_665 -= 1

    def _ClientP_handler_669(self, data, p):
        print(data)
    _ClientP_handler_669._labels = None
    _ClientP_handler_669._notlabels = None

    def _ClientP_handler_685(self, data, p):
        print(data)
    _ClientP_handler_685._labels = None
    _ClientP_handler_685._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_715, sources=[PatternExpr_720], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_714])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_710', block=False)
        _st_label_710 = 0
        while (_st_label_710 == 0):
            _st_label_710 += 1
            if False:
                _st_label_710 += 1
            else:
                super()._label('_st_label_710', block=True)
                _st_label_710 -= 1

    def _SubCoordP_handler_714(self, p):
        self.output('Response received in sub process!!')
        self._send(('APP_EVALUATION_RESPONSE',), p)
    _SubCoordP_handler_714._labels = None
    _SubCoordP_handler_714._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_742, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_741])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_741(self):
        pass
    _ResCoordP_handler_741._labels = None
    _ResCoordP_handler_741._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_759, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_758])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_758(self):
        pass
    _WorkerP_handler_758._labels = None
    _WorkerP_handler_758._notlabels = None

class _NodeMain(da.DistProcess):

    def run(self):
        config_fpath = (sys.argv[1] if (len(sys.argv) > 1) else '../config/main-config.json')
        config = cfg.load_config(config_fpath)
        db_ps = da.new(DBEmulator, num=1)
        da.setup(db_ps, (config['db_config'], config['minDBlatency'], config['maxDBlatency']))
        da.start(db_ps)
        cli_ps = da.new(ClientP, num=config['num_clients'])
        da.setup(cli_ps, (db_ps,))
        da.start(cli_ps)
