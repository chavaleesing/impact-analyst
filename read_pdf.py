import PyPDF2

def validate_text(content, keyword):
    if keyword not in content:
        return False

def validate_count_keyword(content: str, expect_count, keyword) -> bool:
    count = 0
    for line in content.split('\n'):
        count += 1 if keyword in line else 0
    return count == expect_count

def read_pdf(file_path):
    comp_code = "50A0200001" # get from DB ....
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        # for page_num in range(len(reader.pages)):
        #     page = reader.pages[page_num]
        #     page_text = page.extract_text()
        #     if page_text:
        #         lines = page_text.split('\n')
        #         for line in lines:
        #             print(line)
        # page = reader.pages[0]
        # page_text = page.extract_text()
        # print(f"{page_text} \n\n\n\n\n ------ \n\n")
        # print(reader.pages[1].extract_text())
        # for page_num in range(len(reader.pages)):
        page = reader.pages[0]
        page_text = page.extract_text()
        all_lines = page_text.split("\n")
        line_matches = [line for line in all_lines if comp_code in line]
        print(line_matches)

        # lines = page_text.split('\n')
        # for line in lines:
        #     print(line)




pdf_text = read_pdf("test_pdf.pdf")
print(pdf_text)

