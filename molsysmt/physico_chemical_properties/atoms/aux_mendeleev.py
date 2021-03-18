from mendeleev import get_table
df = get_table('elements')


# Weight

file_name = 'weight'

fff = open(file_name + '.py', 'w')

dict_name = 'weight'

fff.write(dict_name + ' = {\n')

for ii in range(117):
    fff.write('\t"{}" : {},\n'.format(df.symbol[ii], df.atomic_weight[ii]))
fff.write('\t"{}" : {}\n'.format(df.symbol[117], df.atomic_weight[117]))

fff.write('}\n')

fff.close()




















