from pyope.ope import OPE
import mysql.connector


"""
Returns a connection to the mysql database
"""
def connection(host,user,password):
  mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    port=3306
  )
  return mydb



def main():
  user = input("Give the user's name :")
  password = input("Give the user's password:")
  cipher = OPE(b'hfgdhjfghfgdhf')
  quit = False
  while quit==False:
    choice = input("Type INSERT to insert a tuple, GET to recover salary information, RANGE to get an interval of salary, QUIT to exit :")

    if(choice.lower()=="insert"):
      try:
        name = input("Give a name :")
        salary = int(input("Give a salary :"))

        mydb = connection("localhost",user,password)

        cur = mydb.cursor()
        query = "INSERT INTO TP2020_ENCRYPTION.OPE_Example(name,salaryOPE) VALUES (%s,%s)"

        cur.execute(query, (name,cipher.encrypt(salary),))
        mydb.commit()
      except Exception as e:
        print(e)
        #print("Salary is not an int OR the name is already in the table")
      print()

    if (choice.lower() == "get"):
      name = input("Give a name :")

      mydb = connection("localhost", user, password)
      cur = mydb.cursor()

      sql = "SELECT salaryOPE FROM TP2020_ENCRYPTION.OPE_Example WHERE name = %s"
      val = (name,)

      cur.execute(sql, val)

      result = cur.fetchall()

      res_list = [x[0] for x in result]

      for cipherSalary in res_list:
        salary = (cipher.decrypt(cipherSalary))
        print("The salary before decryption is ",cipherSalary)
        print("Salary of ",name," is ",salary)
      print()

    if (choice.lower() == "range"):
      range1 = int(input("Give the low border :"))
      range2 = int(input("Give the high border :"))
      if(range1 <= range2):
        mydb = connection("localhost", user, password)

        cur = mydb.cursor()

        query = cur.execute("SELECT name,salaryOPE FROM TP2020_ENCRYPTION.OPE_Example WHERE salaryOPE BETWEEN %s AND %s ORDER BY salaryOPE" % (
          cipher.encrypt(range1), cipher.encrypt(range2)))
        cur.execute(query)

        result = cur.fetchall()
        if(len(result)!=0):
          print("The people having a salary in that interval are :")
          for r in result:
            print(r[0],", his salary after encryption is ",r[1])
        else:
          print("No one with a salary in that interval")
      else:
        print("Low border is bigger than high border")
      print()
    if(choice.lower()=="quit"):
      quit = True
      print()


if __name__ == "__main__":
  main()