import pandas as pd
import unittest
import os

final_nums = {'Mismatch Score': 0}
sizedf = {}

def jmatch(data, people):
  for player in people.iterrows():
    score_size = data[1] - player[1][1]
    if (-0.5 <= score_size <= 1) and not data[0] in final_nums.values(): # If the player's jersey size matches the uniform size,
      final_nums[player[1][0]] = data[0] # Add it to the roster of numbers
      final_nums['Mismatch Score'] += abs(score_size)
      return people.drop(player[0]) # Remove the player from the list of players needing jerseys
  return people # Case to catch a uniform without a match

# Begins matching uniforms to players in prio of least available sizes first.
def smatch(sizelist, ps):
  for size in sizelist:
    for uniform in sizedf[size].iterrows():
      unidata = uniform[1]
      ps = jmatch(unidata, ps) # matches a jersey to a player, removes the player from the needed list
  return ps

def assign(inv_file, player_file):
  inventory = size_score(pd.read_csv(inv_file))
  players = size_score(pd.read_csv(player_file))

  for size in inventory['Size'].unique():
    sizedf[size] = inventory.loc[inventory['Size'] == size]
  lp = sorted(sizedf, key = lambda x:sizedf[x].shape[0]) # Holds the list of all sizes sorted in ascending qty available

  # As players are assigned uniforms, remove the uniforms from the inventory
  # Once all the players have been assigned a uniform, then return the list of names -> numbers
  players = smatch(lp, players)
  return players

# Reads in a DataFrame and converts sizes to decimals
def size_score(items):
  size_dict = {
    'YS': 1,
    'YM': 2,
    'YL': 3.5,
    'YXL': 3.75,
    'AXS': 3.5,
    'AS': 4,
    'AM': 5,
    'AL': 6,
    'AXL': 8,
    'A2XL': 9
  }
  items = items.replace({'Size': size_dict})
  return items

def uniform_full_match(inv, roster):
  mismatch = 0
  players = assign(inv, roster)
  if players.empty or mismatch >= 5:
    print("Team fully outfitted!")
  else:
    print("Team unable to be outfitted")
  return final_nums if players.empty else {}

class FunctionalityTester(unittest.TestCase):
  # Ensures that the size converter works in the expected way, no outliers / extreme testing.
  def test_size_converter_proper_inputs(self):
    test_data = [['T1', 'AS'], ['T2', 'YM']]
    res_data = [['T1', 4], ['T2', 2]]
    t_df = size_score(pd.DataFrame(test_data, columns=['Name', 'Size']))
    r_df = pd.DataFrame(res_data, columns=['Name', 'Size'])
    pd.testing.assert_frame_equal(t_df, r_df)

if __name__ == '__main__':
  unittest.main()