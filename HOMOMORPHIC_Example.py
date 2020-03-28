from pyope.ope import OPE
import mysql.connector

from phe import paillier


"""
Method simulating a server which will proceed to the addition of
several integer encrypted with a homomorphic algorithm given by a client
Returns the result to the client
"""
def homomorphicAdditionServer(public_key,user,password):
    mydb = connection("localhost", user, password)
    cur = mydb.cursor()
    query = cur.execute("SELECT name,salaryHOMOMORPHIC FROM TP2020_ENCRYPTION.HOMOMORPHIC_Example")
    cur.execute(query)
    result = cur.fetchall()

    if(len(result)==0):
        return None
    else:
        temp = public_key.encrypt(0)
        for r in result:
            encrypted = paillier.EncryptedNumber(public_key, int(r[1]))
            temp = temp.__add__(encrypted)
        return temp


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
  #print("Generating paillier keypair")
  public_key = paillier.PaillierPublicKey(21218276132140299981345171408258919441893448968179551651807734346887480236250710232383652741675234390922104910466862995204102193393826577813099728070887808650299645836532466520724568133793779553536988008833660046942041140006780549439310791225496662291842600105297406970158521146072036792214391832129534275580598094428729849245407070005082033624674081452039804219701019308402542111007312660267662181152954646713888493723620350994684730876123094481860081397502477538382287030725791397232124748677509975421605869263471838457679408755619102710493185748864416954630903303836396357835818660093421673646603832893820387152927)
  private_key = paillier.PaillierPrivateKey(public_key,137675721712905603592598691269844695182447341641248561784971314886022204516911538904276806501196083442912491466111873129071013621221477355586737741262005722300844872697468193376520839554353705280841001974848969951463374258939533569840617951348260566329124412775710722277539807788091242653259841697836590327987,154117776672249084342664250956499404215765364216211882680833392111275630242992576292689161185260718825099656883490396480681795181617375039782865068883699181222468268715934547599382348441423651090394789059601273183897853226835432745451703569573326670009829042737774848595334935807712506725655471844147547579621)

  while quit==False:
    choice = input("Type INSERT to insert a tuple, GET to recover salary information,\nRANGE to get an interval of salary, ADD to make an addition through a middleware using homomorphic encryption, QUIT to exit :")

    if(choice.lower()=="add"):

        #The client asks to a server to do the addition for him
        addEncrypted = homomorphicAdditionServer(public_key,user,password)

        if(addEncrypted==None):
            print("No sum of salaries available")
        else:
            print("Sum encrypted :", addEncrypted)
            decrypted = private_key.decrypt(addEncrypted)
            print("Salary sum after decryption is :", decrypted)
        print()



    if(choice.lower()=="insert"):
      try:
        name = input("Give a name :")
        salary = int(input("Give a salary :"))

        mydb = connection("localhost",user,password)

        cur = mydb.cursor()
        query = "INSERT INTO TP2020_ENCRYPTION.HOMOMORPHIC_Example(name,salaryOPE,salaryHOMOMORPHIC) VALUES (%s,%s,%s)"

        cur.execute(query,(name,cipher.encrypt(salary),str(public_key.encrypt(salary).ciphertext()),))
        mydb.commit()
      except Exception as e:
        print(e)
        #print("Salary is not an int OR the name is already in the table")
      print()

    if (choice.lower() == "get"):
      name = input("Give a name :")

      mydb = connection("localhost", user, password)
      cur = mydb.cursor()

      sql = "SELECT salaryOPE FROM TP2020_ENCRYPTION.HOMOMORPHIC_Example WHERE name = %s"
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

        query = cur.execute("SELECT name,salaryOPE FROM TP2020_ENCRYPTION.HOMOMORPHIC_Example WHERE salaryOPE BETWEEN %s AND %s ORDER BY salaryOPE" % (
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