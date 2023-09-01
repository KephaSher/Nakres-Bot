# The big setup code for bitmasks, estimate size 40M
from constants import *
import numpy as np

# ROOK

# 0000100000  -->  0000011111
# Do this later:  0000100000  -->  0000111111  for opposed colors
# HOL UP I COULD JUST DO ONE
# for pos in range(64):
#     for mask in range(1 << 8):
#         for mask2 in range(1 << 8):
#             (row, col) = (pos // 8, pos % 8)
#             ret1 = 0
#             ret2 = 0

#             # mask1 corresponds to row, mask2 to column

#             # start from the column, go left
#             for i in range(col-1, -1, -1):
#                 # if the ith digit from the left is 1
#                 if (mask1 >> (7 - i)) & 1:
#                     # ret1[i+1 : col] = 1
#                     ret1 |= ((1 << (col - (i+1))) - 1) << (8 - col)
#                        break
#             for i in range(col+1, 8):
#                 # if the ith digit from the left is 1
#                 if (mask1 >> (7 - i)) & 1:
#                     # ret1[col : i-1] = 1
#                     ret1 |= ((1 << (7 - col)) - 1) ^ ((1 << (8 - i)) - 1)
#                     break

MASK = np.zeros(8 * 256, dtype=int).reshape(8, 256)
for pos in range(8):
    for mask in range(1 << 8):
        # start from the column, go left
        for i in range(pos-1, -1, -1):
            # if the ith digit from the left is 1
            if (mask >> (7 - i)) & 1:
                MASK[pos][mask] |= ((1 << (pos - (i+1))) - 1) << (8 - pos)
                break

        for i in range(pos+1, 8):
            # if the ith digit from the left is 1
            if (mask >> (7 - i)) & 1:
                MASK[pos][mask] |= ((1 << (7 - pos)) - 1) ^ ((1 << (8 - i)) - 1)
                break

