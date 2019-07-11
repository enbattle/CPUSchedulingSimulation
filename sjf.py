import sys
import math

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
		print("time {}ms: Process {} terminated [Q {}]\r"
				.format(time, current_process, print_queue(queue)))
	else:
		if bursts[sorted_processes_by_number[current_process]] == 1:
			print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q {}]\r"
				.format(time, current_process, tau_dict[current_process], bursts[sorted_processes_by_number[current_process]],
				print_queue(queue)))
		else:
			print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q {}]\r"
				.format(time, current_process, tau_dict[current_process], bursts[sorted_processes_by_number[current_process]],
				print_queue(queue)))

		# recalculate tau
		actual_burst = burst_times[sorted_processes_by_number[current_process]].pop(0)
		tau_dict[current_process] = math.ceil((tau_dict[current_process] * alpha_value) + (actual_burst * alpha_value))
		print("time {}ms: Recalculated tau = {}ms for process {} [Q {}]\r"
			.format(time, tau_dict[current_process], current_process, print_queue(queue)))

		current_io = io_times[sorted_processes_by_number[current_process]].pop(0)
		current_io += time + context_switch_time//2

		print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q {}]\r"
			.format(time, current_process, current_io, print_queue(queue)))

		# Add I/O completion to the I/O queue, and sort it
		io_queue.append((current_io, current_process))
		io_queue.sort()


# Check for I/O burst completion
def check_IO_burst(time, queue, io_queue, tau_dict):
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

			#queue.append(io_queue[i][1])

			print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q {}]\r"
				.format(time, incoming_process, tau_dict[incoming_process], print_queue(queue)))

		else:
			continue

	# Remove finished I/O bursts from queue
	if temp_io_queue:
		for i in range(0, len(temp_io_queue)):
			io_queue.remove(temp_io_queue[i])

def check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, tau_dict):
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

	print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q {}]\r"
		.format(time, sorted_processes_by_time[processes[process_counter]], incoming_burst, print_queue(queue)))

def sjf(processes, bursts, burst_times, io_times, context_switch_time, lambda_value, alpha_value):
	process_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
						"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

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

	# Sorted dictionary with arrival times as keys and the process letter as values
	sorted_processes_by_time = dict()
	sorted_processes_by_number = dict()
	tau_dict = dict()

	# Print out all of the initial processes, their arrival times, and CPU bursts
	for i in range(0, len(processes)):
		tau_dict[process_names[i]] = int(1 / lambda_value)
		if bursts[i] == 1:
			print("Process {} [NEW] (arrival time {} ms) {} CPU burst (tau {}ms)\r".format(process_names[i],
			processes[i], bursts[i], tau_dict[process_names[i]]))
		else:
			print("Process {} [NEW] (arrival time {} ms) {} CPU bursts (tau {}ms)\r".format(process_names[i],
			processes[i], bursts[i], tau_dict[process_names[i]]))
		sorted_processes_by_time[processes[i]] = process_names[i]
		sorted_processes_by_number[process_names[i]] = i


	# List of processes sorted by arrival times
	processes = list(sorted(sorted_processes_by_time.keys()))

	# Print out that the simulator stated for SJF
	print("time {}ms: Simulator started for SJF [Q {}]\r".format(time, print_queue(queue)))

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
					check_IO_burst(time, queue, io_queue, tau_dict)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function
						check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, tau_dict)

						process_counter += 1

				time += 1
				temp_num += 1

			# CPU is now freed
			CPU_in_use = False

		# Check for I/O burst completion
		if io_queue:
			# I/O burst completion function
			check_IO_burst(time, queue, io_queue, tau_dict)

		# Check for process arrivals
		if process_counter != len(processes):
			if time == processes[process_counter]:

				# Process arrival function
				check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, tau_dict)

				process_counter += 1

		# IF CPU is not in use, start running a process
		if CPU_in_use == False and len(queue) != 0:
			# Run first process in the queue (First Come, First Serve)
			current_process = queue.pop(0)

			# Add second half of context switch time to bring in the process
			# Also check for processes that may finish in between the addition of context switch time
			temp_num = 0
			while temp_num < context_switch_time//2:
				# Check for I/O burst completion since theres a 2 second context_switch
				if io_queue:
					check_IO_burst(time, queue, io_queue, tau_dict)

				# Check for process arrivals since there is a 2 second context_switch
				if process_counter != len(processes):
					if time == processes[process_counter]:

						# Process arrival function
						check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, tau_dict)

						process_counter += 1

				time += 1
				temp_num += 1

			# Pop the next burst time for the process and check for next burst completion time
			current_burst = burst_times[sorted_processes_by_number[current_process]][0]
			next_burst_completion = time + current_burst

			print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q {}]\r"
				.format(time, current_process, tau_dict[current_process], current_burst, print_queue(queue)))

			# Check for I/O burst completion since theres a 2 second context_switch
			if io_queue:
				check_IO_burst(time, queue, io_queue, tau_dict)

			# Check for process arrivals since there is a 2 second context_switch
			if process_counter != len(processes):
				if time == processes[process_counter]:

					# Process arrival function
					check_process_arrival(time, queue, sorted_processes_by_time, processes, process_counter, tau_dict)

					process_counter += 1

			# CPU now in use
			CPU_in_use = True

		# Increment time by 1 if there still are bursts to process
		if sum(bursts) != 0:
			time += 1;

	# End of SJF Simulator
	print("time {}ms: Simulator ended for SJF [Q {}]\r".format(time, print_queue(queue)))
