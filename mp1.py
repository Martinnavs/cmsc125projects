# necessary ba nga naay muqueue for every resource? at least one user to use a resource?
# for current approach, stall if tanan possible user naggamit sa some resource and naay lain resource where sila ang naa sa first
# to handle case when 1 user ra and 1< ang resources and dapat naay muqueue each (mawala if dili needed) or katong case stated


import math
from random import randint
import gc

os = {key:value for (key, value) in [(x+1,{}) for x in range(randint(1, 5))]}
users = randint(1, 5)
t = 0
memoize_list = []

for i in range(1,len(os)+1):
	avail_users = [] 
	for j in range(randint(1,5)):
		# assuming nga dili pwede muenqueue si user balik sa usa ka resource

		user = randint(1, users)

		while(user in avail_users):
			user = randint(1, users)

		avail_users.append((user, [randint(1,5), True]))

		# if 1 user ra and added na into os, break 
		if users == 1 or len(avail_users)==0:
			break 
	
	if len(avail_users) > 1:
		avail_users.sort(key = lambda x: x[0])

	os[i] = {key:value for (key,value) in avail_users}


# to delete del dic[list(dic)[0]]
def reorder():
	global memoize_list 
	global os

	for resource in os:
		resource_list = [list(x) for x in list(os[resource].items())]
#		print(resource_list)
		for i in range(len(resource_list)):
			# valid first item
			if resource_list[i][0] not in memoize_list and not(i>0 and resource_list[i-1][1]):
				# if at 0 then valid, runnable first item
				if i != 0:
					# print("HERE, NEED TO CHANGE {}".format(resource_list))
					resource_list.insert(0, resource_list.pop(i))
		
				resource_list[0][1][1] = False
				memoize_list.append(resource_list[0][0])
				break
#		print(resource_list)
		os[resource] = {key:value for (key, value) in resource_list}
#		print(os[resource], end="\n\n")
		gc.collect()

def check_head():
	global os
	global memoize_list
	has_changes = False
	
	for resource in os:
		for user in os[resource]:
			if os[resource][user][0] < 1 :
				# change time except for the new head
				one_timeunit()

#				print("WILL REMOVE {} from {}".format(os[resource][user],os[resource]))
#				print("WILL POP {} FROM {}".format(user, memoize_list))
				memoize_list.remove(user)
				del os[resource][list(os[resource])[0]]
#				print("NEW HEAD{}".format(os[resource]))
#				print("NEW LIST{}".format(memoize_list), end="\n\n")
				has_changes = True
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
					else:
						print("{} to go before termination".format(et))
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
	reorder()
	while not to_terminate():
		move_time()

	print("Program Terminated.")


if __name__ == "__main__":
	main()
