import pandas as pd
import numpy as np
import unittest
import os

# These only ever run once, to initialize the variables.
final_nums = {}
sizedf = {}

# Reads in a DataFrame and converts sizes to decimals
def size_conv(items):
  size_dict = {
    'YS': 1,
    'YM': 2,
    'YL': 3.5,
    'YXL': 3.75,
    'AXS': 3.5,
    'AS': 4,
    'AM': 5,
    'AL': 6,
    'AXL': 7,
    'A2XL': 8
  }
  items = items.replace({'Size': size_dict})
  return items

def jmatch(data, people):
  tol = 0
  while (tol <= 4):
    for player in people.iterrows(): # For each player
      size_diff = data[1] - player[1][1] # Find the difference between player size and uniform size
      if (abs(size_diff) <= tol): # If close enough <<and not data[0] in final_nums.values()>> - removes dupes
        final_nums[player[1][0]] = data[0] # Add it to the roster of numbers
        final_nums['Mismatch Score'] += abs(size_diff) # Track overall mismatch score
        return people.drop(player[0]) # Remove the player from the list of players needing jerseys
    tol += 0.25
  return people # Case to catch a uniform without a match

# Begins matching uniforms to players in prio of least available sizes first.
def smatch(sizelist, ps):
  for size in sizelist: # For all of the sizes of uniforms available,
    for uniform in sizedf[size].iterrows(): # For each uniform of that size,
      unidata = uniform[1] # Grab the uniform size & number
      ps = jmatch(unidata, ps) # Match the uniform to a player and remove from list if possible
  return ps

def assign(inv_file, player_file):
  inventory = size_conv(pd.read_csv(inv_file))
  players = size_conv(pd.read_csv(player_file))

  for size in inventory['Size'].unique():
    sizedf[size] = inventory.loc[inventory['Size'] == size]
  lp = sorted(sizedf, key = lambda x:sizedf[x].shape[0]) # Holds the list of all sizes sorted in ascending qty available

  # As players are assigned uniforms, remove the uniforms from the inventory
  # Once all the players have been assigned a uniform, then return the list of names -> numbers
  players = smatch(lp, players)
  return players

def uniform_full_match(inv, roster):
  final_nums.clear() # Removes previous team numbers, resets MMS
  sizedf.clear() # Resets the size dataframe as well
  final_nums['Mismatch Score'] = 0
  players = assign(inv, roster)
  return final_nums if players.empty else {'Mismatch Score': np.nan}

class FunctionalityTester(unittest.TestCase):
  # Ensures that the size converter works in the expected way, no outliers / extreme testing.
  def test_size_converter_proper_inputs(self):
    test_data = [['T1', 'AS'], ['T2', 'YM']]
    res_data = [['T1', 4], ['T2', 2]]
    t_df = size_conv(pd.DataFrame(test_data, columns=['Name', 'Size']))
    r_df = pd.DataFrame(res_data, columns=['Name', 'Size'])
    pd.testing.assert_frame_equal(t_df, r_df)

if __name__ == '__main__':
  unittest.main()