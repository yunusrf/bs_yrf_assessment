# Python program to find top 'total_frequent_numbers' elements in an array
# Given an integer array 'array_nums' and an integer 'total_frequent_numbers', return the 'total_frequent_numbers' most frequent elements.

class Exercise_4_Solution:

    """ 
    Complexity Analysis using the big O notation: 
    Time Complexity: O( n * k ). ( where n = length of input array and k is length of array_nums)
        In each traversal the temp array of size k (length of array_nums) is traversed, So the time Complexity is O( n * k ).
    Space Complexity: O(n). 
        To store the elements O(n) space is required.
    """

    def FrequencyTopK(self, array_nums, total_frequent_numbers: int):
        output_format = []
        res = []
        counts = {}
 
        len_input = int(len(array_nums))
        if total_frequent_numbers > len_input:
            print(f'Number of K most frequent elements must be less than length of input array')
            return res,output_format
        for i in range(0, len(array_nums)):
            counts[array_nums[i]] = 1 + counts.get(array_nums[i], 0)
        frequency = [[] for i in range(0, len(array_nums) + 1)]
        for value, count in counts.items():
            frequency[count].append(value)

        # print(f'Frequency Array - {frequency}')
       
        try:
            len_frequency = int(len(frequency))
            for i in range(len_frequency - 1, 0, -1):
                for n in frequency[i]:
                    res.append(n)
                    if i == 1:
                        element = f'{n} : {i} time'
                    else:
                        element = f'{n} : {i} times'    

                    output_format.append(element)
                    total_frequent_numbers -= 1
                    if total_frequent_numbers == 0:
                        # print(output_format)
                        return res,output_format
            
        except Exception as e:
                print(e)
        return res,output_format                               

if __name__ == '__main__':

    obj_frequency_ktop = Exercise_4_Solution()
    array_test_1 = [9, 4, 2, 1, 1, 3, 8, 4, 2, 9, 2]
    array_test_2 = [ 15, 12, 11, 13, 12, 15, 16, 17,100 ]
    top_counter = 3
    res,output_format = obj_frequency_ktop.FrequencyTopK(array_test_1,top_counter)
    print(f'Input Array  to get top {top_counter} - {array_test_1}')
    # print(res)
    print(output_format)

    top_counter = 5
    print(f'Input Array  to get top {top_counter} - {array_test_2}')
    res,output_format = obj_frequency_ktop.FrequencyTopK(array_test_2,top_counter)
    # print(res)
    print(output_format)



