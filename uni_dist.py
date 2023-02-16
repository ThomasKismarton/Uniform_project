import assignor
import os
path = os.path.dirname(os.path.realpath(__file__))
inv = path + '\\Uniforms'
roster = path + '\Teams\B11_Green.csv'

for uni_bin in os.scandir(inv):
  team_nums = assignor.uniform_full_match(uni_bin, roster)
  for entry in team_nums:
    print('--------------------------------')
    print(f'{entry:<25} |', team_nums[entry])
