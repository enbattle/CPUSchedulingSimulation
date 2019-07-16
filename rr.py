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
Module that contains the RR algorithm used by the main source file

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
def check_CPU_burst(time, current_process, queue, sorted_processes_by_number, bursts, io_queue, io_times, context_switch_time, reprocessing_queue):
	# Decrease burst counter by 1 of the current process
	bursts[sorted_processes_by_number[current_process]] -= 1

	# Print process termination if burst counter is 0
	# Otherwise, print amount of bursts left and next I/O completion
	if bursts[sorted_processes_by_number[current_process]] == 0:
		print("time {}ms: Process {} terminated [Q {}]\r"
				.format(time, current_process, print_queue(queue)))
	else:

		if time <= 999:
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

		if time <= 999:
			print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]\r"
				.format(time, current_process, current_io, print_queue(queue)))

 		# Add I/O completion to the I/O queue, and sort it
		io_queue.append((current_io, current_process))
		io_queue.sort()

	reprocessing_queue[sorted_processes_by_number[current_process]] = False

# Check for I/O burst completion
def check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times, queue_addition):
	temp_io_queue = []

	for i in range(0, len(io_queue)):
		if io_queue[i][0] == time:
			temp_io_queue.append(io_queue[i])

			# Process is added to the beginning or the end of the queue
			if queue_addition == "END":
				queue.append(io_queue[i][1])
			else:
				queue.insert(0, io_queue[i][1])

			if time <= 999:
				print("time {}ms: Process {} completed I/O; added to ready queue [Q {}]\r"
					.format(time, io_queue[i][1], print_queue(queue)))

			temporary_wait_times[sorted_processes_by_number[io_queue[i][1]]] = time

		else:
			continue

	# Remove finished I/O bursts from queue
	if temp_io_queue:
		for i in range(0, len(temp_io_queue)):
			io_queue.remove(temp_io_queue[i])

# Check for process arrival
def check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times, queue_addition):
	# Process arrives and is added to the queue, either in the beginning or the end
	if queue_addition == "END":
		queue.append(sorted_processes_by_time[processes[process_counter]])
	else:
		queue.insert(0, sorted_processes_by_time[processes[process_counter]])

	temporary_wait_times[sorted_processes_by_number[sorted_processes_by_time[processes[process_counter]]]] = time

	if time <= 999:
		print("time {}ms: Process {} arrived; added to ready queue [Q {}]\r"
			.format(time, sorted_processes_by_time[processes[process_counter]], print_queue(queue)))

# Main function that runs the RR algorithm
def rr(some_processes, some_bursts, some_burst_times, some_io_times, context_switch_time, time_slice, queue_addition):
	processes = copy.deepcopy(some_processes)
	bursts = copy.deepcopy(some_bursts)
	burst_times = copy.deepcopy(some_burst_times)
	io_times = copy.deepcopy(some_io_times)

	process_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", 
						"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

	# Variables used to calculate RR statistics
	total_burst_time = 0
	total_wait_times = dict()
	total_turnaround_times = dict()
	total_context_switches = 0
	total_preemptions = 0

	# RR statistics calculations
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
	process_burst_completion = 0
	next_time_slice = 0

	# Queue that holds all of the current processes
	# Queue that holds current I/O bursts
	queue = []
	io_queue = []
	reprocessing_queue = [False] * len(processes)

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

	# Print out that the simulator stated for RR
	print("time {}ms: Simulator started for RR [Q {}]\r".format(time, print_queue(queue)))

	# While there are still bursts left, keep running processes
	while sum(bursts) != 0:

		# Check if CPU burst is greater than time slice
		# Create a preemption and switch to the next process in the CPU
		if time == next_time_slice and time < process_burst_completion and time != 0:

			# Subtract time slice time from the current process burst time
			burst_times[sorted_processes_by_number[current_process]][0] -= time_slice

			# Set the current process as a process that got preempted and will need reprocessing
			reprocessing_queue[sorted_processes_by_number[current_process]] = True

			# Check if queue is empty or not
			if queue:
				if time <= 999:
					print("time {}ms: Time slice expired; process {} preempted with {}ms to go [Q {}]\r"
						.format(time, current_process, burst_times[sorted_processes_by_number[current_process]][0], print_queue(queue)))

				# Increment the preemption
				total_preemptions += 1

				# Add first half of context switch time to remove the process
				# Also check for processes that may finish in between the addition of context switch time
				temp_num = 0
				while temp_num < context_switch_time//2:
					# Check for I/O burst completion since theres a 2 second context_switch
					if io_queue:
						check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times,  queue_addition)

					# Check for process arrivals since there is a 2 second context_switch
					if process_counter != len(processes):
						if time == processes[process_counter]:

							# Process arrival function				
							check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times, queue_addition)

							process_counter += 1

					time += 1
					temp_num += 1
					temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

				# Add turnaround times to appropriate list
				if current_process in total_turnaround_times:
					total_turnaround_times[current_process].append(temporary_turnaround_times[sorted_processes_by_number[current_process]])
					temporary_turnaround_times[sorted_processes_by_number[current_process]] = 0
				else:
					temp_list = []
					temp_list.append(temporary_turnaround_times[sorted_processes_by_number[current_process]])
					total_turnaround_times[current_process] = temp_list
					temporary_turnaround_times[sorted_processes_by_number[current_process]] = 0

				# Check arugment to add process to end or beginning or queue
				if queue_addition == "END":
					queue.append(current_process)
				else:
					queue.insert(0, current_process)

				# Set the wait time for the preempted process to be the time it was added back into the queue
				temporary_wait_times[sorted_processes_by_number[current_process]] = time

			 	# CPU is now freed
				CPU_in_use = False

			# If the queue is empty, keep running current process by increments of time slice
			else:
				if time <= 999:
					print("time {}ms: Time slice expired; no preemption because ready queue is empty [Q {}]\r"
						.format(time, print_queue(queue)))

				# Set new burst time and next time slice time
				current_burst = burst_times[sorted_processes_by_number[current_process]][0]
				process_burst_completion = time + current_burst
				next_time_slice = time + time_slice

		# Check if CPU burst is less than or equal to the time slice
		# If less than, context switch to the next process and run it immediately
		# If equal to, pop the current process burst from the list and continue
		else:
			if time != 0:
				if (time == next_time_slice and time == process_burst_completion) or (time == process_burst_completion):
					# If the current_process finished CPU burst, pop it out of the list
					burst_times[sorted_processes_by_number[current_process]].pop(0)

					# CPU burst completion function
					check_CPU_burst(time, current_process, queue, sorted_processes_by_number, bursts, io_queue, io_times, context_switch_time, reprocessing_queue)

					# Add first half of context switch time to remove the process
					# Also check for processes that may finish in between the addition of context switch time
					temp_num = 0
					while temp_num < context_switch_time//2:
						# Check for I/O burst completion since theres a 2 second context_switch
						if io_queue:
							check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times, queue_addition)

						# Check for process arrivals since there is a 2 second context_switch
						if process_counter != len(processes):
							if time == processes[process_counter]:

								# Process arrival function				
								check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times, queue_addition)

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
			check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times, queue_addition)

		# Check for process arrivals
		if process_counter != len(processes):
			if time == processes[process_counter]:

				# Process arrival function				
				check_process_arrival(time, queue, sorted_processes_by_time, sorted_processes_by_number, processes, process_counter, temporary_wait_times, queue_addition)

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
					check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times, queue_addition)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function				
						check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, temporary_wait_times, queue_addition)

						process_counter += 1 

				time += 1
				temp_num += 1
				temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

			initial_switch = True

			# Find the next burst time for the process and check for next burst completion time
			current_burst = burst_times[sorted_processes_by_number[current_process]][0]
			process_burst_completion = time + current_burst
			next_time_slice = time + time_slice

			# Add burrent burst time to total burst time (to calculate statistic)
			# Increment number of bursts completed
			if reprocessing_queue[sorted_processes_by_number[current_process]] == False:
				total_burst_time += current_burst

			if time <= 999:
				# If process is first time processing, print it for using all bursts
				# If process is some other time processing, print it for using remaining bursts
				if reprocessing_queue[sorted_processes_by_number[current_process]] == False:
					print("time {}ms: Process {} started using the CPU for {}ms burst [Q {}]\r"
						.format(time, current_process, current_burst, print_queue(queue)))
				else:
					print("time {}ms: Process {} started using the CPU with {}ms burst remaining [Q {}]\r"
						.format(time, current_process, current_burst, print_queue(queue)))

			# Check for I/O burst completion since theres a 2 second context_switch
			if io_queue:
				check_IO_burst(time, queue, io_queue, sorted_processes_by_number, temporary_wait_times, queue_addition)

			# Check for process arrivals since there is a 2 second context_switch
			if process_counter != len(processes):
				if time == processes[process_counter]:

					# Process arrival function				
					check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, temporary_wait_times, queue_addition)

					process_counter += 1

			# CPU now in use
			CPU_in_use = True

		# Track the turnaround times for multiple processes
		if current_process and CPU_in_use:
			temporary_turnaround_times[sorted_processes_by_number[current_process]] += 1

		# Increment time by 1 if there still are bursts to process
		if sum(bursts) != 0:
			time += 1;

	# End of RR Simulator
	print("time {}ms: Simulator ended for RR [Q {}]\r".format(time, print_queue(queue)))

	# Create file (if it does not already exist) and write to it
	statistic_file = "simout.txt"
	open_file = open(statistic_file, "a")

	# Average wait_times calculations
	average_wait_times = 0
	number_wait_times = 0
	for process in total_wait_times.keys():
		average_wait_times += sum(total_wait_times[process])
		number_wait_times += len(total_wait_times[process])

	average_wait_times /= (number_wait_times - total_preemptions)

	# Average turnaround times calculations
	average_turnaround_times = 0
	number_turnaround_times = 0
	for process in total_turnaround_times.keys():
		average_turnaround_times += sum(total_turnaround_times[process])
		average_turnaround_times += sum(total_wait_times[process])
		number_turnaround_times += len(total_turnaround_times[process])
	average_turnaround_times /= (number_turnaround_times - total_preemptions)

	# Printing out the RR algorithm statistics
	open_file.write("Algorithm RR\r")
	open_file.write("-- average CPU burst time: {0:.3f} ms\r".format(total_burst_time/total_bursts_completed))
	open_file.write("-- average wait time: {0:.3f} ms\r".format(average_wait_times))
	open_file.write("-- average turnaround time: {0:.3f} ms\r".format(average_turnaround_times))
	open_file.write("-- total number of context switches: {}\r".format(total_context_switches + total_preemptions))
	open_file.write("-- total number of preemptions: {}\r".format(total_preemptions))

	open_file.close()