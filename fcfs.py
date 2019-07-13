import sys
import math
import random

# Printing the current status of the queue
def print_queue(queue):
	current_queue = ""

	if len(queue) == 0:
		current_queue += "<empty>"
	else:
		for i in range(0, len(queue)):
			if i == len(queue) - 1:
				current_queue += queue[i]
			else:
				current_queue += queue[i] + " "

	return current_queue

# Check if the CPU has finished a burst
def check_CPU_burst(time, current_process, queue, sorted_processes_by_number, bursts, io_queue, io_times, context_switch_time):
	# Decrease burst counter by 1 of the current process
	bursts[sorted_processes_by_number[current_process]] -= 1

	# Print process termination if burst counter is 0
	# Otherwise, print amount of bursts left and next I/O completion
	if bursts[sorted_processes_by_number[current_process]] == 0:
		print("time {}ms: Process {} terminated [Q {}]\r"
				.format(time, current_process, print_queue(queue)))
	else:
		if bursts[sorted_processes_by_number[current_process]] == 1:
			print("time {}ms: Process {} completed a CPU burst; {} burst to go [Q {}]\r"
				.format(time, current_process, bursts[sorted_processes_by_number[current_process]], 
				print_queue(queue)))
		else:
			print("time {}ms: Process {} completed a CPU burst; {} bursts to go [Q {}]\r"
				.format(time, current_process, bursts[sorted_processes_by_number[current_process]], 
				print_queue(queue)))

		current_io = io_times[sorted_processes_by_number[current_process]].pop(0)
		current_io += time + context_switch_time//2

		print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]\r"
			.format(time, current_process, current_io, print_queue(queue)))

 		# Add I/O completion to the I/O queue, and sort it
		io_queue.append((current_io, current_process))
		io_queue.sort()


# Check for I/O burst completion
def check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times):
	temp_io_queue = []

	for i in range(0, len(io_queue)):
		if io_queue[i][0] == time:
			temp_io_queue.append(io_queue[i])
			queue.append(io_queue[i][1])

			print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]\r"
				.format(time, io_queue[i][1], print_queue(queue)))

			temporary_wait_times[sorted_processes_by_number[io_queue[i][1]]] = time

		else:
			continue

	# Remove finished I/O bursts from queue
	if temp_io_queue:
		for i in range(0, len(temp_io_queue)):
			io_queue.remove(temp_io_queue[i])

def check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times):
	# Process arrives and is added to the queue
	queue.append(sorted_processes_by_time[processes[process_counter]])
	temporary_wait_times[sorted_processes_by_number[sorted_processes_by_time[processes[process_counter]]]] = time

	print("time {}ms: Process {} arrived; added to ready queue [Q {}]\r"
		.format(time, sorted_processes_by_time[processes[process_counter]], print_queue(queue)))

def fcfs(some_processes, some_bursts, some_burst_times, some_io_times, context_switch_time):
	processes = some_processes.copy()
	bursts = some_bursts.copy()
	burst_times = some_burst_times.copy()
	io_times = some_io_times.copy()

	process_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", 
						"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

	# Variables used to calculate FCFS statistics
	total_burst_time = 0
	total_wait_times = dict()
	total_turnaround_times = dict()
	total_context_switches = 0

	# FCFS statistics calculations
	total_bursts_completed = sum(bursts)
	temporary_wait_times = [0] * len(processes)
	temporary_turnaround_times = [0] * len(processes)
	
	# Overall time for the process
	time = 0
	CPU_in_use = False

	# Check which process we are on, current process burst occurring, and next burst/io completion
	process_counter = 0
	current_process = 0
	current_burst = 0
	current_io = 0
	next_burst_completion = 0

	# Queue that holds all of the current processes
	# Queue that holds current I/O bursts
	queue = []
	io_queue = []

	# Checking for context switches
	initial_switch = False
	after_switch = False

	# Sorted dictionary with arrival times as keys and the process letter as values
	sorted_processes_by_time = dict()
	sorted_processes_by_number = dict()

	# Print out all of the initial processes, their arrival times, and CPU bursts
	for i in range(0, len(processes)):
		if bursts[i] == 1:
			print("Process {} [NEW] (arrival time {} ms) {} CPU burst\r".format(process_names[i], 
			processes[i], bursts[i]))
		else:
			print("Process {} [NEW] (arrival time {} ms) {} CPU bursts\r".format(process_names[i], 
			processes[i], bursts[i]))
		sorted_processes_by_time[processes[i]] = process_names[i]
		sorted_processes_by_number[process_names[i]] = i

	# List of processes sorted by arrival times
	processes = list(sorted(sorted_processes_by_time.keys()))

	# Print out that the simulator stated for FCFS
	print("time {}ms: Simulator started for FCFS [Q {}]\r".format(time, print_queue(queue)))

	# While there are still bursts left, keep running processes
	while sum(bursts) != 0:
		# Check for CPU burst completion (CPU is free for next process)
		# (Also check if process has terminated with last CPU burst)
		if time == next_burst_completion and time != 0:

			# CPU burst completion function
			check_CPU_burst(time, current_process, queue, sorted_processes_by_number, bursts, io_queue, io_times, context_switch_time)

			# Add first half of context switch time to remove the process
			# Also check for processes that may finish in between the addition of context switch time
			temp_num = 0
			while temp_num < context_switch_time//2:

				# # Track the queue wait times for multiple processes
				# if queue:
				# 	for i in range(0, len(queue)):
				# 		temporary_wait_times[sorted_processes_by_number[queue[i]]] += 1

				# Check for I/O burst completion since theres a 2 second context_switch
				if io_queue:
					check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function				
						check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times)

						process_counter += 1

				time += 1
				temp_num += 1
				temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

			after_switch = True

			# Add turnaround times to appropriate list
			if current_process in total_turnaround_times:
				total_turnaround_times[current_process].append(temporary_turnaround_times[sorted_processes_by_number[current_process]])
				temporary_turnaround_times[sorted_processes_by_number[current_process]] = 0
			else:
				temp_list = []
				temp_list.append(temporary_turnaround_times[sorted_processes_by_number[current_process]])
				total_turnaround_times[current_process] = temp_list
				temporary_turnaround_times[sorted_processes_by_number[current_process]] = 0

			# Check for context switch (for statistics) and reset booleans for next context switch
			if initial_switch and after_switch:
				total_context_switches += 1

				initial_switch = False
				after_switch = False

		 	# CPU is now freed
			CPU_in_use = False

		# # Track the queue wait times for multiple processes
		# if queue:
		# 	for i in range(0, len(queue)):
		# 		temporary_wait_times[sorted_processes_by_number[queue[i]]] += 1

		# Check for I/O burst completion
		if io_queue:
			# I/O burst completion function
			check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times)

		# Check for process arrivals
		if process_counter != len(processes):
			if time == processes[process_counter]:

				# Process arrival function				
				check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times)

				process_counter += 1

		# IF CPU is not in use, start running a process
		if CPU_in_use == False and len(queue) != 0:
			# Run first process in the queue (First Come, First Serve)
			current_process = queue.pop(0)

			# Add queue wait times to appropriate list
			if current_process in total_wait_times:
				total_wait_times[current_process].append(time - temporary_wait_times[sorted_processes_by_number[current_process]])
				temporary_wait_times[sorted_processes_by_number[current_process]] = 0
			else:
				temp_list = []
				temp_list.append(time - temporary_wait_times[sorted_processes_by_number[current_process]])
				total_wait_times[current_process] = temp_list
				temporary_wait_times[sorted_processes_by_number[current_process]] = 0

			# Add second half of context switch time to bring in the process
			# Also check for processes that may finish in between the addition of context switch time
			temp_num = 0
			while temp_num < context_switch_time//2:

				# # Track the queue wait times for multiple processes
				# if queue:
				# 	for i in range(0, len(queue)):
				# 		temporary_wait_times[sorted_processes_by_number[queue[i]]] += 1

				# Check for I/O burst completion since theres a 2 second context_switch
				if io_queue:
					check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function				
						check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, temporary_wait_times)

						process_counter += 1 

				time += 1
				temp_num += 1
				temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

			initial_switch = True

			# Pop the next burst time for the process and check for next burst completion time
			current_burst = burst_times[sorted_processes_by_number[current_process]].pop(0)
			next_burst_completion = time + current_burst

			# Add burrent burst time to total burst time (to calculate statistic)
			# Increment number of bursts completed
			total_burst_time += current_burst

			print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]\r"
				.format(time, current_process, current_burst, print_queue(queue)))

			# Check for I/O burst completion since theres a 2 second context_switch
			if io_queue:
				check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times)

			# Check for process arrivals since there is a 2 second context_switch
			if process_counter != len(processes):
				if time == processes[process_counter]:

					# Process arrival function				
					check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, temporary_wait_times)

					process_counter += 1

			# CPU now in use
			CPU_in_use = True

		# Track the turnaround times for multiple processes
		if current_process and CPU_in_use:
			temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

		# Increment time by 1 if there still are bursts to process
		if sum(bursts) != 0:
			time += 1;

	# End of FCFS Simulator

	print("time {}ms: Simulator ended for FCFS [Q {}]\r".format(time, print_queue(queue)))

	# Average wait_times calculations
	average_wait_times = 0
	number_wait_times = 0
	for process in total_wait_times.keys():
		average_wait_times += sum(total_wait_times[process])
		number_wait_times += len(total_wait_times[process])

	average_wait_times /= number_wait_times

	# Average turnaround times calculations
	average_turnaround_times = 0
	number_turnaround_times = 0
	for process in total_turnaround_times.keys():
		average_turnaround_times += sum(total_turnaround_times[process])
		average_turnaround_times += sum(total_wait_times[process])
		number_turnaround_times += len(total_turnaround_times[process])
	average_turnaround_times /= number_turnaround_times

	# Printing out the FCFS algorithm statistics
	print("Algorithm FCFS\r")
	print("-- average CPU burst time: {0:.3f} ms\r".format(total_burst_time/total_bursts_completed))
	print("-- average wait time: {0:.3f} ms\r".format(average_wait_times))
	print("-- average turnaround time: {0:.3f} ms\r".format(average_turnaround_times))
	print("-- total number of context switches: {}\r".format(total_context_switches))
	print("-- total number of preemptions: 0\r")
