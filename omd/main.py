
from __future__ import print_function
import sys
import pyomd
import datetime

class MyCallback (pyomd.PythonOutputCallback):
	
	def __init__(self):
		pyomd.PythonOutputCallback.__init__(self)
	
	def process_symbol_name(self, symbol_name):
		print("Processing symbol ", symbol_name)
		self.symbol_ = symbol_name
	
	def process_callback_label(self, callback_label):
		print("Processing process_callback_label ", callback_label)
	
	def process_tick_descriptor(self, tick_descriptor):
		print("Processing tick descriptor")
		self.desc_ = pyomd.TickDescriptor(tick_descriptor)
	
	def process_event(self, tick, time):
		print(self.symbol_, " ", time, " ")
		n = self.desc_.get_num_of_fields()
		for i in range(0, int(n)):
			field = self.desc_.get_field(i)
			if field.get_type() != pyomd.DataType.TYPE_STRING:
				print(tick.get_double(i), " ")
			
	#	print("\n")
	
	def done(self):
		print("Done ", self.symbol_)
	
	def process_error(self, error_code, error_msg):
		print("Processing error: ", error_msg)
	
	def replicate(self):
		# Important: You need to call __disown__() here to avoid object be deleted py python,
		# the SWIG/C++ will take care to delete this object.
		return MyCallback().__disown__()
	

class main:
	
	def start(self, input_argv):
		context = "DEFAULT";
		if len(input_argv) > 1:
			context = input_argv[1]
		
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "The context is " + context)
		#print(context)
		
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Starting python test...")
		dbs = pyomd.DbInfo.get_all_databases(context)
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Databases are loaded...")
		conn = pyomd.Connection()
		conn.connect(context)
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Connection succeeded...")
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Enumerating the known OneTick databases...")
		#print("Enumerating the known OneTick databases...")
		for db in dbs:
			name = db.get_db_name()
			pyomd.Logger.log(pyomd.Logger.INFO_MSG, name)
			#print(name)
			
			if name == "DEMO_L1":
				pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Printing some sample symbols from DEMO_L1 database...")
				symbols = db.get_all_symbols(conn, 20031201)
				for j in range (1, 10):
					pyomd.Logger.log(pyomd.Logger.INFO_MSG, symbols[j])
					#print(symbols[j])
			
		begtime = datetime.datetime(2003, 12, 1, 14, 30, 0)
		endtime = datetime.datetime(2003, 12, 1, 14, 31, 30, 45)
		symbols = pyomd.StringCollection()

		symbols.push_back("DEMO_L1::A")
		
		queries = pyomd.StringCollection()
		queries.push_back("VWAP;TRD")
		
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Creating callback object...")
		cb = MyCallback()
		
		#print(isinstance(cb, pyomd.PythonOutputCallback))
		
		cb.set_callback_label("Label")
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Running a chain query...")
		pyomd.RequestGroup.process_chain_queries(symbols, queries, begtime, endtime, cb, conn, 20031201)
		
		graph = pyomd.Graph()
		group = pyomd.RequestGroup()
		
		eventproc = graph.add_root("PASSTHROUGH", cb)
		eventproc.bind_tick_type("TRD")
		
		prevproc = eventproc.add_source("VALUE_COMPARE", "a")
		prevproc.set_parameter("FIELD", "SIZE")
		prevproc.set_parameter("VALUE", "1000")
		prevproc.set_parameter("RELATIONSHIP_TO_CONST", "GE")
		
		symbols = pyomd.StringCollection()
		symbols.push_back("DEMO_L1::AA")
		symbols.push_back("DEMO_L1::AAA")
		
		group.add_requests(symbols, graph, begtime, endtime, 20031201)
		
		pyomd.Logger.log(pyomd.Logger.INFO_MSG, "Running a graph query...")
		group.process_requests(conn)
	

try:
	sys.stdout = open('output.txt', 'w')
	lib = pyomd.OneTickLib(None)
	start_ob = main()
	start_ob.start(sys.argv)
except pyomd.OneTickException as err:
	print("OneTickException : ", format(err))
except NameError as err:
	print("NameError: ", format(err))
except NotImplementedError as err:
	print("NotImplementedError : ", format(err))
except AttributeError as err:
	print("AttributeError : ", format(err))
except:
	print("Unexpected error:", sys.exc_info()[0])
	
