from migen.flow.network import *
from migen.flow.transactions import *
from migen.actorlib.sim import *
from migen.pytholite.compiler import Pytholite
from migen.sim.generic import Simulator
from migen.fhdl import verilog

layout = [("r", 32)]

def number_gen():
	for i in range(10):
		yield Token("result", {"r": i})

class SimNumberGen(SimActor):
	def __init__(self):
		self.result = Source(layout)
		SimActor.__init__(self, number_gen())

def run_sim(ng):
	g = DataFlowGraph()
	d = Dumper(layout)
	g.add_connection(ng, d)
	
	c = CompositeActor(g)
	sim = Simulator(c)
	sim.run(30)
	del sim

def make_ng_pytholite():
	ng_pytholite = Pytholite(number_gen)
	ng_pytholite.result = Source(layout)
	ng_pytholite.finalize()
	return ng_pytholite

def main():
	print("Simulating native Python:")
	ng_native = SimNumberGen()
	run_sim(ng_native)
	
	print("Simulating Pytholite:")
	ng_pytholite = make_ng_pytholite()
	run_sim(ng_pytholite)
	
	print("Converting Pytholite to Verilog:")
	ng_pytholite = make_ng_pytholite()
	print(verilog.convert(ng_pytholite))

main()
