import MySQLdb


def zwroc_tabele(host, user, password, baza):
	conn = MySQLdb.connect(host, user, password, baza)
	c = conn.cursor()
	c.execute("SELECT c.customerNumber, c.creditLimit, p.productCode, p.productLine, p.productScale, p.productVendor, p.buyPrice \
				FROM Customers c, Orders o, OrderDetails d, Products p\
			    where c.customerNumber = o.customerNumber and o.orderNumber = d.orderNumber and p.productCode = d.productCode")
	return c.fetchall()
	
for i in zwroc_tabele("localhost", "root", "ania", "xxx"):
	print i