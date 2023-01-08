## Eliminar 1 columna en un dataframe

df = pd.dataFrame([])
df.drop('COLUMN_NAME', inplace=True, axis=1)

# LISTA LAS COLUMNAS
print(df.columns.tolist())

# RENOMBRAR COLUMNA
df.columns.values[0] = "NEW NAME"

# FILTRO PAPELUCHO y luego cambio la columna al index para el clustering

def filter_by_value(csv_file, column, value):
    df = pd.read_csv(csv_file, index_col=0)
    df2 = df[df[column].str.contains(value)]
    print(df2)
    return df2


df = filter_by_value('clusteringFiles/data_all_books_scaled_book.csv', "book", 'Papelucho')
# COLUMNA A INDEX
df = df.set_index('book')

# ELIMINAR PRIMERA COLUMNA
df.drop(columns=df.columns[0], axis=1, inplace=True)


# Create a new column with index values
df['index_column'] = df.index

#using reset_index() to set index into column
df2=df.reset_index()

# INDEX A COLUMNA
#Using reset_index, inplace=True
df.reset_index(inplace=True)


# TO LIST
df = df[["positive"]]

df_list = df.values.tolist()

# QUERY ON DATAFRAME
retorna un df

df.query('Gender=="Male" & Year=="2014" ')

If you have to use df.query(), the correct syntax is:

df.query('column_name.str.contains("abc")', engine='python')
You can easily combine this with other conditions:

df.query('column_a.str.contains("abc") or column_b.str.contains("xyz") and column_c>100', engine='python')


# GET FREQUENCY
Use value_counts() as @DSM commented.

In [37]:
df = pd.DataFrame({'a':list('abssbab')})
df['a'].value_counts()

Out[37]:

b    3
a    2
s    2
dtype: int64
Also groupby and count. Many ways to skin a cat here.

In [38]:
df.groupby('a').count()

Out[38]:

   a
a   
a  2
b  3
s  2

[3 rows x 1 columns]
See the online docs.

If you wanted to add frequency back to the original dataframe use transform to return an aligned index:

In [41]:
df['freq'] = df.groupby('a')['a'].transform('count')
df

Out[41]:

   a freq
0  a    2
1  b    3
2  s    2
3  s    2
4  b    3
5  a    2
6  b    3

[7 rows x 2 columns]