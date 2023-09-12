'''
	 OtqQueryExample.py

This example illustrates how to construct, modify and evaluate
the query from the existing OTQ file. And also shows how to use QueryCancellationHandle
to cancel running queries.

Command line arguments:
	-otq_file          - Name of one tick query file.
	-context           - Context name. Database name is looked up in this context.
	-symbol_file       - Name of file that contain list of symbols to query. Individual symbols can be commented out by #. 
	-symbol            - Space separated list of symbols to query. 
	-symbol_date       - Date when queried securities had the specified names in form YYYYMMDD.
	-start             - Start time of the query in form YYYYMMDDhhmmss.
	-end               - End time of the query in form YYYYMMDDhhmmss.
	-timezone          - Timezone of start and end time. Output times also will be shown in this timezone.
	-apply_times_daily - If 'true', invoke the query multiple times, once for each day. 
	-running_query     - If 'true', specified that the query is running. 
	-param             - Space separated list of name/value pairs for otq variables. 
	-timeout           - Timeout in milliseconds
	
To illustrate query cancellation one needs to run queries agains remote Tick Server.
'''
from __future__ import print_function
import sys
import threading
import datetime
import time
import pyomd
import ExampleUtil
import InfoCallback

class RequestCancellation (threading.Thread):
	
	def __init__(self, h, t):
		threading.Thread.__init__(self)
		self.handle = h
		self.timeout = t
		self.interrupted = False
	
	def setSubscriptionId(self, conn, id):
	    self.connection = conn
	    self.subscription_id = id
	
	def run(self):
		try :
			
			# There is no way to kill this thread, so we check whether thread is interrupted to exit
			i = 0;
			while (False == self.interrupted) and (i < self.timeout):
				i += 5
				time.sleep(5)
			
			if self.interrupted:
				print("Exiting with Interruption.")
				return 
			
			if (self.subscription_id != None) and (len(self.subscription_id) != 0):
			    print("Cancelling query with subscription id:" + str(self.subscription_id))
			    pyomd.RequestGroup.cancel_running_query(self.connection, self.subscription_id)
			else:
				print("Cancelling query using handle: ", self.handle)
				self.handle.cancel_query()
		except Exception as err :
			print ("Exception happened in Cancellation thread: ", format(err))

		print("Exiting Canceller.")
	
	def interrupt(self):
		self.interrupted = True
	

class OtqQueryExample:
	
	def otqExample(self, options):
		'''Construct,modify and evaluate the query from the existing OTQ file.'''
		print("Options:")
		
		# Connect to context as logged in user. "DEFAULT" context is used if not set in command line. 
		context = options.getValue("context", 0, "DEFAULT")
		print("context = " + context)
		
		# Create object to evaluate query from OTQ file
		otq_file = options.getValue("otq_file")
		print("otq_file = " + str(otq_file));
		otq_query = pyomd.OtqQuery(otq_file)
		
		# Processing symbols
		symbols = pyomd.StringCollection()
		
		# From command line
		symbol_count = options.getParam("symbol", False)
		if symbol_count > 0 :
			print("symbol = "),
			for i in range(0, symbol_count):
				symbol_i = options.getValue("symbol", i)
				symbols.push_back(symbol_i)
				print (symbol_i, " "),
			print("")
		
		# From symbol file
		value = options.getValue("symbol_file", 0, "");
		if len(value) != 0 :
			print("symbol_file = " + value)
			file = open(value, 'r')
			for symbol in file:
				symbol = symbol.rstrip('\n')
				if symbol[0] != '#':
					symbols.push_back(symbol)
			file.close()
		
		if len(symbols) != 0 :
			otq_query.set_symbols(symbols);
		
		# Processing symbol date
		value = options.getValue("symbol_date", 0, "")
		if len(value) != 0:
			print("symbol_date = " + value)
			symbol_date = int(value)
			otq_query.set_symbol_date(symbol_date)
		
		# Processing start and end time
		timezone = options.getValue("timezone",0,"UTC")
		print("timezone = " + timezone)
		value = options.getValue("start", 0, "")
		if len(value) != 0:
			print("start = " + value)
			d = ExampleUtil.YYYMMDDhhmmss2Date(value, timezone)
			otq_query.set_start_time(d)
		
		value = options.getValue("end", 0, "")
		if len(value) != 0:
			print("end = " + value)
			d = ExampleUtil.YYYMMDDhhmmss2Date(value, timezone)
			otq_query.set_end_time(d)
		
		# Processing "apply_times_daily" option
		value = options.getValue("apply_times_daily", 0, "")
		if len(value) != 0:
			if value.lower() == "true" :
				print("apply_times_daily = True")
				otq_query.set_apply_times_daily_flag(True, timezone)
	        
			elif value.lower() == "false" :
				print("apply_times_daily = False")
				otq_query.set_apply_times_daily_flag(False, timezone)
			else:
				raise ExampleUtil.OmdExampleException("Invalid value " + str(value) + " for option apply_times_daily")
			
		# Processing "running query" option
		value = options.getValue("running_query", 0, "")
		if len(value) != 0 :
			running_query_properties = pyomd.RunningQueryProperties()
			if value.lower() == "true":
				print("running_query = True")
				otq_query.set_running_query_properties(True,running_query_properties)
			elif value.lower() == "false" :
				print("running_query = False")
				otq_query.set_running_query_properties(False, running_query_properties)
			else :
				raise ExampleUtil.OmdExampleException("Invalid value " + str(value) + " for option running_query")
		
		# Processing query parameters
		n_val = options.getParam("param", False)
		if n_val > 0 :
			print("param ="),
			params = pyomd.otq_parameters_t()
			for i in range(0, n_val) :
				value = options.getValue("param", i)
				param = value.split("=")
				if len(param) == 2:
					params.set(param[0], param[1])
					print(" " + str(param[0]) + "=" + str(param[1])),
				else:
					raise ExampleUtil.OmdExampleException("Invalid value " + str(value) + " for option param");
			
			otq_query.set_otq_parameters(params)
			print("")
		
		# Processing timeout
		value = options.getValue("timeout", 0, "")
		timeout = 0
		if len(value) != 0 :
			print("timeout = " + value)
			timeout = int(value)
		
		
		conn = pyomd.Connection()
		conn.connect(context)
		
		# Create user callback object
		cb = InfoCallback.InfoCallback(timezone)
		
		# Evaluate query
		print("Starting query evaluation")
		
		if timeout > 0 :
			request_groups_with_tip = pyomd.RequestGroupsWithTIP()
			otq_query.parse(conn)
			otq_query.extract_queries(request_groups_with_tip, cb)
			
			r_group_count = len(request_groups_with_tip)
			print ("RequestGroup count = ", r_group_count)
			for i in range(0, r_group_count):
				request_group_with_tip = request_groups_with_tip[i]
				request_group = request_group_with_tip.get_request_group()
				time_interval_prop = request_group_with_tip.get_time_interval_properties()
				
				ch = pyomd.QueryCancellationHandle.create_instance()
				req_cancel = RequestCancellation(ch, timeout)
				if time_interval_prop.get_running_query_flag :
				    subscription_id = time_interval_prop.get_running_query_properties().get_subscription_id()
				    print("subscription_id = " + subscription_id)
				    req_cancel.setSubscriptionId(conn, subscription_id)
				
				req_cancel.start()
				request_group.process_requests(conn, ch, time_interval_prop)
				
				if req_cancel.is_alive():
					req_cancel.interrupt()
				
				pyomd.QueryCancellationHandle.destroy_instance(ch)
			
		else :
			pyomd.RequestGroup.process_otq_file(otq_query, cb, conn)
	
	def usage():
		'''Print out available command line arguments.'''
		print("Usage: otq_example.exe OPTION ...\n" 
		+ "  -otq_file <otq_file_name>\n"
		+ "  [-context <context_name>]\n"
		+ "  [-symbol_file <symbol file>]\n"
		+ "  [-symbol	<symbol1 symbol2 ...>]\n"
		+ "  [-symbol_date <YYYYMMDD>]\n"
		+ "  [-param <name1=value1 name2=value2 ...>]\n"
		+ "  [-start <YYYYMMDDhhmmss>]\n"
		+ "  [-end <YYYYMMDDhhmmss\n"
		+ "  [-timezone <timezone_name>]\n"
		+ "  [-apply_times_daily <true/false>]\n"
		+ "  [-running_query <true/false>]\n"
		+ "  [-timeout <timeout in milliseconds>\n"
		+ "  [-help]\n"
		+ "All optional parameters are taken from OTQ file if not set\n")
	
	
'''Defines the entry point for the console application.'''
try :
	omdlib = pyomd.OneTickLib(None)
	example = OtqQueryExample()
	options = ExampleUtil.CmdLine(sys.argv)
	
	# Processing help option
	if options.getParam("help", 0) >= 0:
		raise ExampleUtil.OmdExampleException("")
	
	example.otqExample(options)
except ExampleUtil.OmdExampleException as error :
	print("ExampleUtil.OmdExampleException was thrown: ", format(error))
	OtqQueryExample.usage()
except pyomd.OneTickException as error:
	print("OneTickException was thrown: ",format(error))
except Exception as error:
	print("Exception was thrown: ", format(error));

