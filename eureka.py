# Function to get next value in the sequence
# Input:
#   digits - list of values
# Output:
#   new_digits - derived (next) list of values
def get_next(digits):
    new_digits = []
    count = 0
    prev = digits[0]
    for i in digits:
        if i == prev:
            count += 1
        else:
            new_digits.extend((count,prev))
            count = 1
            prev = i
    new_digits.extend((count,prev))
    return new_digits

def get_seq(value, N=2):
    seq = []
    for i in range(N):
        new_val = get_next(value)
        seq.append(new_val)
        value = new_val
    return seq

def get_ratio_list(seq):
    ratio_list = []
    for i in range(len(seq)):
        ratio_list.append(len(seq[i])/len(seq[i-1]))
    return ratio_list

values = []
values.append(1)
values.append([1,1])
res = get_next(values)
print(res)