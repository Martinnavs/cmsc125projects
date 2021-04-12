"""
A. Navarez's Submission for CMSC 125 Machine Problem 1
Multiprogramming Simulation

Assumptions:
- One user cannot requeue to the same resource
e.g. There cannot be 2 records of User 1 requests
to some Resource X
- The number of users that will use/request for a certain resource is randomly generated (0-30).
- If a user is enqueued in two or more resources, the following rules are
  to be followed:

  1. User priorities are based on their number
    e.g. User 1 goes first than User 2, User 2 than User 3, and so on

  2. Users with high priorities that are enqueued in multiple resources
     are prioritized based on the Resource number
    e.g. User 1 is queued in both Resource 1 and Resource 2, User 1 uses
         Resource 1 rather than Resource 2

  3. In the case where Rule 2 is present and there are other queued users,
     Rule 1 and Rule 2 are applied to the queue except the head. The head will be placed in the second position of the queue and the User determined by both rules becomes the head.
    e.g.
      Before Rule 3:
      Resource 1 queued users - 1, 2, 3
      Resource 2 queued users - 1, 4, 5
      Resource 3 queued users - 1, 4, 6

      After Rule 3:
      Resource 1 queued users - 1, 2, 3
      Resource 2 queued users - 4, 1, 5 (1 currently using another resource, Resource 2 is prior to Resource 3 so 4 uses it)
      Resource 3 queued users - 6, 1, 4 (1 and 4 currently using another resource)

  4. In the case where Rule 2 is present and there are no other queued users OR
     all users in the queue are currently using other resources,the system
     STALLS the usage of the user/s in a that resource, following
     the prioritization in Rule 2.
    e.g.
      Resource 1 queued users - 1
      Resource 2 queued users - 2
      Resource 3 queued users - 1
      Resource 4 queued users - 1, 2

      After Rule 4
      Resource 1 queued users - 1 (active)
      Resource 2 queued users - 2 (active)
      Resource 3 queued users - 1 (STALLED) 
                          [no other queued users, currently using resource 1]
      Resource 4 queued users - 1 (STALLED), 2 (cannot use rule 3)
                          [has queued users, all currently using some other]

- Initialization will start at t=0, and updates will proceed based on the t value, which represents the elapsed time unit
- Printing per unit time indicates (a) the resource, (b) the user currently 
using it with its status (STALLED or time units remaining) or FREE if there 
are no users, and (c) other enqueued users with their alloted time and the 
time when they are able to use the resource
- Program terminates once all resources are free
"""

from random import randint, sample, choice
import gc

# INITIALIZATION PHASE

# can edit this for random scope, which determines the 
# number of users, resources, and time allocated
actual_val = 30

resources = sample(range(1,31), randint(1,actual_val))
resources.sort()
os = {key:value for (key, value) in [(x,{}) for x in resources]}
os = dict(sorted(os.items(), key=lambda x: x[0]))

users = sample(range(1,31), randint(1, actual_val))

t = 0
memoize_list = []
original_time = {}

print("!"*70)
print("Generated resources: " + str(resources))

for resource in os:
	avail_users = [] 
	for j in range(randint(0, actual_val)):
		# assuming nga dili pwede muenqueue si user balik sa usa ka resource

		user = choice(users)

		while(user in avail_users):
			user = choice(users)

		rand_time = randint(1,actual_val)
		original_time[user] = None #initializing 
		avail_users.append((user, [rand_time, True]))

		# if 1 user ra and added na into os, break 
		if len(users)== 1 or len(avail_users)==0:
			break 
	
	if len(avail_users) > 1:
		avail_users.sort(key = lambda x: x[0])

	os[resource] = {key:value for (key,value) in avail_users}

users.sort()
print("Generated users: " + str(users))

# END OF INITIALIZATION

def reorder():
	global memoize_list 
	global os

	for resource in os:
		resource_list = [list(x) for x in list(os[resource].items())]
		for i in range(len(resource_list)):
			# valid first item
			if resource_list[i][0] not in memoize_list:
				if i==0 or (i>0 and resource_list[0][1][1]):
					# if at 0 then valid, runnable first item
					if i != 0:
						resource_list.insert(0, resource_list.pop(i))
			
					resource_list[0][1][1] = False
					memoize_list.append(resource_list[0][0])
					original_time[resource_list[0][0]] = resource_list[0][1][0]
					break

		os[resource] = {key:value for (key, value) in resource_list}
		gc.collect()

def check_head():
	global os
	global memoize_list
	has_changes = False
	
	for resource in os:
		for user in os[resource]:
			if (os[resource][user][0] == 0 and not has_changes) or os[resource][user][0] < 0:
				# change time except for the new head
				if not has_changes:
				  one_timeunit()
				  has_changes = True

				memoize_list.remove(user)
				del os[resource][list(os[resource])[0]]
			break
	
	if has_changes:
		reorder()
	return has_changes

def print_os():
	print("Resource x User for t={}".format(t))
	print("-"*60)
	for resource in os:
		print("Resource {}:".format(resource), end = " ")
		if len(os[resource]) == 0:
			print("FREE")
		else:
			timeval = 0
			first = True
			for user in os[resource]:
				et = os[resource][user][0]
				if first:
					print("user {} currently using ".format(user), end="" ) 
					if os[resource][user][1]:
						print("- STALLED")
						print("[" + "!"*10 + "]")
					else:
						print("{} to go before termination".format(et))
						preq = "=" *  (original_time[user]-et)
						arr = ">" if et!=0 else ""
						spc = " " * (et)
						print("[" + preq + arr + spc + "]", end ="")
						print(" DONE USING")if et == 0 else print("")
					first = False
					print("Users in Line:")
				else:
					print("user {}, alloted time: {}, to use in: {}".format(user, et,timeval)) 
				timeval += et
	
		print()

def one_timeunit():
	global t
	global os

	t = t + 1

	for resource in os:
		for user in os[resource]:
			if not os[resource][user][1]:
				os[resource][user][0] -= 1
			break

def to_terminate():
	for resource in os:
		if len(os[resource]) > 0:
			return False

	return True

def move_time():
	print_os()
	if not check_head():
		one_timeunit()
	print("\n\n")

def main():
	print("!"*70)
	reorder()

	while not to_terminate():
		move_time()

	print("Program Terminated.")


if __name__ == "__main__":
	main()
