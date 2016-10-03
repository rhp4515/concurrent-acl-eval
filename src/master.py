
import da
PatternExpr_395 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ'), da.pat.FreePattern('data')])
PatternExpr_402 = da.pat.FreePattern('p')
PatternExpr_420 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE'), da.pat.FreePattern('data')])
PatternExpr_427 = da.pat.FreePattern('p')
PatternExpr_471 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE_RESPONSE'), da.pat.FreePattern('data')])
PatternExpr_478 = da.pat.FreePattern('p')
PatternExpr_502 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_507 = da.pat.FreePattern('p')
PatternExpr_529 = da.pat.TuplePattern([])
PatternExpr_546 = da.pat.TuplePattern([])
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
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_395, sources=[PatternExpr_402], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_394]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_420, sources=[PatternExpr_427], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_419])])

    def setup(self, conf, minLatency, maxLatency):
        self._state.conf = conf
        self._state.minLatency = minLatency
        self._state.maxLatency = maxLatency
        self._state.conf = self._state.conf
        self._state.minLatency = self._state.minLatency
        self._state.maxLatency = self._state.maxLatency
        print('SETTING UP DB')
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
        print(self._state.employee)
        print(self._state.customer)
        print(self._state.bank)
        print(self._state.movie)
        print(self._state.minLatency)
        print(self._state.maxLatency)
        print(self._state.emp_bank_hist)
        print(self._state.cust_movie_hist)
        print('BUILDING DB')
        super()._label('_st_label_390', block=False)
        _st_label_390 = 0
        while (_st_label_390 == 0):
            _st_label_390 += 1
            if False:
                _st_label_390 += 1
            else:
                super()._label('_st_label_390', block=True)
                _st_label_390 -= 1

    def _DBEmulator_handler_394(self, data, p):
        print(data)
        self.output('Response received!!')
        self._send(('DB_READ_RESPONSE', {'key': 'value1'}), p)
    _DBEmulator_handler_394._labels = None
    _DBEmulator_handler_394._notlabels = None

    def _DBEmulator_handler_419(self, data, p):
        print(data)
        self.output('Response received!!')
        self._send(('DB_WRITE_RESPONSE', {'key': 'value1'}), p)
    _DBEmulator_handler_419._labels = None
    _DBEmulator_handler_419._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_471, sources=[PatternExpr_478], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_470])])

    def setup(self, coord_ps):
        self._state.coord_ps = coord_ps
        print(self._state.coord_ps)

    def run(self):
        self._send(('DB_WRITE', {'key': 'value'}), self._state.coord_ps)
        self.output('Starting Application Instance')
        super()._label('_st_label_466', block=False)
        _st_label_466 = 0
        while (_st_label_466 == 0):
            _st_label_466 += 1
            if False:
                _st_label_466 += 1
            else:
                super()._label('_st_label_466', block=True)
                _st_label_466 -= 1

    def _ClientP_handler_470(self, data, p):
        print(data)
        self.output('Response received in client!!')
    _ClientP_handler_470._labels = None
    _ClientP_handler_470._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_502, sources=[PatternExpr_507], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_501])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_497', block=False)
        _st_label_497 = 0
        while (_st_label_497 == 0):
            _st_label_497 += 1
            if False:
                _st_label_497 += 1
            else:
                super()._label('_st_label_497', block=True)
                _st_label_497 -= 1

    def _SubCoordP_handler_501(self, p):
        self.output('Response received in sub process!!')
        self._send(('APP_EVALUATION_RESPONSE',), p)
    _SubCoordP_handler_501._labels = None
    _SubCoordP_handler_501._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_529, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_528])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_528(self):
        pass
    _ResCoordP_handler_528._labels = None
    _ResCoordP_handler_528._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_546, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_545])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_545(self):
        pass
    _WorkerP_handler_545._labels = None
    _WorkerP_handler_545._notlabels = None

class _NodeMain(da.DistProcess):

    def run(self):
        config_fpath = (sys.argv[1] if (len(sys.argv) > 1) else '../config/main-config.json')
        config = cfg.load_config(config_fpath)
        db_ps = da.new(DBEmulator, num=1)
        da.setup(db_ps, (config['db_config'], config['minDBlatency'], config['maxDBlatency']))
        da.start(db_ps)
        coord_ps = da.new(SubCoordP, num=config['num_coords'])
        da.setup(coord_ps, ())
        cli_ps = da.new(ClientP, num=config['num_clients'])
        da.setup(cli_ps, (db_ps,))
        da.start(coord_ps)
        da.start(cli_ps)
