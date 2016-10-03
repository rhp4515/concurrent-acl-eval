
import da
PatternExpr_329 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_WRITE')])
PatternExpr_334 = da.pat.FreePattern('p')
PatternExpr_340 = da.pat.TuplePattern([da.pat.ConstantPattern('DB_READ')])
PatternExpr_345 = da.pat.FreePattern('p')
PatternExpr_373 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_RESPONSE'), da.pat.FreePattern('result')])
PatternExpr_380 = da.pat.FreePattern('p')
PatternExpr_400 = da.pat.TuplePattern([da.pat.ConstantPattern('APP_EVALUATION_REQUEST')])
PatternExpr_405 = da.pat.FreePattern('p')
PatternExpr_432 = da.pat.TuplePattern([])
PatternExpr_435 = da.pat.FreePattern('p')
PatternExpr_452 = da.pat.TuplePattern([])
PatternExpr_455 = da.pat.FreePattern('p')
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
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_0', PatternExpr_329, sources=[PatternExpr_334], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_328]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DBEmulatorReceivedEvent_1', PatternExpr_340, sources=[PatternExpr_345], destinations=None, timestamps=None, record_history=None, handlers=[self._DBEmulator_handler_339])])

    def setup(self, conf, minLatency, maxLatency):
        self._state.conf = conf
        self._state.minLatency = minLatency
        self._state.maxLatency = maxLatency
        self.output('SETTING UP DB')
        with open(self._state.conf, 'r') as f:
            db_data = f.read()
        json_content = json.loads(json.dumps(xmltodict.parse(db_data)))['db']
        json_data = json_content['data']
        self._state.employee = pd.read_json(json.dumps(json_data['employee']))
        self._state.bank = pd.read_json(json.dumps(json_data['bank']))
        self._state.movie = pd.read_json(json.dumps(json_data['movie']))
        json_schema = json_content['schema']
        emp_bank_hist_schema = json_schema['emp_bank_hist']['column']
        self._state.emp_bank_hist = pd.DataFrame([], columns=emp_bank_hist_schema)

    def run(self):
        print(self._state.employee)
        print(self._state.bank)
        print(self._state.movie)
        print(self._state.minLatency)
        print(self._state.maxLatency)
        print(self._state.emp_bank_hist)
        self.output('BUILDING DB')
        super()._label('_st_label_324', block=False)
        _st_label_324 = 0
        while (_st_label_324 == 0):
            _st_label_324 += 1
            if False:
                _st_label_324 += 1
            else:
                super()._label('_st_label_324', block=True)
                _st_label_324 -= 1

    def _DBEmulator_handler_328(self, p):
        pass
    _DBEmulator_handler_328._labels = None
    _DBEmulator_handler_328._notlabels = None

    def _DBEmulator_handler_339(self, p):
        pass
    _DBEmulator_handler_339._labels = None
    _DBEmulator_handler_339._notlabels = None

class ClientP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientPReceivedEvent_0', PatternExpr_373, sources=[PatternExpr_380], destinations=None, timestamps=None, record_history=None, handlers=[self._ClientP_handler_372])])

    def setup(self, coords):
        self._state.coords = coords
        pass

    def run(self):
        self.output('Starting Application Instance')
        self._send(('APP_EVALUATION_REQUEST',), self._state.coords)
        super()._label('_st_label_368', block=False)
        _st_label_368 = 0
        while (_st_label_368 == 0):
            _st_label_368 += 1
            if False:
                _st_label_368 += 1
            else:
                super()._label('_st_label_368', block=True)
                _st_label_368 -= 1

    def _ClientP_handler_372(self, result, p):
        self.output('Response received!!')
    _ClientP_handler_372._labels = None
    _ClientP_handler_372._notlabels = None

class SubCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_SubCoordPReceivedEvent_0', PatternExpr_400, sources=[PatternExpr_405], destinations=None, timestamps=None, record_history=None, handlers=[self._SubCoordP_handler_399])])

    def setup(self):
        pass

    def run(self):
        super()._label('_st_label_395', block=False)
        _st_label_395 = 0
        while (_st_label_395 == 0):
            _st_label_395 += 1
            if False:
                _st_label_395 += 1
            else:
                super()._label('_st_label_395', block=True)
                _st_label_395 -= 1

    def _SubCoordP_handler_399(self, p):
        self.output(p)
        self.output('RECEIVED_REQUEST')
        self._send(('APP_EVALUATION_RESPONSE', True), p)
        self.output('SENT_RESPONSE')
    _SubCoordP_handler_399._labels = None
    _SubCoordP_handler_399._notlabels = None

class ResCoordP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ResCoordPReceivedEvent_0', PatternExpr_432, sources=[PatternExpr_435], destinations=None, timestamps=None, record_history=None, handlers=[self._ResCoordP_handler_431])])

    def setup(self):
        pass

    def run(self):
        pass

    def _ResCoordP_handler_431(self, p):
        pass
    _ResCoordP_handler_431._labels = None
    _ResCoordP_handler_431._notlabels = None

class WorkerP(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerPReceivedEvent_0', PatternExpr_452, sources=[PatternExpr_455], destinations=None, timestamps=None, record_history=None, handlers=[self._WorkerP_handler_451])])

    def setup(self):
        pass

    def run(self):
        pass

    def _WorkerP_handler_451(self, p):
        pass
    _WorkerP_handler_451._labels = None
    _WorkerP_handler_451._notlabels = None

class _NodeMain(da.DistProcess):

    def run(self):
        config_fpath = (sys.argv[1] if (len(sys.argv) > 1) else '../config/main-config.json')
        config = cfg.load_config(config_fpath)
        db_ps = da.new(DBEmulator, num=1)
        da.setup(db_ps, (config['db_config'], config['minDBlatency'], config['maxDBlatency']))
        da.start(db_ps)
