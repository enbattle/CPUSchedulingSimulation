'''
Group Project

Steven Li
Justin Chen
Ishita Padhiar

July 12, 2019
Operating Systems
Summer 2019

'''

import sys
import math
import copy
import random

'''
Module that contains the SJF algorithm used by the main source file

'''

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
def check_CPU_burst(time, current_process, queue, sorted_processes_by_number, bursts, io_queue, io_times, context_switch_time, tau_dict, burst_times, alpha_value):
	# Decrease burst counter by 1 of the current process
	bursts[sorted_processes_by_number[current_process]] -= 1

	# Print process termination if burst counter is 0
	# Otherwise, print amount of bursts left and next I/O completion
	if bursts[sorted_processes_by_number[current_process]] == 0:
		print("time {}ms: Process {} terminated [Q {}]"
				.format(time, current_process, print_queue(queue)))
	else:
		if time <= 999:
			if bursts[sorted_processes_by_number[current_process]] == 1:
				print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q {}]"
					.format(time, current_process, tau_dict[current_process], bursts[sorted_processes_by_number[current_process]],
					print_queue(queue)))
			else:
				print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]"
					.format(time, current_process, tau_dict[current_process], bursts[sorted_processes_by_number[current_process]],
					print_queue(queue)))

		# recalculate tau
		actual_burst = burst_times[sorted_processes_by_number[current_process]].pop(0)
		tau_dict[current_process] = math.ceil((tau_dict[current_process] * (1-alpha_value)) + (actual_burst * alpha_value))
		
		if time <= 999:
			print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]"
				.format(time, tau_dict[current_process], current_process, print_queue(queue)))

		current_io = io_times[sorted_processes_by_number[current_process]].pop(0)
		current_io += time + context_switch_time//2

		if time <= 999:
			print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]"
				.format(time, current_process, current_io, print_queue(queue)))

		# Add I/O completion to the I/O queue, and sort it
		io_queue.append((current_io, current_process))
		io_queue.sort()


# Check for I/O burst completion
def check_IO_burst(time, queue, io_queue, tau_dict, sorted_processes_by_number, temporary_wait_times):
	temp_io_queue = []

	for i in range(0, len(io_queue)):
		if io_queue[i][0] == time:
			temp_io_queue.append(io_queue[i])

			incoming_process = io_queue[i][1]
			incoming_burst = tau_dict[incoming_process]
			inserted = False
			for j in range(0, len(queue)):
				temp_burst = tau_dict[queue[j]]
				if (incoming_burst < temp_burst) or (incoming_burst == temp_burst and incoming_process < queue[j]):
					queue.insert(j, incoming_process)
					inserted = True
					break

			if (inserted == False):
				queue.append(incoming_process)

			if time <= 999:
				print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q {}]"
					.format(time, incoming_process, tau_dict[incoming_process], print_queue(queue)))

			temporary_wait_times[sorted_processes_by_number[io_queue[i][1]]] = time

		else:
			continue

	# Remove finished I/O bursts from queue
	if temp_io_queue:
		for i in range(0, len(temp_io_queue)):
			io_queue.remove(temp_io_queue[i])

def check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, tau_dict, temporary_wait_times):
	# Process arrives and is added to the queue
	incoming_process = sorted_processes_by_time[processes[process_counter]]
	incoming_burst = tau_dict[incoming_process]
	inserted = False
	for i in range(0, len(queue)):
		temp_burst = tau_dict[queue[i]]
		if (incoming_burst < temp_burst) or (incoming_burst == temp_burst and incoming_process < queue[i]):
			queue.insert(i, incoming_process)
			inserted = True
			break

	if (inserted == False):
		queue.append(incoming_process)

	temporary_wait_times[sorted_processes_by_number[sorted_processes_by_time[processes[process_counter]]]] = time

	if time <= 999:
		print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]"
			.format(time, sorted_processes_by_time[processes[process_counter]], incoming_burst, print_queue(queue)))

# Main function that runs the SJF Algorithm
def sjf(some_processes, some_bursts, some_burst_times, some_io_times, context_switch_time, lambda_value, alpha_value):
	processes = copy.deepcopy(some_processes)
	bursts = copy.deepcopy(some_bursts)
	burst_times = copy.deepcopy(some_burst_times)
	io_times = copy.deepcopy(some_io_times)

	process_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
						"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

	# Variables used to calculate SJF statistics
	total_burst_time = 0
	total_wait_times = dict()
	total_turnaround_times = dict()
	total_context_switches = 0

	# SJF statistics calculations
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
	tau_dict = dict()

	# Print out all of the initial processes, their arrival times, and CPU bursts
	for i in range(0, len(processes)):
		tau_dict[process_names[i]] = int(1 / lambda_value)
		if bursts[i] == 1:
			print("Process {} [NEW] (arrival time {} ms) {} CPU burst (tau {}ms)".format(process_names[i],
			processes[i], bursts[i], tau_dict[process_names[i]]))
		else:
			print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {}ms)".format(process_names[i],
			processes[i], bursts[i], tau_dict[process_names[i]]))
		sorted_processes_by_time[processes[i]] = process_names[i]
		sorted_processes_by_number[process_names[i]] = i


	# List of processes sorted by arrival times
	processes = list(sorted(sorted_processes_by_time.keys()))

	# Print out that the simulator stated for SJF
	print("time {}ms: Simulator started for SJF [Q {}]".format(time, print_queue(queue)))

	# While there are still bursts left, keep running processes
	while sum(bursts) != 0:
		# Check for CPU burst completion (CPU is free for next process)
		# (Also check if process has terminated with last CPU burst)
		if time == next_burst_completion and time != 0:

			# CPU burst completion function
			check_CPU_burst(time, current_process, queue, sorted_processes_by_number, bursts, io_queue, io_times, context_switch_time, tau_dict, burst_times, alpha_value)

			# Add first half of context switch time to remove the process
			# Also check for processes that may finish in between the addition of context switch time
			temp_num = 0
			while temp_num < context_switch_time//2:
				# Check for I/O burst completion since theres a 2 second context_switch
				if io_queue:
					check_IO_burst(time, queue, io_queue, tau_dict, sorted_processes_by_number, temporary_wait_times)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function
						check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, tau_dict, temporary_wait_times)

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

		# Check for I/O burst completion
		if io_queue:
			# I/O burst completion function
			check_IO_burst(time, queue, io_queue, tau_dict, sorted_processes_by_number, temporary_wait_times)

		# Check for process arrivals
		if process_counter != len(processes):
			if time == processes[process_counter]:

				# Process arrival function
				check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, tau_dict, temporary_wait_times)

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
				# Check for I/O burst completion since theres a 2 second context_switch
				if io_queue:
					check_IO_burst(time, queue, io_queue, tau_dict, sorted_processes_by_number, temporary_wait_times)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function
						check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, tau_dict, temporary_wait_times)

						process_counter += 1

				time += 1
				temp_num += 1
				temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

			initial_switch = True

			# Pop the next burst time for the process and check for next burst completion time
			current_burst = burst_times[sorted_processes_by_number[current_process]][0]
			next_burst_completion = time + current_burst

			# Add burrent burst time to total burst time (to calculate statistic)
			# Increment number of bursts completed
			total_burst_time += current_burst

			if time <= 999:
				print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]"
					.format(time, current_process, tau_dict[current_process], current_burst, print_queue(queue)))

			# Check for I/O burst completion since theres a 2 second context_switch
			if io_queue:
				check_IO_burst(time, queue, io_queue, tau_dict, sorted_processes_by_number, temporary_wait_times)

			# Check for process arrivals since there is a 2 second context_switch
			if process_counter != len(processes):
				if time == processes[process_counter]:

					# Process arrival function
					check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, tau_dict, temporary_wait_times)

					process_counter += 1

			# CPU now in use
			CPU_in_use = True

		# Track the turnaround times for multiple processes
		if current_process and CPU_in_use:
			temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

		# Increment time by 1 if there still are bursts to process
		if sum(bursts) != 0:
			time += 1;

	# End of SJF Simulator
	print("time {}ms: Simulator ended for SJF [Q {}]".format(time, print_queue(queue)))

	# Create file (if it does not already exist) and write to it
	statistic_file = "simout.txt"
	open_file = open(statistic_file, "a")

	# Average wait_times calculations
	average_wait_times = 0
	number_wait_times = 0
	for process in total_wait_times.keys():
		average_wait_times += sum(total_wait_times[process])

	average_wait_times /= total_bursts_completed

	# Average turnaround times calculations
	average_turnaround_times = 0
	number_turnaround_times = 0
	for process in total_turnaround_times.keys():
		average_turnaround_times += sum(total_turnaround_times[process])
		average_turnaround_times += sum(total_wait_times[process])

	average_turnaround_times /= total_bursts_completed

	# Printing out the SJF algorithm statistics
	open_file.write("Algorithm SJF\n")
	open_file.write("-- average CPU burst time: {0:.3f} ms\n".format(total_burst_time/total_bursts_completed))
	open_file.write("-- average wait time: {0:.3f} ms\n".format(average_wait_times))
	open_file.write("-- average turnaround time: {0:.3f} ms\n".format(average_turnaround_times))
	open_file.write("-- total number of context switches: {}\n".format(total_context_switches))
	open_file.write("-- total number of preemptions: 0\n")

	open_file.close()