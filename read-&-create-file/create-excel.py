import pandas as pd
import xlsxwriter


def main():

    while True:
        try:
            print("Nhập file cần chuyển:")
            file_path = input()
            file = pd.read_excel(file_path, sheet_name="Sheet1")
            break
        except:
            continue

    newFile = file.to_numpy().tolist()

    arrayNames, arrayPoints, arrayRanks = [], [], []

    for el in newFile:
        average = (float(el[1]) + float(el[2])) / 2

        arrayNames.append(el[0])
        arrayPoints.append(average)

        if average >= 8:
            arrayRanks.append("Giỏi")
        elif average > 5 and average < 8:
            arrayRanks.append("Khá")
        else:
            arrayRanks.append("Trung Bình")

    data = {"Tên": arrayNames, "Điểm trung bình": arrayPoints, "Xếp loại": arrayRanks}

    df = pd.DataFrame(data)

    print("--------------")
    print("Nhập file mới:")
    newInput = input()

    writer = pd.ExcelWriter(newInput, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    border_fmt = workbook.add_format({"bottom": 2, "top": 2, "left": 2, "right": 2})
    worksheet.conditional_format(
        xlsxwriter.utility.xl_range(0, 0, 0, len(df.columns) - 1),
        {"type": "no_errors", "format": border_fmt},
    )
    writer._save()

    print("---------------> Chuyển file thành công! <---------------")


if __name__ == "__main__":
    main()
