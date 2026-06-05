import pandas as pd


df = pd.read_csv("messy_data.csv")
print("Shape:", df.shape)
print(f"Missing values are: {df.isnull().sum()}")

df = df.dropna(how="all")

df = df.drop_duplicates(subset=["name", "age", "salary"])

df["name"] = df["name"].str.strip().str.title()
df["department"] = df["department"].str.strip().str.title()
df["department"] = df["department"].replace('Hr', "HR")

df["department"] = df["department"].replace("", pd.NA)

df["salary"] = df["salary"].fillna(df["salary"].median())
df["age"] = df["age"].fillna(df["age"].median())

df= df.dropna(subset=["name", "department"])

df["join_date"] = pd.to_datetime(df["join_date"])

print("Final Shape", df.shape)
print("Total Missing value\n ",df.isnull().sum())

df.to_csv("clean_employees.csv", index=False)