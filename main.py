import sys
import math
import random
from randomGenerator import srand48, drand48

''' The project will implement a rudimentary simulation of an operating system, focusing on 
    processes, assumed to be resident in memory, waiting to use the CPU. The processes will 
    mimic the READY, RUNNING, and BLOCKED states associated with CPU activity. The algorithms 
    hat will be implemented are: 

    	- First Come First Served (FCFS) 
    	- Shortest Job First (SJF)
    	- Shortest Remaining Time (SRT) 
    	- Round Robin (RR).
'''

def main():
	# Seed for the random number generator to determine the interarrival times of CPU bursts.
	number_generator_seed = sys.argv[1]

	# Lambda value that determines average value generated for interarrival times
	# 	(with exponential distribution).
	lambda_value = sys.argv[2]

	# Upper-bound for valid pseudo-random values (will skip values greater than upper bound).
	upper_bound = sys.argv[3]

	# Number of processes to simulate.
	# Process IDs are assigned in alphabetical order A through Z, therefore atmost there will
	#	be 26 processes to simulate.
	number_simulations = sys.argv[4]

	# Time (in milliseconds) it takes to perform a context switch.
	context_switch_time = sys.argv[5]

	# For SJF and SRT, we cannot know the actual CPU burst times beforehand, so we will make
	# 	an estimate determined via exponential averaging (using "ceiling" function).
	alpha_value = sys.argv[6]

	# For the RR algoorithm, we need to define the time slice value (in milliseconds).
	time_slice = sys.argv[7]

	# For the RR algorithm, we define whether processes or added to the beginning or end of
	#	the ready queue when they arrive or complete I/O.
	# Value should be set to BEGINNING or END, with END being the default behavior.
	if len(sys.argv) > 8:
		queue_addition = sys.argv[8]
	else:
		queue_addition = "END"



if __name__== "__main__":
	main()