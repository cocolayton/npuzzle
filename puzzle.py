#DON'T REPEAT WORK YOU'VE ALREADY DONE!
import copy
def LoadFromFile(filepath):
	with open(filepath, "r") as f:
		N = int(f.readline())

		rest_of_file = f.readlines()

		# check if correct number of rows
		if len(rest_of_file) != N:
			print("invalid puzzle 1")
			return None

		puzzle = {}
		found_hole = 0 # to make sure there is one hole
		count = 0 # keep track of new key in dictionary

		for line in rest_of_file:
			char_list = line.split() # separate numbers
			#char_list = list(map(int, char_list)) 
			puzzle[count] = char_list

			# check if correct number of columns
			if len(char_list) != N:
				print("invalid puzzle 2")
				return None

			for value in char_list:
				# keep track if "*" shows up
				if value == "*":
					found_hole += 1
				# make sure all labels are valid
				elif int(value) > ((N**2) -1) or int(value) < 1:
					print("invalid puzzle 3")
					return None

			count += 1

		# check if there is one "*"
		if found_hole != 1:
			print("invalid puzzle 4")
			return None

		return puzzle, N

def DebugPrint(puzzle_dict):
	for key in puzzle_dict:
		print(puzzle_dict[key])


def IsGoal(state):
	N = len(state)
	num = 1
	for row_index in range(N): #0, 1, 2
		line = []
		for column_index in range(N):
			if (num == N**2):
				line.append("*")
			else:
				line.append(str(num))
			num += 1

		if state[row_index] != line:
			return False


	return True

def ComputeNeighbors(state):
	neighbors = []
	max_index = len(state) - 1

	for row_index, value in state.items():
		if "*" in value:
			column_index = value.index("*")

			# max number of moves: left, right, up, down (check for corner/edge cases tho)

			# move left num into space (can't do this if in first column)
			if column_index != 0:
				new_puzzle = copy.deepcopy(state)
				row = copy.deepcopy(value)

				num_moved = row[column_index - 1]
				row[column_index - 1] = row[column_index]
				row[column_index] = num_moved
				new_puzzle[row_index] = row

				neighbors.append([num_moved, new_puzzle])

			# move right num into space (can't do this if in last column)
			if column_index != max_index:
				new_puzzle_2 = copy.deepcopy(state)
				row_2 = copy.deepcopy(value)

				num_moved_2 = row_2[column_index + 1]
				row_2[column_index + 1] = row_2[column_index]
				row_2[column_index] = num_moved_2
				new_puzzle_2[row_index] = row_2

				neighbors.append([num_moved_2, new_puzzle_2])

			# move num below into the space (can't do this if in bottom row)
			if row_index < max_index:
				new_puzzle_3 = copy.deepcopy(state)
				row_3 = copy.deepcopy(value)

				row_below = new_puzzle_3[row_index + 1]
				num_moved_3 = row_below[column_index]
				row_below[column_index] = row_3[column_index]
				row_3[column_index] = num_moved_3

				new_puzzle_3[row_index + 1] = row_below
				new_puzzle_3[row_index] = row_3

				neighbors.append([num_moved_3, new_puzzle_3])

			# move num above into the space (can't do this if in the top row)
			if row_index > 0:
				new_puzzle_4 = copy.deepcopy(state)
				#print("puzzle 4", new_puzzle_4)
				row_4 = copy.deepcopy(value)

				#print("before up 1", neighbors)
				#print("state before", state)

				row_above = new_puzzle_4[row_index - 1]
				#print("row above", row_above)
				num_moved_4 = row_above[column_index]
				#print("num_moved", num_moved_4)
				row_above[column_index] = row_4[column_index]
				row_4[column_index] = num_moved_4

				#print("row above", row_above)
				#print("row", row_4)
				#print(state)

				#print("row 2", row_index)

				new_puzzle_4[row_index - 1] = row_above
				new_puzzle_4[row_index] = row_4

				#print("puzzle up", new_puzzle_4)

				#print("before up", neighbors)


				neighbors.append([num_moved_4, new_puzzle_4])
				#print("neighbors after up", neighbors)

	return neighbors

def BFS(state):
	# convert state to tuple so can be added to dictionary, sets
	tuple_list = []
	for key, value in state.items():
		tuple_list.append(tuple(value))
	
	puzzle_state = tuple(tuple_list)

	frontier = [state]
	discovered = set(puzzle_state)
	parents = {puzzle_state: None}

	while len(frontier) != 0: # check if empty
		current_state = frontier.pop(0) # get num and dict
		#current_state_puzzle = current_state[1] # just get dictionary
		#print(type(current_state_puzzle))

		# make current state a tuple so it can be added
		#current_tuple = copy.deepcopy(current_state)
		#tuple_list = []
		#for key, value in current_tuple.items():
			#tuple_list.append(tuple(value))
	
		#current_state_tuple = tuple(tuple_list)
		#discovered.add(current_state_tuple)

		if IsGoal(current_state) == True:
			puzzle_path = []
			#num_moved = current_state[0]
			#puzzle_path.append(num_moved)
			check = current_state
			while check != state:
				
				# make tuple to check in parents
				tuple_list = []
				for key, value in check.items():
					tuple_list.append(tuple(value))
	
				check_tuple = tuple(tuple_list)

				puzzle_and_num = parents[check_tuple] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle_and_num[0] # get the num moved
				puzzle_path.append(puzzle_num_moved)
				check = puzzle_and_num[1] # get the dictionary
				#print(type(check))
			
			puzzle_path = puzzle_path[::-1]
			return puzzle_path
			# return the path you need by backtracking in parents

		#print("current state", current_state)
		#print(ComputeNeighbors(current_state))
		for neighbor in ComputeNeighbors(current_state):
			#print("neighbor", neighbor)
			# make a tuple so can check if in discovered
			tuple_list = []
			for key, value in (neighbor[1]).items():
				tuple_list.append(tuple(value))
	
			neighbor_tuple = tuple(tuple_list)
			
			if neighbor_tuple not in discovered: # at 1 because the first item in neighbor is the num moved
				frontier.append(neighbor[1])

				# make neighbor[1] (the puzzle) a tuple for the set
				neighbor_puzzle = neighbor[1]
				tuple_list = []
				for key, value in neighbor_puzzle.items():
					tuple_list.append(tuple(value))
	
				neighbor_puzzle = tuple(tuple_list)
				discovered.add(neighbor_puzzle)

				num_moved = neighbor[0]
				#neighbor_added = tuple([num_moved, neighbor_puzzle])

				parents[neighbor_puzzle] = [num_moved, current_state] # include num moved for this one

	return None # no path possible


def DFS(state):
	# convert state to tuple so can be added to dictionary, sets
	tuple_list = []
	for key, value in state.items():
		tuple_list.append(tuple(value))
	
	puzzle_state = tuple(tuple_list)

	frontier = [state]
	discovered = set(puzzle_state)
	parents = {puzzle_state: None}

	while len(frontier) != 0: # check if empty
		current_state = frontier.pop(0) # get num and dict
		#current_state_puzzle = current_state[1] # just get dictionary
		#print(type(current_state_puzzle))

		# make current state a tuple so it can be added
		#current_tuple = copy.deepcopy(current_state)
		#tuple_list = []
		#for key, value in current_tuple.items():
			#tuple_list.append(tuple(value))
	
		#current_state_tuple = tuple(tuple_list)
		#discovered.add(current_state_tuple)

		if IsGoal(current_state) == True:
			puzzle_path = []
			#num_moved = current_state[0]
			#puzzle_path.append(num_moved)
			check = current_state
			while check != state:
				
				# make tuple to check in parents
				tuple_list = []
				for key, value in check.items():
					tuple_list.append(tuple(value))
	
				check_tuple = tuple(tuple_list)

				puzzle_and_num = parents[check_tuple] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle_and_num[0] # get the num moved
				puzzle_path.append(puzzle_num_moved)
				check = puzzle_and_num[1] # get the dictionary
				#print(type(check))


			puzzle_path = puzzle_path[::-1]
			return puzzle_path
			# return the path you need by backtracking in parents

		#print("current state", current_state)
		#print(ComputeNeighbors(current_state))
		for neighbor in ComputeNeighbors(current_state):
			#print("neighbor", neighbor)
			# make a tuple so can check if in discovered
			tuple_list = []
			for key, value in (neighbor[1]).items():
				tuple_list.append(tuple(value))
	
			neighbor_tuple = tuple(tuple_list)
			
			if neighbor_tuple not in discovered: # at 1 because the first item in neighbor is the num moved
				frontier.insert(0, neighbor[1])

				# make neighbor[1] (the puzzle) a tuple for the set
				neighbor_puzzle = neighbor[1]
				tuple_list = []
				for key, value in neighbor_puzzle.items():
					tuple_list.append(tuple(value))
	
				neighbor_puzzle = tuple(tuple_list)
				discovered.add(neighbor_puzzle)

				num_moved = neighbor[0]
				#neighbor_added = tuple([num_moved, neighbor_puzzle])

				parents[neighbor_puzzle] = [num_moved, current_state] # include num moved for this one

	return None # no path possible

def getGoalState(state):
	N = len(state)
	goal = {}
	num = 1
	for row_index in range(N): #0, 1, 2
		line = []
		for column_index in range(N):
			if (num == N**2):
				line.append("*")
			else:
				line.append(str(num))
			num += 1

		goal[row_index] = line

	tuple_list = []
	for key, value in goal.items():
		tuple_list.append(tuple(value))
	
	goal_tuple = tuple(tuple_list)

	return goal, goal_tuple



def BidirectionalSearch(state):
	tuple_list = []
	for key, value in state.items():
		tuple_list.append(tuple(value))
	
	puzzle_state = tuple(tuple_list)

	goal_state, goal_state_tuple = getGoalState(state)

	frontier_BFS = [state]
	frontier_DFS = [goal_state]
	discovered_BFS = set(puzzle_state)
	discovered_DFS = set(goal_state_tuple)
	parents_BFS = {puzzle_state: None}
	parents_DFS = {goal_state_tuple: None}

	while len(frontier_BFS) != 0 and len(frontier_DFS) != 0: # check if empty

		current_state_BFS = frontier_BFS.pop(0) # get num and dict
		current_state_DFS = frontier_DFS.pop(0) # get num and dict
		
		#recent_discovered_BFS = discovered_BFS.pop()
		#recent_discovered_DFS = discovered_DFS.pop()
		
		if discovered_BFS & discovered_DFS:
			puzzle_path_BFS = []

			check_BFS = current_state_BFS
			while check_BFS != state:
				
				# make tuple to check in parents
				tuple_list = []
				for key, value in check_BFS.items():
					tuple_list.append(tuple(value))
	
				check_tuple = tuple(tuple_list)

				puzzle_and_num = parents_BFS[check_tuple] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle_and_num[0] # get the num moved
				puzzle_path_BFS.append(puzzle_num_moved)
				check_BFS = puzzle_and_num[1] # get the dictionary
				#print(type(check))

			puzzle_path_DFS = []
			check_DFS = current_state_DFS
			while check_DFS != goal_state:
				# make tuple to check in parents
				tuple_list = []
				for key, value in check_DFS.items():
					tuple_list.append(tuple(value))
	
				check_tuple = tuple(tuple_list)

				puzzle_and_num = parents_DFS[check_tuple] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle_and_num[0] # get the num moved
				puzzle_path_DFS.append(puzzle_num_moved)
				check_DFS = puzzle_and_num[1] # get the dictionary
				#print(type(check))

			puzzle_path_BFS = puzzle_path_BFS[::-1] # reverse because numbers are added to the list in the reverse order of what we want

			puzzle_path = puzzle_path_BFS + puzzle_path_DFS # no need to reverse DFS because it will already be in right order bc reveresed the reversed order
			
			return puzzle_path
			# return the path you need by backtracking in parents

		#print("current state", current_state)
		#print(ComputeNeighbors(current_state))
		for neighbor in ComputeNeighbors(current_state_BFS):
			#print("neighbor", neighbor)
			# make a tuple so can check if in discovered
			tuple_list = []
			for key, value in (neighbor[1]).items():
				tuple_list.append(tuple(value))
	
			neighbor_tuple = tuple(tuple_list)
			
			if neighbor_tuple not in discovered_BFS: # at 1 because the first item in neighbor is the num moved
				frontier_BFS.append(neighbor[1])

				# make neighbor[1] (the puzzle) a tuple for the set
				neighbor_puzzle = neighbor[1]
				tuple_list = []
				for key, value in neighbor_puzzle.items():
					tuple_list.append(tuple(value))
	
				neighbor_puzzle = tuple(tuple_list)
				discovered_BFS.add(neighbor_puzzle)

				num_moved = neighbor[0]
				#neighbor_added = tuple([num_moved, neighbor_puzzle])

				parents_BFS[neighbor_puzzle] = [num_moved, current_state_BFS] # include num moved for this one


		for neighbor in ComputeNeighbors(current_state_DFS):
			#print("neighbor", neighbor)
			# make a tuple so can check if in discovered
			tuple_list = []
			for key, value in (neighbor[1]).items():
				tuple_list.append(tuple(value))
	
			neighbor_tuple = tuple(tuple_list)
			
			if neighbor_tuple not in discovered_DFS: # at 1 because the first item in neighbor is the num moved
				frontier_DFS.insert(0, neighbor[1])

				# make neighbor[1] (the puzzle) a tuple for the set
				neighbor_puzzle = neighbor[1]
				tuple_list = []
				for key, value in neighbor_puzzle.items():
					tuple_list.append(tuple(value))
	
				neighbor_puzzle = tuple(tuple_list)
				discovered_DFS.add(neighbor_puzzle)

				num_moved = neighbor[0]
				#neighbor_added = tuple([num_moved, neighbor_puzzle])

				parents_DFS[neighbor_puzzle] = [num_moved, current_state_DFS] # include num moved for this one

	return None # no path possible




puzzle, N = LoadFromFile("/Users/cocolayton/n-puzzle/puzzle_text.txt")

#new_puzzle = {0: ["1", "2", "3"], 1: ["4", "5", "6"], 2: ["7", "8", "*"]}

#goal = IsGoal(new_puzzle)
#print(goal)
path1 = BFS(puzzle)
print("path 1", path1)

path2 = DFS(puzzle)
print("path 2", path2)

path = BidirectionalSearch(puzzle)
print("path", path)

#print(puzzle)

#DebugPrint(puzzle)



