import assignor
import os
import json
import numpy as np
import pandas as pd
import unittest

path = os.path.dirname(os.path.realpath(__file__))
inv = path + '\\Uniforms'
rosters = path + '\Teams'
uni_dict = {}

# Calculates the erasure scores for each combination of bin and team
def erasure_gen(arr):
  erasure_arr = np.copy(arr)
  row_vector = np.nansum(arr, axis=1)
  col_vector = np.nansum(arr, axis=0)
  for row in range(arr.shape[0]):
    for col in range(arr.shape[1]):
      erasure_arr[row][col] = np.nansum([row_vector[row], col_vector[col], 2*arr[row][col]]) * arr[row][col]
  return erasure_arr

assignment_dict = {}

# Iterates over all the bins in the uniform inventory
for uni_bin in os.scandir(inv):
  uni_dict[uni_bin.name] = {}
  # Iterates through all teams
  for team in os.scandir(rosters):
    # Assigns uniform numbers to players, determines the mismatch score (MMS) per team for a specific bin
    team_nums = assignor.uniform_full_match(uni_bin, team)
    # Records the MMS indexed at (Team, Bin)
    uni_dict[uni_bin.name][team.name] = team_nums['Mismatch Score']
    assignment_dict[uni_bin.name + team.name] = dict(team_nums)

# Generates a matrix of MMS for bin-team pairings
uni_matrix = pd.DataFrame(uni_dict)
team_idx = list(uni_matrix.index)
bin_idx = list(uni_matrix.columns)

# Begin numpy work with matrices
np_matrix = uni_matrix.to_numpy()
erasures = erasure_gen(np_matrix)

pd.DataFrame(erasures).to_csv(rf'{path}/erasures.csv', sep=',', mode='w')

while erasures.size > 0:
  index = np.unravel_index(np.argmax(erasures), np.shape(erasures))
  erasures = np.delete(np.delete(erasures, index[0], 0), index[1], 1)

  # Select the team-bin combination with the largest erasure score, remove it from the list, print the numbers
  team = team_idx.pop(index[0])
  ubin = bin_idx.pop(index[1])
  print(team, ubin)
  print(json.dumps(assignment_dict[ubin + team], indent=2))

uni_matrix.to_csv(rf'{path}/tablevis.csv', sep=',', mode='w')


# class HighLevelTester(unittest.TestCase):
#   def full_match_test(self):
#     print('okay')

# if __name__ == '__main__':
#   unittest.main()