
import da
PatternExpr_527 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_534 = da.pat.FreePattern('p')
PatternExpr_575 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_582 = da.pat.FreePattern('p')
PatternExpr_650 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_657 = da.pat.FreePattern('p')
PatternExpr_663 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_670 = da.pat.FreePattern('p')
PatternExpr_689 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_694 = da.pat.FreePattern('p')
PatternExpr_716 = da.pat.TuplePattern([])
PatternExpr_733 = da.pat.TuplePattern([])
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
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_527, sources=[PatternExpr_534], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_526]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_575, sources=[PatternExpr_582], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_574])])

    def setup(self, config):
        self._state.config = config
        self._state.conf = self._state.config['db_config']
        self._state.minLatency = self._state.config['minDBlatency']
        self._state.maxLatency = self._state.config['maxDBlatency']
        self._state.logger = get_logger('db_logger', self._state.config['db_log'])
        self._state.tables = {}
        with open(self._state.conf, 'r') as f:
            db_data = f.read()
        json_content = json.loads(json.dumps(xmltodict.parse(db_data)))['db']
        json_schema = json_content['schema']
        for schema in json_schema:
            self._state.tables[schema] = pd.DataFrame([], columns=json_schema[schema]['column'])
        json_data = json_content['data']
        for table in json_data:
            self._state.tables[table] = pd.read_json(json.dumps(json_data[table]))

    def run(self):
        print(self._state.tables)
        super()._label('_st_label_363', block=False)
        _st_label_363 = 0
        while (_st_label_363 == 0):
            _st_label_363 += 1
            if False:
                _st_label_363 += 1
            else:
                super()._label('_st_label_363', block=True)
                _st_label_363 -= 1

    def _read(self, df, data):
        row = df[(df['id'] == data['id'])]
        if (len(row) > 0):
            return row.iloc[0].to_json()
        else:
            new_data = []
            cols = df.columns
            for col in cols:
                for k in data:
                    df.ix[(len(df), k)] = data[k]
            return data

    def _write(self, df, data):
        index = df.loc[(df['id'] == data['id'])].index.tolist()
        if (len(index) > 0):
            for k in data:
                df.ix[(index[0], k)] = data[k]
        else:
            df.loc[len(df)] = data
        return data

    def _op(self, fn, data):
        if data['delay']:
            time.sleep(random.randint(self._state.minLatency, self._state.maxLatency))
        payload = fn(self._state.tables[data['table']], data['payload'])
        print(self._state.tables[data['table']])
        return payload

    def _DBEmulator_handler_526(self, data, p):
        self._state.logger.info('[DB_READ_REQ] payload:{}'.format(data))
        payload = self._op(self._read, data)
        self._send(('DB_READ_RESPONSE', payload), p)
        self._state.logger.info('[DB_READ_RESP] payload:{}'.format(data))
    _DBEmulator_handler_526._labels = None
    _DBEmulator_handler_526._notlabels = None

    def _DBEmulator_handler_574(self, data, p):
        self._state.logger.info('[DB_WRITE_REQ] payload:{}'.format(data))
        payload = self._op(self._write, data)
        self._send(('DB_WRITE_RESPONSE', payload), p)
        self._state.logger.info('[DB_WRITE_RESP] payload:{}'.format(data))
    _DBEmulator_handler_574._labels = None
    _DBEmulator_handler_574._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_650, sources=[PatternExpr_657], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_649]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_1', PatternExpr_663, sources=[PatternExpr_670], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_662])])

    def setup(self, coord_ps):
        self._state.coord_ps = coord_ps
        pass

    def run(self):
        self._send(('DB_READ', {'table': 'employee', 'payload': {'id': 10}, 'delay': True}), self._state.coord_ps)
        super()._label('_st_label_645', block=False)
        _st_label_645 = 0
        while (_st_label_645 == 0):
            _st_label_645 += 1
            if False:
                _st_label_645 += 1
            else:
                super()._label('_st_label_645', block=True)
                _st_label_645 -= 1

    def _ClientP_handler_649(self, data, p):
        pass
    _ClientP_handler_649._labels = None
    _ClientP_handler_649._notlabels = None

    def _ClientP_handler_662(self, data, p):
        pass
    _ClientP_handler_662._labels = None
    _ClientP_handler_662._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_689, sources=[PatternExpr_694], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_688])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_684', block=False)
        _st_label_684 = 0
        while (_st_label_684 == 0):
            _st_label_684 += 1
            if False:
                _st_label_684 += 1
            else:
                super()._label('_st_label_684', block=True)
                _st_label_684 -= 1

    def _SubCoordP_handler_688(self, p):
        self.output('Response received in sub process!!')
        self._send(('APP_EVALUATION_RESPONSE',), p)
    _SubCoordP_handler_688._labels = None
    _SubCoordP_handler_688._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_716, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_715])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_715(self):
        pass
    _ResCoordP_handler_715._labels = None
    _ResCoordP_handler_715._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_733, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_732])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_732(self):
        pass
    _WorkerP_handler_732._labels = None
    _WorkerP_handler_732._notlabels = None

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
