import csv


class Methods_List():
    def __init__(self):
        print("test")

    def csv_create(self, filepath):
        with open(filepath, 'x') as file:
            pass
    def csv_read(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file, delimiter = ',')

            alldata = []
            for row in reader:
                alldata.append(row)
            return alldata

    def csv_data_add(self, filepath, datalist):
        with open(filepath, 'a', newline = '') as file:
            sis_name = datalist

            writer = csv.writer(file, delimiter = ',')
            writer.writerow(sis_name)

    def csv_data_edit(self, filepath, datalist):
        with open(filepath, 'w', newline='') as file:

            writer = csv.writer(file, delimiter = ',')

            for item in datalist:
                writer.writerow(item)


    def csv_data_delete(self, filepath, index):
        datalist = self.csv_read(filepath)
        datalist.pop(index)

        self.csv_data_edit(filepath, datalist)

    def read_course_csv(filename):
        data = []
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
           
            for row in csv_reader:
                data.append(row[0])
        return data
