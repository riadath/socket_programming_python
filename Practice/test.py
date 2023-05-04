from dnslib.dns import *


q1 = DNSRecord.question("cse.du.ac.bd.")


q2 = q1.get_q().get_qname()
# print(q2)

def get_queryType(qtype,value):
    if qtype == 'A':
        return QTYPE.A,A(value)
    if qtype == 'AAAA':
        return QTYPE.AAAA,AAAA(value)
    if qtype == 'MX':
        return QTYPE.MX,MX(value)
    if qtype == 'CNAME':
        return QTYPE.CNAME,CNAME(value)
    if qtype == 'NS':
        return QTYPE.NS,NS(value)
    

a1 = q1.reply()
qt,val = get_queryType('NS','ns1.cse.du.ac.bd')

a1.add_answer(RR(q2,qt,rdata=val, ttl=60))
# print(a1)

a2 = str(a1.get_a()).split()
res,r_type = a2[4],a2[3]
print(res,r_type)

