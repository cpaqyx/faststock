


records = [[111, 'aaa', True],                 #此处可以是List。
          [222, 'bbb', False],
          [333, 'ccc', True],
          [444, '中文', False]]

records.append([666, 'bbb', False])
row = []
row.append(777)
row.append('cccc')
row.append(True)

records.append(row)

records.append([])

print(records)