def getTodb(db, name, value):
	out = dict(name = "%s" % name, value = "%s" % value)
	db.append(out)
	print("Updated: ")
	for person in db:
		fields = []
		for name in person:
			fields.append(name)
		print(person[fields[0]], person[fields[1]])
	print()
db = []
getTodb(db, "Sue", "Soft")
getTodb(db, "Joe", "Hardware")
getTodb(db, "MyChicken", "CEO")









from random import *

def detA(A):
	matrix_grade = len(A)
	det, member, order, temp = 0, 1, 0, 0;
	checked = [ [False for i in range(matrix_grade)] for j in range(matrix_grade) ]


	for first_row_element in range(matrix_grade):
		for member_inclusion in range(matrix_grade - 1):		
			member = A[0][first_row_element];
			checked[0][first_row_element] = True;

			for rows in range(matrix_grade - 1 ):
				for row_elem in range(matrix_grade):

					if (checked[0][row_elem] == False) and (checked[rows+1][row_elem] == False):
						checked[0][row_elem] = True
						checked[rows+1][row_elem] = True
						member *= A[rows+1][row_elem]
						if temp == 0: temp += row_elem
						else:
							if row_elem > temp:
								temp = row_elem
								order += 1
						break

			det += (-1)**(order)*member
			order, temp = 0, 0
			for i in range(matrix_grade): 	checked[0][i] = False

		for i in range(matrix_grade):
			for j in range(matrix_grade):
				checked[i][j] = False;



	return det
# A = [ [(randrange(5) + 1) for i in range(3)] for j in range(3)]

A = [ [1, 4, 5], [2, 5, 2], [5, 3, 3] ]
for a in A:
	print(a)
print(detA(A))


a = [1,2,3]
print(a)
del a[1]