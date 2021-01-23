import csv

class CSVFileProcessor:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def isValid(self):
        with open(self.file_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = list(csv.DictReader(csv_file))

            errors = []

            for row in csv_reader:
                if "barcode" not in row:
                    errors.append("barcode header missing")
                elif "sku" not in row:
                    errors.append("sku header missing")
                elif "size" not in row:
                    errors.append("size header missing")
                elif "product" not in row:
                    errors.append("product header missing")
                elif "design" not in row:
                    errors.append("design header missing")
                elif "season" not in row:
                    errors.append("season header missing")

                correct_headers = ['barcode', 'sku', 'size', 'product', 'design', 'season'] 

                for header in row:
                    if header not in correct_headers:
                        errors.append(header + " not in " + str(correct_headers))

            if len(errors) > 0:
                print(row)
                print("\n".join(errors))
                return False
            else:
                self.data = csv_reader
                return True


    def getData(self):
        if self.data:
            return self.data
        return None
