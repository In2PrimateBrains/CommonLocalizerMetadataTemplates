import pandas as pd

def read_spreadsheet(file_path):
    spreadsheets = pd.read_excel(file_path, None)
    return spreadsheets

def format_entry(row):
    lines = []

    # Data level and requirement level
    if not pd.isna(row["DataLevel1"]):
        data_level = f"**{row['DataLevel1']}**"
        indent = ""
    elif not pd.isna(row["DataLevel2"]):
        data_level = f"**{row['DataLevel2']}**"
        indent = "  "
    else:
        data_level = f"**{row['DataLevel3']}**"
        indent = "    "

    requirement_level = f"*[{row['RequirementLevel']}]*"
    description = row["Description"]

    lines.append(f"{indent}- {data_level} {requirement_level}: {description}")

    # Example, Allowed Values, Comments
    if not pd.isna(row["Example"]):
        lines.append(f"{indent}  - Example: {row['Example']}")
    if not pd.isna(row["AllowedValues"]):
        lines.append(f"{indent}  - Allowed Values: {row['AllowedValues']}")
    if not pd.isna(row["Comments"]):
        lines.append(f"{indent}  - Note: {row['Comments']}")

    return "\n".join(lines)

def generate_markdown_file(df, sheet_name):
    content = []
    content.append(f"## {sheet_name}\n")
    
    for _, row in df.iterrows():
        content.append(format_entry(row))

    return "\n".join(content)

if __name__ == "__main__":
    file_path = "metadata_fields.xlsx"
    output_file = "metadata_fields.md"

    sheets = read_spreadsheet(file_path)

    with open(output_file, "w") as md_file:
        for sheetname in sheets:
            md_content = generate_markdown_file(sheets[sheetname], sheetname)
            md_file.write(md_content + "\n\n")
