import bppy as bp
from bppy.model.sync_statement import *
from bppy.model.b_thread import *
from math import ceil, log2

class EvaluatorListener(bp.PrintBProgramRunnerListener):
	def starting(self, b_program):
		self.events = []
	def ended(self, b_program):
		pass
	def event_selected(self, b_program, event):
		self.events.append(event.name)
		if len(self.events) == 50:
			raise TimeoutError()

def generate_model(n=6, mode=bp.execution_thread):
    @mode
    def node(u, x):
        while True:
          yield sync(waitFor=bp.BEvent(f'n{u}_{x}'))
          if u >= n:
            # last layer
            if (x >= n):
              yield sync(request=bp.BEvent(f'n{u-n}_{x%n}'))
            else:
              yield sync(request=bp.BEvent(f'result_{x}'))
          else:
            # inner node
            flip = yield choice({0:0.5, 1:0.5})
            yield sync(request=bp.BEvent(f'n{u*2}_{2*x+flip}'))

    @mode
    def start():
        yield sync(request=bp.BEvent(f'n1_0'))

    d = 1
    nodes = []
    while d > 0 and (d, 0) not in nodes:
        nodes = nodes + [(d*(2**u), x) for u in range(ceil(log2(n/d))+1) for x in range(d*(2**u))]
        d = nodes[-1][0] - n

    bp_gen = lambda: bp.BProgram(bthreads=[node(*vertex) for vertex in nodes]+[start()],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy(),
                             listener=EvaluatorListener())
    event_list = [bp.BEvent(f'n{u}_{x}') for u, x in nodes] + [bp.BEvent(f'result_{x}') for x in range(n)]
    return bp_gen, event_list

