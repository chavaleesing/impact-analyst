import glob
import os


def get_not_match_on_ms():
    folder_patterns = ['../repo/bo/*/src/main/*', '../repo/others/*/src/main/*']
    folder_patterns = ['../repo/orchestrator/*/src/main/java/com/ktb/wp/batch/controller/*']
    # folder_patterns = ['../repo/orchestrator/*/src/main/java/*']
    # folder_pattern = '../*/*/*/src/main/*'
    matching_folders = []
    for folder_pattern in folder_patterns:
        matching_folders.extend(glob.glob(folder_pattern))
    keywords = ["/v1"]
    for kw in keywords:
        all_paths = set()
        for file_path in matching_folders:
            is_match = False
            if not file_path.endswith(".java"):
                print(f"this is folder : {file_path}")
                continue
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, 1):
                    if kw in line:
                        is_match = True
                if not is_match:
                    all_paths.add(file_path)
    
        print("---------------------------------------------")
        print(f"keyword = {kw}")
        batches = set([i.split("/")[3] for i in all_paths])
        for batch in batches:
            print(batch)

def get_general_match():
    folder_patterns = ['../repo/bo/*/src/main/*', '../repo/others/*/src/main/*']
    folder_patterns = ['../repo/batch/*/src/main/*', '../repo/processor/*/src/main/*', '../repo/orchestrator/*/src/main/*']
    # folder_pattern = '../*/*/*/src/main/*'
    matching_folders = []
    for folder_pattern in folder_patterns:
        matching_folders.extend(glob.glob(folder_pattern))
    keywords = ["/api/campaign-inquiry/v1/dropdown-lists", 
        "/api/customer-override-ekyc/v1/customer", 
        "/api/customer-privilege-status-update/v1/customer-privilege/status", 
        "/api/company-profile-registration/v1/company", 
        "/api/all-privilege-inquiry/v1/privileges", 
        "/api/settlement-group-inquiry/v1/payment", 
        "/api/redemption/v1/redemption", 
        "/api/privilege-list-inquiry/v1/privileges", 
        "/api/settlement-result/v1approve", 
        "/api/void/v1/reverse/void", 
        "/api/void/v1void", 
        "/api/consent/v1/customer-consent", 
        "/api/transaction-inquiry/v1/transactions", 
        "/api/settlement-overall-report/v1/payment", 
        "/api/campaign-registration/v1privilege", 
        "/api/settlement-detail-inquiry/v1/payment", 
        "/api/payment-summary-inquiry/v1/summary", 
        "/api/company-supported-privilege-inquiry/v1/companies", 
        "/api/privilege-profile-inquiry/v1/privilege-profile", 
        "/api/settlement-transfer-tracking/v1/payment", 
        "/api/privilege-inquiry/v1/privilege", 
        "/api/settlement-group-result/v1approve", 
        "/api/settlement-group/v1/config", 
        "/api/company-inquiry/v1/companies", 
        "/api/customer-details-inquiry/v1/customer", 
        "/api/customer-details-inquiry/v1/cid-validate", 
        "/api/company-inquiry/v1/companies", 
        "/api/transaction-inquiry/v1/transactions", 
        "/api/transaction-inquiry/v1/lists", 
        "/api/batch-interface/v1batch", 
        "/api/batch-interface/v1status"]
    keywords = ["org.springframework.data.redis.core.redistemplate"]
    for kw in keywords:
        all_paths = set()
        for folder in matching_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, 1):
                            if kw in line.lower():
                                all_paths.add(file_path)
                                print(f"service: {file_path.split("/")[3]} | {line}")
    
        print("---------------------------------------------")
        print(f"keyword = {kw}")
    print("Summary ~~~~~~~~")
    batches = set([i.split("/")[3] for i in all_paths])
    for batch in batches:
        print(batch)

def get_general_match_as_batches():
    # folder_patterns = ['../repo/bo/*/src/main/*', '../repo/others/*/src/main/*']
    result = dict()
    folder_patterns = ['../repo/batch/*/src/main/*', '../repo/processor/*/src/main/*']
    matching_folders = []
    for folder_pattern in folder_patterns:
        matching_folders.extend(glob.glob(folder_pattern))
    keywords = ['"cid"', '"firstname_th"', '"midname_th"', '"lastname_th"', '"firstname_en"', '"midname_en"', '"lastname_en"', '"mobile_number"', '"address_number"',  
                '"village_building_name"',  '"floor"',  '"village_no"',  '"alley"',  '"junction"',  '"road"',  
                
                '"bank_account_no"',  '"tax_id"',  
                
                '"from_account"',  '"to_account"',  
                
                '"company_tax_id"']
    for kw in keywords:
        result[kw] = set()
        all_paths = set()
        for folder in matching_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "entity" not in file_path:
                        continue
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, 1):
                            if kw in line:
                                all_paths.add(file_path)
                                result[kw].add(file_path.split("/")[3])
    # print(result)

    result2 = dict()
    for k, v in result.items():
        for ms in v:
            if ms not in result2:
                result2[ms] = set()
            result2[ms].add(k)
    print(result2)
    for k,v in result2.items():
        print(k)
        for i in v:
            print(i)
        print()
        print(".......................")

    from openpyxl import Workbook
    import collections

# Original dictionary
    data = collections.OrderedDict(sorted(result2.items()))

    # Create a new workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    # Write the column headers (keys of the dictionary)
    headers = list(data.keys())
    ws.append(headers)  # Add the headers as the first row

    # Find the maximum number of columns we need to add (max length of sets)
    max_rows = max(len(values) for values in data.values())

    # Create rows by transposing the data
    for i in range(max_rows):
        row = []
        for key in headers:
            values = list(data[key])
            if i < len(values):
                row.append(values[i])
            else:
                row.append('')  # If a column has fewer rows, fill the rest with empty cells
        ws.append(row)

    # Save the workbook to an Excel file
    wb.save("output.xlsx")

    print("Excel file 'output.xlsx' has been created successfully!")

    # batches = set([i.split("/")[3] for i in all_paths])
    # for batch in batches:
    #     print(batch)


def list_folders_in_path(path):
    # List all folders in the specified path
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


def list_all_orches_endpoint():
    result = dict()
    with open('result.txt', 'w') as wfile: 
        folder_pattern = '../repo/orchestrator/customer-consent-orchestrator/src/main/java/com/ktb/wp/batch/controller/*'
        folder_pattern = '../repo/orchestrator/*/src/main/**/controller/*'
        matching_folders = glob.glob(folder_pattern, recursive=True)

        for file_path in matching_folders:
            # print(f"\n--------\nMS = {file_path.split("/")[3]}")
            if result.get(file_path.split("/")[3], None) is None:
                result[file_path.split("/")[3]] = []
            if not file_path.endswith(".java"):
                # print(f"this is folder : {file_path}")
                continue
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                url = "< url >"
                for line_num, line in enumerate(lines, 1):
                    if "v1" in line:
                        url = line.split('"')[-2]
                    if "@GetMapping" in line or "@PostMapping" in line:
                        wfile.write(line)
                        if len(line.split("\"")) >= 2:
                            print(url + line.split("\"")[-2])
                            result[file_path.split("/")[3]].append(url + line.split("\"")[-2])
                        else:
                            print(url + line)
                            result[file_path.split("/")[3]].append(url + line)
                        if url == "< url >":
                            eeee=1
    print(",,,,,,,,,,,,,")
    # for k, v in result.items():
    #     for vv in v:
    #         print(vv)
        # print(f"{k} = {v}")



def list_all_endpoint():
    temp = set()
    with open('result.txt', 'w') as wfile: 
        folder_pattern = '../repo/processor/*'
        matching_folders = glob.glob(folder_pattern)
        for folder in matching_folders:
            wfile.write(f"\n\n-------- {folder.split("/")[-1]}")
            # print(f"-------- {folder.split("/")[-1]}")
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not "controller" in file_path or "test" in file_path:
                        continue
                    url = "<url>"
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, 1):
                            if folder.split("/")[-1] in line and ' "' in line:
                                wfile.write(line)
                                # print(line)
                                # print(f"{line.split('"')[-2]}")
                                url = line.split('"')[-2]
                            if "@GetMapping" in line or "@PostMapping" in line:
                                wfile.write(line)
                                if len(line.split("\"")) >= 2:
                                    print(url + line.split("\"")[-2])
                                else:
                                    print(url + line)
                                    temp.add(folder.split("/")[-1])
    print(f"\n\n{temp}")

print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
get_general_match_as_batches()
# list_all_endpoint()


