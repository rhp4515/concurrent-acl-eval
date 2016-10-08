
import da
PatternExpr_488 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_495 = da.pat.FreePattern('p')
PatternExpr_541 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_548 = da.pat.FreePattern('p')
_config_object = {}
import sys
import csv
import config as cfg
import constants as const
import xmltodict, json
import pandas as pd
import random
import time
from utils import get_logger

class DBEmulator(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_488, sources=[PatternExpr_495], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_487]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_541, sources=[PatternExpr_548], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_540])])

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
        super()._label('_st_label_324', block=False)
        _st_label_324 = 0
        while (_st_label_324 == 0):
            _st_label_324 += 1
            if False:
                _st_label_324 += 1
            else:
                super()._label('_st_label_324', block=True)
                _st_label_324 -= 1

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

    def _DBEmulator_handler_487(self, data, p):
        print('>>>>>>>>>>>>>>>>', p)
        self._state.logger.info('[DB_READ_REQ] payload:{}'.format(data))
        payload = self._op(self._read, data)
        self._send(('DB_READ_RESPONSE', payload), p)
        self._state.logger.info('[DB_READ_RESP] payload:{}'.format(data))
    _DBEmulator_handler_487._labels = None
    _DBEmulator_handler_487._notlabels = None

    def _DBEmulator_handler_540(self, data, p):
        self._state.logger.info('[DB_WRITE_REQ] payload:{}'.format(data))
        payload = self._op(self._write, data)
        self._send(('DB_WRITE_RESPONSE', payload), p)
        self._state.logger.info('[DB_WRITE_RESP] payload:{}'.format(data))
    _DBEmulator_handler_540._labels = None
    _DBEmulator_handler_540._notlabels = None
