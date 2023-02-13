from dnslib.dns import *
# d = DNSRecord.question("twitter.com")

# print(str(d.get_q()).strip(';').split())


# m2 = d.pack()
# print("\n\n\n",m1)
# print("\n\n___________________\n",m2)

# m3 = DNSRecord.parse(m2)
# print(m3)

value = "google.com"
key = "ns1.cse.du.ac.bd"
d = DNSRecord(
        DNSHeader(qr=1,aa=1,ra=0),
        q=DNSQuestion("abc.com"),
        a=RR(value,QTYPE.NS,rdata=NS(key))
    )

# print(d)

m1 = str(d.get_a()).split()
print(m1)

# def get_queryType(qtype,value):
#     if qtype == 'A':
#         return QTYPE.A,A(value)
#     if qtype == 'AAAA':
#         return QTYPE.AAAA,AAAA(value)
#     if qtype == 'MX':
#         return QTYPE.MX,MX(value)
#     if qtype == 'CNAME':
#         return QTYPE.CNAME,CNAME(value)
#     if qtype == 'NS':
#         return QTYPE.NS,NS(value)


# def create_response(domain_name,r_record):
#     qtype,value = 0,0
#     print(qtype,type(qtype),value,type(value))
#     return DNSRecord(
#             DNSHeader(qr=1,aa=1,ra=1),
#             q=DNSQuestion("abc.com"),
#             a=RR("abc.com",rdata=A("1.2.3.4"))
#         )

# domain_name = "cse.du.ac.bd."
# record_list = ["ns1.cse.du.ac.bd.","NS"]
# print(create_response(domain_name,record_list))