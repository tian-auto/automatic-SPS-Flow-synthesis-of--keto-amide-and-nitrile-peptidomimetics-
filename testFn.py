class testFn:


	def num():
		
		print("1")

	globals()["num_2"] = 3

	print("********************")
	print(num_2)
	
	print("********************")
	for i in range(10):
		if i/2 % 1 ==0:
			globals()["num_%d"%i] = i+10
			print(i)
		else:
			print("error")
	print("********************")
	print(num_2)
	print("********************")