"""
	Name: Coco Layton
	Date: October 25, 2020
	Block: G
"""
import copy

"""
	Load puzzle from file and make sure it's valid

	Arguments: string
	Returns: dictionary, int
"""
def LoadFromFile(filepath):
	with open(filepath, "r") as f:
		N = int(f.readline())
		rest_of_file = f.readlines()

		# check if correct number of rows
		if len(rest_of_file) != N:
			print("invalid puzzle")
			return None

		puzzle = {}
		found_hole = 0 # to make sure there is one hole
		count = 0 # keep track of new key in dictionary

		for line in rest_of_file:
			char_list = line.split() # separate numbers
			puzzle[count] = char_list

			# check if correct number of columns
			if len(char_list) != N:
				print("invalid puzzle")
				return None

			for value in char_list:
				# keep track if "*" shows up
				if value == "*":
					found_hole += 1
				# make sure all labels are valid
				elif int(value) > ((N**2) -1) or int(value) < 1:
					print("invalid puzzle")
					return None

			count += 1

		# make sure there is only one "*"
		if found_hole != 1:
			print("invalid puzzle")
			return None

		return puzzle, N

def DebugPrint(puzzle_dict):
	for key in puzzle_dict:
		print(puzzle_dict[key])

"""
	Check if the puzzle sent in is in the solved state

	Arguments: dictionary
	Returns: boolean
"""
def IsGoal(state):
	N = len(state)
	num = 1 # increment to get numbers of puzzle in order

	for row_index in range(N):
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


"""
	Given the puzzle sent in, compute all possible moves that can be done and what the new
	puzzle would look like. Return a list of the numbers that were moved and what the corresponding
	new puzzle is

	Arugments: dictionary
	Returns: list
"""
def ComputeNeighbors(state):
	neighbors = []
	max_index = len(state) - 1

	for row_index, value in state.items():
		if "*" in value:
			column_index = value.index("*")

			# move num to the left of the space (can't do this if in first column)
			if column_index != 0:
				new_puzzle = copy.deepcopy(state) # deepcopy so that state isn't changed
				row = copy.deepcopy(value)

				num_moved = row[column_index - 1]
				row[column_index - 1] = row[column_index]
				row[column_index] = num_moved
				new_puzzle[row_index] = row

				neighbors.append([num_moved, new_puzzle])

			# move right num into space (can't do this if in last column)
			if column_index != max_index:
				new_puzzle = copy.deepcopy(state)
				row = copy.deepcopy(value)

				num_moved = row[column_index + 1]
				row[column_index + 1] = row[column_index]
				row[column_index] = num_moved
				new_puzzle[row_index] = row

				neighbors.append([num_moved, new_puzzle])

			# move num below into the space (can't do this if in bottom row)
			if row_index < max_index:
				new_puzzle = copy.deepcopy(state)
				row = copy.deepcopy(value)

				row_below = new_puzzle[row_index + 1]
				num_moved = row_below[column_index]
				row_below[column_index] = row[column_index]
				row[column_index] = num_moved

				new_puzzle[row_index + 1] = row_below
				new_puzzle[row_index] = row

				neighbors.append([num_moved, new_puzzle])

			# move num above into the space (can't do this if in the top row)
			if row_index > 0:
				new_puzzle = copy.deepcopy(state)
				
				row = copy.deepcopy(value)

				row_above = new_puzzle[row_index - 1]
				
				num_moved = row_above[column_index]

				row_above[column_index] = row[column_index]
				row[column_index] = num_moved

				new_puzzle[row_index - 1] = row_above
				new_puzzle[row_index] = row


				neighbors.append([num_moved, new_puzzle])
				

	return neighbors


"""
	Take in a puzzle (dictionary) and convert it to a tuple so it can be added to sets and other
	dictionaries without a hashing problem

	Arguments: dictionary
	Returns: tuple
"""
def ConvertToTuple(state):
	tuple_list = []
	for key, value in state.items():
		tuple_list.append(tuple(value))
	
	puzzle_tuple = tuple(tuple_list)
	return puzzle_tuple

"""
	Breadth first search algorithm that looks at all possible neighbors of each new puzzle state (starting
	with the original puzzle sent in) to find the shortest path (which is a list of the numbers in the
	puzzle that are moved) to solve the puzzle

	Arguments: dictionary
	Returns: list
"""
def BFS(state):
	puzzle_tuple = ConvertToTuple(state) 

	frontier = [state] # keeps track of new puzzle states to check
	discovered = set(puzzle_tuple) # keeps track of puzzle states already looked at
	parents = {puzzle_tuple: None} # keeps track of each neighbor puzzle's parent puzzle

	while len(frontier) != 0:
		current_state = frontier.pop(0)
		
		if IsGoal(current_state) == True:
			puzzle_path = []
			check = current_state # as traverse back through parent dict, check is used to check when
									# you're back to the original state and thus have found a path
			
			while check != state:
				# get the num_moved and parent puzzle for this puzzle state from the parent dict
				check_tuple = ConvertToTuple(check)
				puzzle_and_num = parents[check_tuple] # get num_moved, parent puzzle
				puzzle_num_moved = puzzle_and_num[0]
				puzzle_path.append(puzzle_num_moved)
				check = puzzle_and_num[1]
			
			puzzle_path = puzzle_path[::-1]
			return puzzle_path


		for neighbor in ComputeNeighbors(current_state):
			neighbor_tuple = ConvertToTuple(neighbor[1])
			
			if neighbor_tuple not in discovered:
				frontier.append(neighbor[1]) # append puzzle dictionary to the back of the list

				neighbor_puzzle = neighbor[1]
				neighbor_puzzle_tuple = ConvertToTuple(neighbor_puzzle)

				# add this neighbor puzzle to discovered and the parent dict
				discovered.add(neighbor_puzzle_tuple)
				num_moved = neighbor[0]
				parents[neighbor_puzzle_tuple] = [num_moved, current_state] # current state = parent puzzle

	return None # no path possible


"""
	Depth first search algorithm implemented.

	Arguments: dictionary
	Returns: list
"""
def DFS(state):
	puzzle_tuple = ConvertToTuple(state)

	frontier = [state] # keeps track of new puzzle states to check
	discovered = set(puzzle_tuple) # keeps track of puzzle states already looked at
	parents = {puzzle_tuple: None} # keeps track of each neighbor puzzle's parent puzzle

	while len(frontier) != 0:
		current_state = frontier.pop(0)

		if IsGoal(current_state) == True:
			puzzle_path = []
			check = current_state # as traverse back through parent dict, check is used to check when
									# you're back to the original state and thus have found a path

			while check != state:
				# get the num_moved and parent puzzle for this puzzle state from the parent dict
				check_tuple = ConvertToTuple(check)
				puzzle_and_num = parents[check_tuple] # get num_moved, parent puzzle
				puzzle_num_moved = puzzle_and_num[0]
				puzzle_path.append(puzzle_num_moved)
				check = puzzle_and_num[1]


			puzzle_path = puzzle_path[::-1]
			return puzzle_path

		for neighbor in ComputeNeighbors(current_state):
			neighbor_tuple = ConvertToTuple(neighbor[1])
			
			if neighbor_tuple not in discovered:
				frontier.insert(0, neighbor[1]) # append puzzle dictionary to the front of the list

				neighbor_puzzle = neighbor[1]
				neighbor_puzzle_tuple = ConvertToTuple(neighbor_puzzle)
				
				# add this neighbor puzzle to discovered and the parent dict
				discovered.add(neighbor_puzzle_tuple)
				num_moved = neighbor[0]
				parents[neighbor_puzzle_tuple] = [num_moved, current_state] # current state = parent tuple

	return None # no path possible

"""
	Takes in the original puzzle, and uses it to determine the solved state of the puzzle. This function
	returns both the goal puzzle as a dictionary and tuple.

	Arugments: dictionary
	Returns: dictionary, tuple
"""
def getGoalState(state):
	N = len(state)
	goal = {}
	num = 1 # increment to get numbers of puzzle in order
	for row_index in range(N):
		line = []
		for column_index in range(N):
			if (num == N**2):
				line.append("*")
			else:
				line.append(str(num))
			num += 1

		goal[row_index] = line

	# now make a tuple version
	goal_tuple = ConvertToTuple(goal)

	return goal, goal_tuple

"""
	Function to make a tuple a dictionary
"""
def ToDict(tuple_state, state):
	N = len(state)
	dict_state = {}
	for num in range(N):
		dict_state[num] = tuple_state[num]

	return dict_state


"""
	BiDirectional Search implemented

	Arguments: dictionary
	Returns: List
"""
def BidirectionalSearch(state):
	puzzle_tuple = ConvertToTuple(state)
	goal_state, goal_state_tuple = getGoalState(state)

	# keeps track of new puzzle states to check for BFS
	frontier_for = [state]
	frontier_back = [goal_state]

	# keeps track of puzzle states already looked at
	discovered_for = set()
	discovered_back = set()

	# keeps track of each neighbor puzzle's parent puzzle
	parents_for = {puzzle_tuple: None}
	parents_back = {goal_state_tuple: None}

	while len(frontier_for) != 0 and len(frontier_back) != 0:
		current_state_for = frontier_for.pop(0)
		tuple_current_state_for = ConvertToTuple(current_state_for) # tuple so can add to discovered

		current_state_back = frontier_back.pop(0)
		tuple_current_state_back = ConvertToTuple(current_state_back)

		discovered_for.add(tuple_current_state_for)
		discovered_back.add(tuple_current_state_back)
		
		if discovered_for & discovered_back:
			puzzle_path_for = []
			check_for = discovered_for.intersection(discovered_back) # as traverse back through parent dict, check is used to check when
																	# you're back to the original state and thus have found a path
			
			check_for = ToDict(check_for.pop(), state) # convert so it doesn't get messed up by tuple later

			while check_for != state:
				# get the num_moved and parent puzzle for this puzzle state from the parent dict
				check_for = ConvertToTuple(check_for)
				puzzle_and_num = parents_for[check_for] # get num_moved, parent puzzle
				puzzle_num_moved = puzzle_and_num[0]
				puzzle_path_for.append(puzzle_num_moved)
				check_for = puzzle_and_num[1]

			puzzle_path_for = puzzle_path_for[::-1]

			puzzle_path_back = []
			check_back = discovered_back.intersection(discovered_for) # as traverse back through parent dict, check used to check when back to
																		# OG state (which in this case is the goal state) and thus have found a path
			
			check_back = ToDict(check_back.pop(), state) # convert so it doesn't get messed up by tuple later
			
			while check_back != goal_state:
				# get the num_moved and parent puzzle for this puzzle state from the parent dict
				check_back = ConvertToTuple(check_back)
				puzzle_and_num = parents_back[check_back] # get num_moved, parent puzzle
				puzzle_num_moved = puzzle_and_num[0]
				puzzle_path_back.append(puzzle_num_moved)
				check_back = puzzle_and_num[1]

			puzzle_path = puzzle_path_for + puzzle_path_back
			return puzzle_path


		for neighbor in ComputeNeighbors(current_state_for):
			neighbor_tuple = ConvertToTuple(neighbor[1])
			
			if neighbor_tuple not in discovered_for:
				frontier_for.append(neighbor[1]) # append puzzle dictionary to the back of the list

				neighbor_puzzle = neighbor[1]
				neighbor_puzzle_tuple = ConvertToTuple(neighbor_puzzle)
				
				# add this neighbor puzzle to discovered and the parent dict
				discovered_for.add(neighbor_puzzle_tuple)
				num_moved = neighbor[0]
				parents_for[neighbor_puzzle_tuple] = [num_moved, current_state_for] # current state = parent tuple

				# as soon as find a neighbor in discovered quit and go find path
				if neighbor_tuple in discovered_back:
					break

		for neighbor in ComputeNeighbors(current_state_back):
			neighbor_tuple = ConvertToTuple(neighbor[1])
			
			if neighbor_tuple not in discovered_back:
				frontier_back.append(neighbor[1]) # append puzzle dictionary to the back of the list

				neighbor_puzzle = neighbor[1]
				neighbor_puzzle_tuple = ConvertToTuple(neighbor_puzzle)
				
				# add this neighbor puzzle to discovered and the parent dict
				discovered_back.add(neighbor_puzzle_tuple)

				num_moved = neighbor[0]
				parents_back[neighbor_puzzle_tuple] = [num_moved, current_state_back] # current state = parent tuple

				# as soon as find a neighbor in discovered quit and go find path
				if neighbor_tuple in discovered_for:
					break

	return None # no path possible


puzzle, N = LoadFromFile("/Users/cocolayton/n-puzzle/puzzle_text.txt")

path1 = BFS(puzzle)
print("path 1", path1)

path2 = DFS(puzzle)
print("path 2", path2)

path = BidirectionalSearch(puzzle)
print("path bi", path)



