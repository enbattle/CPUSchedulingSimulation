import sys
import math

def print_queue(queue):
	current_queue = ""

	if len(queue) == 0:
		current_queue += "<empty>"
	else:
		for i in range(0, len(queue)):
			current_queue += queue[i] + " "

def fcfs(processes, bursts, burst_times, io_times, context_switch_time):
	process_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", 
						"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	time = 0

	queue = []

	print("Process {} [NEW] (arrival time {} ms) {} CPU bursts")
	print("Stimulator started for FCFS")
