# st = 'abcabcdfeacd'
# def longest_subestring(s):
#     start = 0
#     max_length = 0
#     length = 0
#     for end in range(1,len(s)+1):
#         if len(s[start:end]) == len(set(s[start:end])):
#             length +=1
#             print(s[start:end],set(s[start:end]))
#         else:
#             print(s[start:end],set(s[start:end]))
#             start+=1
#             end = end
            
#         if length > max_length:
#             max_length = length
#         # print(length)
            
# print(longest_subestring(st))


# print(map(lambda x,y:x+y,[1,2],[3,4]))
l =[11,2,3,4,5,6,7,8,9]
print(list(filter(lambda x : x == 0,l)))


d1 ={'G':'g','E':'e','N':'n'}
d2 = {'T':'t','I':'i'}

print(list(d1.values()))
