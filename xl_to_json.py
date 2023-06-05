import pandas as pd
import json

excel_file = "Laminates_all_Category_data-29-05-2023-19-56.xlsx"
df = pd.read_excel(excel_file, sheet_name="Sheet 1")
cols = ["Brand", "subCategory", "color", "finish", "tags", "offerImageUrl_1"]
df = df[cols]
df["subCategory"] = df["subCategory"].apply(
    lambda x: x.lower().replace("laminates", "").strip()
)
df["tags"] = df["tags"].apply(lambda x: x.split(","))

data = df.to_dict(orient="records")
with open("laminates.json", "w") as f:
    json.dump(data, f)
