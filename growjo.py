import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By

# path = f'/Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/NDA_Profile'
options = uc.ChromeOptions()
driver = uc.Chrome(headless=False, use_subprocess=True)

# startRow = 0
startRow = 3468
# for i in range(21, 200):
for i in range(89, 201):
  driver.get(url=f"https://growjo.com/home/{i}")
  df = driver.find_element(By.CSS_SELECTOR, '.jss31.cstm-table')
  # print(df.get_attribute("outerHTML"))
  dfs = pd.read_html(df.get_attribute("outerHTML"))
  df = dfs[0]
  df2 = df[['Rank','Company', 'City', 'Country', 'Funding', 'Industry', 'Employees', 'Revenue', 'Emp Growth %']]
  # x = dfs[0]
  print(dfs)
  #df2.to_excel('./output/growjo.xlsx', startrow=startRow, header=None, index=False)
  # df2.append_df
  with pd.ExcelWriter('./output/growjo.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:  
    df2.to_excel(writer, header=False, index=False, startrow=startRow)
  startRow += 51
  print (f"Finished page: {i}, Next is: {i+1}, Next record start @: {startRow}")

  # data = {'EmployeeID': [101, 102, 103],
  #         'EmployeeName': ['Alice', 'Bob', 'Charlie'],
  #         'Salary': [60000, 70000, 80000]}


# df_new = pd.DataFrame(data)

# with pd.ExcelWriter('existing_file.xlsx', engine='openpyxl', mode='a') as writer:
#     # Write the new DataFrame to a new sheet
#     df_new.to_excel(writer, sheet_name='New Sheet', index=False)