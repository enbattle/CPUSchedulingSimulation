import sys
import math
import random
import time
from randomGenerator import Rand48
from fcfs import fcfs

''' The project will implement a rudimentary simulation of an operating system, focusing on 
    processes, assumed to be resident in memory, waiting to use the CPU. The processes will 
    mimic the READY, RUNNING, and BLOCKED states associated with CPU activity. The algorithms 
    hat will be implemented are: 

    	- First Come First Served (FCFS) 
    	- Shortest Job First (SJF)
    	- Shortest Remaining Time (SRT) 
    	- Round Robin (RR).
'''

''' OUTPUT02
	Process A [NEW] (arrival time 9 ms) 16 CPU bursts

	OUTPUT03
	Process A [NEW] (arrival time 9 ms) 16 CPU bursts
	Process B [NEW] (arrival time 18 ms) 21 CPU bursts

	OUTPUT04
	Process A [NEW] (arrival time 9 ms) 16 CPU bursts
	Process B [NEW] (arrival time 18 ms) 21 CPU bursts
	Process C [NEW] (arrival time 42 ms) 4 CPU bursts
	Process D [NEW] (arrival time 156 ms) 11 CPU bursts
	Process E [NEW] (arrival time 134 ms) 55 CPU bursts
	Process F [NEW] (arrival time 106 ms) 34 CPU bursts
	Process G [NEW] (arrival time 65 ms) 80 CPU bursts
	Process H [NEW] (arrival time 11 ms) 83 CPU bursts
	Process I [NEW] (arrival time 68 ms) 77 CPU bursts
	Process J [NEW] (arrival time 0 ms) 10 CPU bursts
	Process K [NEW] (arrival time 7 ms) 13 CPU bursts
	Process L [NEW] (arrival time 189 ms) 7 CPU bursts
	Process M [NEW] (arrival time 16 ms) 48 CPU bursts
	Process N [NEW] (arrival time 122 ms) 31 CPU bursts
	Process O [NEW] (arrival time 29 ms) 31 CPU bursts
	Process P [NEW] (arrival time 159 ms) 16 CPU bursts

	OUTPUT05
	Process A [NEW] (arrival time 102 ms) 85 CPU bursts
	Process B [NEW] (arrival time 365 ms) 6 CPU bursts
	Process C [NEW] (arrival time 246 ms) 95 CPU bursts
	Process D [NEW] (arrival time 388 ms) 57 CPU bursts
	Process E [NEW] (arrival time 1515 ms) 83 CPU bursts
	Process F [NEW] (arrival time 1684 ms) 97 CPU bursts
	Process G [NEW] (arrival time 669 ms) 1 CPU burst
	Process H [NEW] (arrival time 376 ms) 49 CPU bursts

'''

''' Function generates the burst_time value and/or I/O time value for each burst
'''
def burst_and_io_generator(i, lambda_value, upper_bound, burst_or_io_list, generator):

	random_number = generator.drand48()
	burst_time_value = math.ceil(-math.log(random_number) / lambda_value)

	# Skip burst times that exceed upper bound
	while burst_time_value > upper_bound:
		random_number = generator.drand48()
		burst_time_value = math.ceil(-math.log(random_number) / lambda_value)

	burst_or_io_list[i].append(burst_time_value)


''' Main Function
'''
def main():
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

	# For the RR algorithm, we define whether processes or added to the beginning or end of
	#	the ready queue when they arrive or complete I/O.
	# Value should be set to BEGINNING or END, with END being the default behavior.
	if len(sys.argv) > 8:
		queue_addition = sys.argv[8]
	else:
		queue_addition = "END"

	# List that contains all of the stimulations
	processes = [0] * number_simulations

	# List that contains the amount of bursts for each of the processes
	bursts = [0] * number_simulations

	# List of lists that contains the burst times each burst in each process
	burst_times = [[]] * number_simulations

	# List of lists that contains the I/O times for each burst in each process
	io_times = [[]] * number_simulations

	# Initiating the generator with srand48
	generator = Rand48(number_generator_seed)
	generator.srand48()

	for i in range(0, number_simulations):
		# Adding the arrival times for each process
		random_number = generator.drand48()
		arrival_time = math.floor(-math.log(random_number) / lambda_value)
		processes[i] = arrival_time

		# Skip arrival times that exceed upper bound
		if arrival_time > upper_bound:
			print(upper_bound)
			i-=1
			continue
		else:
			# Adding the number of bursts needed for each process
			random_number = generator.drand48()

			# Skip bursts that exceed upper bound
			while  math.floor(random_number * 100) + 1 > upper_bound:
				random_number = generator.drand48()

			bursts[i] = math.floor(random_number * 100) + 1

			# For each burst of a process, generate a burst time  and an I/O time
			for j in range(0, bursts[i]):
				# Last burst does not have an I/O, so just generate a burst time
				if j == bursts[i] - 1:
					burst_and_io_generator(i, lambda_value, upper_bound, burst_times, generator)
					continue
				else:
					# Generating burst time values
					burst_and_io_generator(i, lambda_value, upper_bound, burst_times, generator)

					# Generating I/O values
					burst_and_io_generator(i, lambda_value, upper_bound, io_times, generator)


	print(processes)
	print(bursts)
	print(burst_times)
	print(io_times)


if __name__== "__main__":
	main()