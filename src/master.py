
import da
PatternExpr_614 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_621 = da.pat.FreePattern('p')
PatternExpr_662 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_669 = da.pat.FreePattern('p')
PatternExpr_739 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_746 = da.pat.FreePattern('p')
PatternExpr_752 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_759 = da.pat.FreePattern('p')
PatternExpr_778 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_783 = da.pat.FreePattern('p')
PatternExpr_805 = da.pat.TuplePattern([])
PatternExpr_822 = da.pat.TuplePattern([])
_config_object = {'channel': 'fifo', 'clock': 'Lamport'}
import logging
import sys
import csv
import config as cfg
import constants as const
import xmltodict, json
import pandas as pd
import random
import time

def get_logger(name, path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(path, mode='w')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

class DBEmulator(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_614, sources=[PatternExpr_621], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_613]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_662, sources=[PatternExpr_669], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_661])])

    def setup(self, config):
        self._state.config = config
        self._state.conf = self._state.config['db_config']
        self._state.minLatency = self._state.config['minDBlatency']
        self._state.maxLatency = self._state.config['maxDBlatency']
        self._state.logger = get_logger('db_logger', self._state.config['db_log'])
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
        super()._label('_st_label_403', block=False)
        _st_label_403 = 0
        while (_st_label_403 == 0):
            _st_label_403 += 1
            if False:
                _st_label_403 += 1
            else:
                super()._label('_st_label_403', block=True)
                _st_label_403 -= 1

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
        return payload

    def _DBEmulator_handler_613(self, data, p):
        self._state.logger.info('[DB_READ_REQ] payload:{}'.format(data))
        payload = self._op(self._read, data)
        self._send(('DB_READ_RESPONSE', payload), p)
        self._state.logger.info('[DB_READ_RESP] payload:{}'.format(data))
    _DBEmulator_handler_613._labels = None
    _DBEmulator_handler_613._notlabels = None

    def _DBEmulator_handler_661(self, data, p):
        self._state.logger.info('[DB_WRITE_REQ] payload:{}'.format(data))
        payload = self._op(self._write, data)
        self._send(('DB_WRITE_RESPONSE', payload), p)
        self._state.logger.info('[DB_WRITE_RESP] payload:{}'.format(data))
    _DBEmulator_handler_661._labels = None
    _DBEmulator_handler_661._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_739, sources=[PatternExpr_746], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_738]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_1', PatternExpr_752, sources=[PatternExpr_759], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_751])])

    def setup(self, coord_ps):
        self._state.coord_ps = coord_ps
        pass

    def run(self):
        self._send(('DB_WRITE', {'table': 'employee', 'payload': {'id': 1, 'name': 'emp10'}, 'delay': True}), self._state.coord_ps)
        super()._label('_st_label_734', block=False)
        _st_label_734 = 0
        while (_st_label_734 == 0):
            _st_label_734 += 1
            if False:
                _st_label_734 += 1
            else:
                super()._label('_st_label_734', block=True)
                _st_label_734 -= 1

    def _ClientP_handler_738(self, data, p):
        pass
    _ClientP_handler_738._labels = None
    _ClientP_handler_738._notlabels = None

    def _ClientP_handler_751(self, data, p):
        pass
    _ClientP_handler_751._labels = None
    _ClientP_handler_751._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_778, sources=[PatternExpr_783], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_777])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_773', block=False)
        _st_label_773 = 0
        while (_st_label_773 == 0):
            _st_label_773 += 1
            if False:
                _st_label_773 += 1
            else:
                super()._label('_st_label_773', block=True)
                _st_label_773 -= 1

    def _SubCoordP_handler_777(self, p):
        self.output('Response received in sub process!!')
        self._send(('APP_EVALUATION_RESPONSE',), p)
    _SubCoordP_handler_777._labels = None
    _SubCoordP_handler_777._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_805, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_804])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_804(self):
        pass
    _ResCoordP_handler_804._labels = None
    _ResCoordP_handler_804._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_822, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_821])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_821(self):
        pass
    _WorkerP_handler_821._labels = None
    _WorkerP_handler_821._notlabels = None

class _NodeMain(da.DistProcess):

    def run(self):
        config_fpath = (sys.argv[1] if (len(sys.argv) > 1) else '../config/main-config.json')
        config = cfg.load_config(config_fpath)
        db_ps = da.new(DBEmulator, num=1)
        da.setup(db_ps, (config,))
        da.start(db_ps)
        cli_ps = da.new(ClientP, num=config['num_clients'])
        da.setup(cli_ps, (db_ps,))
        da.start(cli_ps)
