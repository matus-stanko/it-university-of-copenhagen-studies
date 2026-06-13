from collections import Counter

def search_pascal_multiples_fast(row_limit):
    # Implement your fast function here. Feel free to copy-paste and then change the slow function from below, or to completely re-implement the function from scratch. 
    def triangle(rows):
        triangle_list = []
        for i in range(rows):   #i - row of rows
            temp_list=[] 
            for j in range(i+1):        #j - column of row i
                if j == 0 or j == i:   #if column first or last
                    temp_list.append(1)  #add number 1 
                else:
                    temp_list.append(triangle_list[i-1][j-1] + triangle_list[i-1][j])  #triangle_list[i-1][j-1] - number of last row previous column + triangle_list[i-1][j] - last row actual column
            triangle_list.append(temp_list) #add actial row of number to triangle_list
        return triangle_list
    
    def edit_triangle(rows):
        if rows <= 15:   #there are no number that will repeat at least 3 times until 16 rows
            return []   # so return empty list
        else:
            tr = (triangle(rows))   #get triangle
            del tr[:4]      #get rid of outermost numbers in first rows. 
            for i in range(len(tr)): 
                tr[i] = tr[i][2:-2]   #get rid of the first 2 and last 2 numbers (outermost numbers)
        return tr

    flat_list = [item for sublist in edit_triangle(row_limit) for item in sublist]  #make a flat list from nested list
    counts = Counter(flat_list)   #make a dictionary with counts of each elements

    list_of_numbers = []
    for num, count in counts.items():  #iterate dictionary
        if count >= 3:   #if count is >=3
            list_of_numbers.append(num)
    return list_of_numbers

#----------- DO NOT CHANGE ANYTHING BELOW THIS LINE


def search_pascal_multiples_slow(row_limit):

    # Building up Pascal's triangle with a dict of lists
    ptriangle = {}
    ptriangle[0] = [1]
    ptriangle[1] = [1,1]
    ptriangle[2] = [1,2,1]
    for r in range(3, row_limit):
        ptriangle[r] = []
        for i in range(len(ptriangle[r-1])+1):
            if i == 0: # on left border, so we just add 1
                ptriangle[r].append(1)
            elif i == len(ptriangle[r-1]): # on right border, so we just add 1
                ptriangle[r].append(1)
            else: # not on border, so we sum up the two numbers above
                ptriangle[r].append(ptriangle[r-1][i-1] + ptriangle[r-1][i])

    # Putting all numbers into one list, except the outermost 2 numbers in each row
    number_list = []
    for r in range(row_limit):
        row = ptriangle[r]
        for i, number in enumerate(row):
            if i > 1 and i < len(row)-1: # exclude the outermost 2 numbers in each row
                number_list.append(number)

    # Counting the numbers
    number_set = set(number_list) 
    pascal_multiples = []
    for unique_number in number_set:
        count = 0
        for number in number_list:
            if number == unique_number:
                count = count + 1
        if count > 3:
            pascal_multiples.append(unique_number)
    
    return sorted(pascal_multiples)


from timeit import default_timer as timer

def main():
	row_limit = 250

	start = timer()
	print(search_pascal_multiples_slow(row_limit))
	end = timer()
	runtime_slow = end-start

	start = timer()
	print(search_pascal_multiples_fast(row_limit))
	end = timer()
	runtime_fast = end-start

	print(round(runtime_slow / runtime_fast, 2))

if __name__ == "__main__":
	main()