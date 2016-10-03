
import da
PatternExpr_548 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_555 = da.pat.FreePattern('p')
PatternExpr_580 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_587 = da.pat.FreePattern('p')
PatternExpr_637 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_644 = da.pat.FreePattern('p')
PatternExpr_653 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_660 = da.pat.FreePattern('p')
PatternExpr_682 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_687 = da.pat.FreePattern('p')
PatternExpr_709 = da.pat.TuplePattern([])
PatternExpr_726 = da.pat.TuplePattern([])
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
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_548, sources=[PatternExpr_555], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_547]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_580, sources=[PatternExpr_587], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_579])])

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
        super()._label('_st_label_337', block=False)
        _st_label_337 = 0
        while (_st_label_337 == 0):
            _st_label_337 += 1
            if False:
                _st_label_337 += 1
            else:
                super()._label('_st_label_337', block=True)
                _st_label_337 -= 1

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
            for k in data:
                df.ix[(index[0], k)] = data[k]
        else:
            df.loc[len(self._state.employee)] = data
        return data

    def _op(self, fn, data):
        payload = None
        if (data['table'] == 'employee'):
            payload = fn(self._state.employee, data)
        elif (data['table'] == 'customer'):
            payload = fn(self._state.customer, data)
        elif (data['table'] == 'bank'):
            payload = fn(self._state.bank, data)
        elif (data['table'] == 'movie'):
            payload = fn(self._state.movie, data)
        elif (data['table'] == 'emp_bank_hist'):
            payload = fn(self._state.emp_bank_hist, data)
        elif (data['table'] == 'cust_movie_hist'):
            payload = fn(self._state.cust_movie_hist, data)
        return payload

    def _DBEmulator_handler_547(self, data, p):
        print(data)
        payload = self._op(self._read, data)
        self._send(('DB_READ_RESPONSE', payload), p)
    _DBEmulator_handler_547._labels = None
    _DBEmulator_handler_547._notlabels = None

    def _DBEmulator_handler_579(self, data, p):
        print(data)
        payload = self._op(self._write, data)
        self._send(('DB_WRITE_RESPONSE', payload), p)
    _DBEmulator_handler_579._labels = None
    _DBEmulator_handler_579._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_637, sources=[PatternExpr_644], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_636]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_1', PatternExpr_653, sources=[PatternExpr_660], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_652])])

    def setup(self, coord_ps):
        self._state.coord_ps = coord_ps
        pass

    def run(self):
        self._send(('DB_WRITE', {'table': 'employee', 'id': 1, 'name': 'emp10'}), self._state.coord_ps)
        super()._label('_st_label_632', block=False)
        _st_label_632 = 0
        while (_st_label_632 == 0):
            _st_label_632 += 1
            if False:
                _st_label_632 += 1
            else:
                super()._label('_st_label_632', block=True)
                _st_label_632 -= 1

    def _ClientP_handler_636(self, data, p):
        print(data)
    _ClientP_handler_636._labels = None
    _ClientP_handler_636._notlabels = None

    def _ClientP_handler_652(self, data, p):
        print(data)
    _ClientP_handler_652._labels = None
    _ClientP_handler_652._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_682, sources=[PatternExpr_687], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_681])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_677', block=False)
        _st_label_677 = 0
        while (_st_label_677 == 0):
            _st_label_677 += 1
            if False:
                _st_label_677 += 1
            else:
                super()._label('_st_label_677', block=True)
                _st_label_677 -= 1

    def _SubCoordP_handler_681(self, p):
        self.output('Response received in sub process!!')
        self._send(('APP_EVALUATION_RESPONSE',), p)
    _SubCoordP_handler_681._labels = None
    _SubCoordP_handler_681._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_709, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_708])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_708(self):
        pass
    _ResCoordP_handler_708._labels = None
    _ResCoordP_handler_708._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_726, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_725])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_725(self):
        pass
    _WorkerP_handler_725._labels = None
    _WorkerP_handler_725._notlabels = None

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
