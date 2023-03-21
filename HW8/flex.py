import pandas as pd
import os
import flexmatcher
# The mediated schema has three attributes:
# name, website, headquarter, ceo, founded, employees, 
# market_value, market_capitalization, annual_revenue, business

# creating one sample DataFrame where the schema is (year, Movie, imdb_rating)
vals1_path = os.path.join('datasets', 'DDD-teamblind.com.csv')
vals1 = pd.read_csv(vals1_path, encoding = "ISO-8859-1", index_col=[0])
header = vals1.columns.values.tolist()
data1 = pd.DataFrame(vals1)
# specifying mapping between schema of the dataframe and the mediated schema
data1_mapping = {'name': 'name',
                'website': 'website',
                'locations': 'headquarter',
                'size': 'employees',
                'industry': 'business',
                'founded': 'founded'}

# creating another sample DataFrame where the schema is
# (title, produced, popularity)
vals2_path = os.path.join('datasets', 'output_disfold.csv')
vals2 = pd.read_csv(vals2_path, encoding = "ISO-8859-1")
header = vals2.columns.values.tolist()
data2 = pd.DataFrame(vals2, columns=header)
# specifying mapping between schema of the dataframe and the mediated schema
data2_mapping = {'name': 'name',
                'market_cap': 'market_capitalization',
                'country': 'headquarter',
                'employees': 'employees',
                'industry': 'business',
                'founded': 'founded',
                'ceo': 'ceo',
                'stock': '',
                'sector': '',
                'headquarters': ''}

# creating a list of dataframes and their mappings
schema_list = [data1, data2]
mapping_list = [data1_mapping, data2_mapping]

# creating the third dataset (which is our test dataset)
# we assume that we don't know the mapping and we want FlexMatcher to find it.
vals3_path = os.path.join('datasets', 'wiki.csv')
vals3 = pd.read_csv(vals3_path, encoding = "ISO-8859-1")
header = vals3.columns.values.tolist()
data3 = pd.DataFrame(vals3, columns=header)


# Using Flexmatcher
fm = flexmatcher.FlexMatcher(schema_list, mapping_list, sample_size=100)
fm.train()                                           # train flexmatcher
predicted_mapping = fm.make_prediction(data3)

# printing the predictions
print ('FlexMatcher predicted that "rt" should be mapped to ' +
       predicted_mapping['rt'])
print ('FlexMatcher predicted that "yr" should be mapped to ' +
       predicted_mapping['yr'])
print ('FlexMatcher predicted that "id" should be mapped to ' +
       predicted_mapping['id'])