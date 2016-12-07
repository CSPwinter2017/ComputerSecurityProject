import csv
from scapy.layers.inet import *


class DocumentationManager(object):
    def __init__(self, csvPath, filednames):
        self.csvPath = csvPath
        self.filednames = filednames
        with open(self.csvPath, 'a') as csvfile:
            headers = []
            for filed in filednames:
                headers.append(str(filed).split(".")[-1].replace(">", '').replace("'", ''))
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

    def write_row_to_csv(self, row):
        with open(self.csvPath, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, self.filednames)
            writer.writerow(row)

    def write_pkt_to_csv(self, pkt):
        self.write_row_to_csv(self.parse_dns_packet(pkt))

    def parse_dns_packet(self, pkt):
        res = {}
        for filed in self.filednames:
            res[filed] = pkt[filed]
        return res

if __name__ == '__main__':
    row = {IP: "IP", UDP: "DUP"}
    DocumentationManager("./test.csv", [IP, UDP]).write_row_to_csv(row)
