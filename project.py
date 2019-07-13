import sys
import math
import random
import time
from randomGenerator import Rand48
from fcfs import fcfs
from rr import rr

''' The project will implement a rudimentary simulation of an operating system, focusing on 
    processes, assumed to be resident in memory, waiting to use the CPU. The processes will 
    mimic the READY, RUNNING, and BLOCKED states associated with CPU activity. The algorithms 
    hat will be implemented are: 
    	- First Come First Served (FCFS) 
    	- Shortest Job First (SJF)
    	- Shortest Remaining Time (SRT) 
    	- Round Robin (RR).
'''

''' Function generates the burst_time value and/or I/O time value for each burst
'''
def burst_and_io_generator(lambda_value, upper_bound, burst_or_io_list, generator):

	random_number = generator.drand48()
	burst_time_value = math.ceil(-math.log(random_number) / lambda_value)

	# Skip burst times that exceed upper bound
	while burst_time_value > upper_bound:
		random_number = generator.drand48()
		burst_time_value = math.ceil(-math.log(random_number) / lambda_value)

	burst_or_io_list.append(burst_time_value)


''' Main Function
'''
def main():

	# Error handling for the arguments
	print(len(sys.argv))
	if len(sys.argv) != 8 and len(sys.argv) != 9:
		print("ERROR: Incorrect number of arguments!\r", file=sys.stderr)
		sys.exit()

	try:
		# Seed for the random number generator to determine the interarrival times of CPU bursts.
		number_generator_seed = int(sys.argv[1])

		# Lambda value that determines average value generated for interarrival times
		# 	(with exponential distribution).
		lambda_value = float(sys.argv[2])

		# Upper-bound for valid pseudo-random values (will skip values greater than upper bound).
		upper_bound = int(sys.argv[3])

		# Number of processes to simulate.
		# Process IDs are assigned in alphabetical order A through Z, therefore atmost there will
		#	be 26 processes to simulate.
		number_simulations = int(sys.argv[4])

		# Time (in milliseconds) it takes to perform a context switch.
		context_switch_time = int(sys.argv[5])

		# For SJF and SRT, we cannot know the actual CPU burst times beforehand, so we will make
		# 	an estimate determined via exponential averaging (using "ceiling" function).
		alpha_value = float(sys.argv[6])

		# For the RR algoorithm, we need to define the time slice value (in milliseconds).
		time_slice = int(sys.argv[7])
	except ValueError:
		print("ERROR: Improper arguments were given!\r", file = sys.stderr)
		sys.exit()

	# For the RR algorithm, we define whether processes or added to the beginning or end of
	#	the ready queue when they arrive or complete I/O.
	# Value should be set to BEGINNING or END, with END being the default behavior.
	if len(sys.argv) > 8:
		queue_addition = sys.argv[8]
	else:
		queue_addition = "END"

	# List that contains all of the stimulations
	processes = []

	# List that contains the amount of bursts for each of the processes
	bursts = []

	# List of lists that contains the burst times each burst in each process
	burst_times = [] 

	# List of lists that contains the I/O times for each burst in each process
	io_times = []

	# Initiating the generator with srand48
	generator = Rand48(number_generator_seed)
	generator.srand48()

	i = 0
	while i < number_simulations:
		# Adding the arrival times for each process
		random_number = generator.drand48()
		arrival_time = math.floor(-math.log(random_number) / lambda_value)

		# Skip arrival times that exceed upper bound
		if arrival_time > upper_bound:
			continue
		else:
			# Store the arrival time if it does not exceed upper bound
			processes.append(arrival_time)

			# Adding the number of bursts needed for each process
			random_number = generator.drand48()

			# Skip bursts that exceed upper bound
			while  math.floor(random_number * 100) + 1 > upper_bound:
				random_number = generator.drand48()

			bursts.append(math.floor(random_number * 100) + 1)

			temp_burst = []
			temp_io = []

			# For each burst of a process, generate a burst time  and an I/O time
			for j in range(0, bursts[len(bursts)-1]):
				# Last burst does not have an I/O, so just generate a burst time
				if j == bursts[len(bursts)-1] - 1:
					burst_and_io_generator(lambda_value, upper_bound, temp_burst, generator)
					continue
				else:
					# Generating burst time values
					burst_and_io_generator(lambda_value, upper_bound, temp_burst, generator)

					# Generating I/O values
					burst_and_io_generator(lambda_value, upper_bound, temp_io, generator)

			burst_times.append(temp_burst)
			io_times.append(temp_io)

		i += 1

	print("PROCESSES ARRIVALS")
	print(processes)
	print()
	print("BURSTS")
	print(bursts)
	print()
	print("BURST TIMES")
	print(burst_times)
	print()
	print("I/O TIMES")
	print(io_times)
	print()

	fcfs(processes, bursts, burst_times, io_times, context_switch_time)
	# rr(processes, bursts, burst_times, io_times, context_switch_time, time_slice, queue_addition)


if __name__== "__main__":
	main()