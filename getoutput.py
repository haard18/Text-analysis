import pandas as pd
df=pd.read_csv('analysis_results.csv')
# Selecting the desired columns in the specified order
selected_columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE','SUBJECTIVITY SCORE',
    'AVERAGE SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE COUNT PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

df_selected = df[selected_columns]

# Write the selected columns to an Excel file
df_selected.to_excel('Output.xlsx', index=False)

print("CSV file converted to Excel format successfully!")