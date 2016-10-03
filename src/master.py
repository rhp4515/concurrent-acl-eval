
import da
PatternExpr_460 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_467 = da.pat.FreePattern('p')
PatternExpr_555 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_562 = da.pat.FreePattern('p')
PatternExpr_624 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_631 = da.pat.FreePattern('p')
PatternExpr_640 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_647 = da.pat.FreePattern('p')
PatternExpr_669 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_674 = da.pat.FreePattern('p')
PatternExpr_696 = da.pat.TuplePattern([])
PatternExpr_713 = da.pat.TuplePattern([])
_config_object = {'channel': 'fifo', 'clock': 'Lamport'}
import sys
import csv
import config as cfg
import constants as const
import xmltodict, json
import pandas as pd

class DBEmulator(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_460, sources=[PatternExpr_467], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_459]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_555, sources=[PatternExpr_562], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_554])])

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
        super()._label('_st_label_336', block=False)
        _st_label_336 = 0
        while (_st_label_336 == 0):
            _st_label_336 += 1
            if False:
                _st_label_336 += 1
            else:
                super()._label('_st_label_336', block=True)
                _st_label_336 -= 1

    def _read(self, df, data):
        row = df[(df['id'] == data['id'])]
        if (len(row) > 0):
            return row.iloc[0].to_json()
        else:
            data.pop('table', None)
            df.loc[len(self._state.employee)] = data
            return data

    def _write(self, df, data):
        index = df.loc[(df['id'] == data['id'])].index.tolist()
        print(index)
        data.pop('table', None)
        print(data)
        if (len(index) > 0):
            df.ix[(index[0], 'id')] = data['id']
            df.ix[(index[0], 'name')] = data['name']
        else:
            df.loc[len(self._state.employee)] = data
        return data

    def _DBEmulator_handler_459(self, data, p):
        print(data)
        payload = None
        if (data['table'] == 'employee'):
            payload = self._read(self._state.employee, data)
        elif (data['table'] == 'customer'):
            payload = self._read(self._state.customer, data)
        elif (data['table'] == 'bank'):
            payload = self._read(self._state.bank, data)
        elif (data['table'] == 'movie'):
            payload = self._read(self._state.movie, data)
        print(self._state.employee)
        self._send(('DB_READ_RESPONSE', payload), p)
    _DBEmulator_handler_459._labels = None
    _DBEmulator_handler_459._notlabels = None

    def _DBEmulator_handler_554(self, data, p):
        print(data)
        if (data['table'] == 'employee'):
            payload = self._write(self._state.employee, data)
        print(self._state.employee)
        self._send(('DB_WRITE_RESPONSE', payload), p)
    _DBEmulator_handler_554._labels = None
    _DBEmulator_handler_554._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_624, sources=[PatternExpr_631], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_623]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_1', PatternExpr_640, sources=[PatternExpr_647], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_639])])

    def setup(self, coord_ps):
        self._state.coord_ps = coord_ps
        pass

    def run(self):
        self._send(('DB_WRITE', {'table': 'employee', 'id': 1, 'name': 'emp10'}), self._state.coord_ps)
        super()._label('_st_label_619', block=False)
        _st_label_619 = 0
        while (_st_label_619 == 0):
            _st_label_619 += 1
            if False:
                _st_label_619 += 1
            else:
                super()._label('_st_label_619', block=True)
                _st_label_619 -= 1

    def _ClientP_handler_623(self, data, p):
        print(data)
    _ClientP_handler_623._labels = None
    _ClientP_handler_623._notlabels = None

    def _ClientP_handler_639(self, data, p):
        print(data)
    _ClientP_handler_639._labels = None
    _ClientP_handler_639._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_669, sources=[PatternExpr_674], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_668])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_664', block=False)
        _st_label_664 = 0
        while (_st_label_664 == 0):
            _st_label_664 += 1
            if False:
                _st_label_664 += 1
            else:
                super()._label('_st_label_664', block=True)
                _st_label_664 -= 1

    def _SubCoordP_handler_668(self, p):
        self.output('Response received in sub process!!')
        self._send(('APP_EVALUATION_RESPONSE',), p)
    _SubCoordP_handler_668._labels = None
    _SubCoordP_handler_668._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_696, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_695])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_695(self):
        pass
    _ResCoordP_handler_695._labels = None
    _ResCoordP_handler_695._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_713, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_712])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_712(self):
        pass
    _WorkerP_handler_712._labels = None
    _WorkerP_handler_712._notlabels = None

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
