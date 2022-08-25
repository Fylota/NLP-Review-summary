import pandas as pd

mapping_dict = {['a', 'b', 'c', 'd']:'A',
                ['aa', 'bb', 'cc']:'B'}

df = pd.DataFrame(pd.Series(mapping_dict).reset_index()).set_axis(['keywords','text'],1,inplace=False)
print(df)
