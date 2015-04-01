import multiprocessing
from weppyweb.commands import schedule, _q_default


s = multiprocessing.Process(target=schedule)
q0 = multiprocessing.Process(target=_q_default)

try:
    s.start()
    q0.start()
except:
    s.terminate()
    q0.terminate()
