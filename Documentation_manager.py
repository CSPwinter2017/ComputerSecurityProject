import csv


class DocumentationManager(object):

    def __init__(self, csvPath, filednames):
        self.csvPath = csvPath
        self.filednames = filednames
        with open(self.csvPath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, self.filednames)
            writer.writeheader()

    def write_packet_to_csv(self, row):
        with open(self.csvPath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, self.filednames)
            writer.writerow(row)


    # def parse_dns_packet(self, pkt):
    #     res = {}
    #     for