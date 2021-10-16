# importing the requests library
import requests
import json

import time


def payshop(id,valor):
    # api-endpoint
    URL = "https://ifthenpay.com/api/payshop/get"
    
    # location given here
    apiKey = "GJY-560773"
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'payshopkey':apiKey,
               'id':id,
               'valor':valor,
               'validade':''
    
            
    
    }
    #print(PARAMS)
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    
    # extracting data in json format
    # data = r.json()
    print(r.text)
    response=json.loads(r.text)
    
    return response
    

def mbway(id,valor,tel,email):

     URL = "http://mbway.ifthenpay.com/ifthenpaymbw.asmx/SetPedidoJSON"

     # location given here
     apiKey = "RBJ-924465"

     # defining a params dict for the parameters to be sent to the API
     PARAMS = {'MbWayKey':apiKey,
                    'referencia':"500",
                    'canal':"03",
                    'valor':valor,
                    'nrtlm':tel,
                    'email':email,
                    'descricao':id,
               

     }
     #print(PARAMS)
     # sending get request and saving the response as response object
     r = requests.get(url = URL, params = PARAMS)

     # extracting data in json format
     # data = r.json()
     response=json.loads(r.text)

     return response
def verifyMbway(id):

     URL = "http://mbway.ifthenpay.com/ifthenpaymbw.asmx/EstadoPedidosJSON"

     # location given here
     apiKey = "RBJ-924465"

     # defining a params dict for the parameters to be sent to the API
     PARAMS = {'MbWayKey':apiKey,
                    
                    'canal':"03",
                    'idspagamento':id
                    
                    
               

     }
     #print(PARAMS)
     # sending get request and saving the response as response object
     r = requests.get(url = URL, params = PARAMS)

     # extracting data in json format
     # data = r.json()
     response=json.loads(r.text)

     response=response["EstadoPedidos"]
     print(response)
     response=response[0]
     print(response)

#or response["Estado"]=="123"
     if response["Estado"]=="000"  :
          return True


     elif response["Estado"]=="123":
          return -1     
     else:
          return False

    #print(response)
    

def generateMbRef( order_id, order_value ):
   chk_val = 0
    
   ent_id="12375"
   subent_id="904"
   order_id = "0000" + order_id
   
   if len(ent_id) != 5:
        #print("Lamentamos mas tem de indicar uma entidade válida")
        return
        
   if len(subent_id) == 0:
        #print("Lamentamos mas tem de indicar uma subentidade válida")
        return
        
   if order_value < 1:
        #print("Lamentamos mas não é possível gerar uma referência MB para valores inferiores a 1 Euro")
        return
   
   order_value = '%01.2f' % order_value
   
   if len(subent_id) == 1:
        #apenas serão considerados os 6 caracteres mais à direita do order_id
        chk_str = ent_id + subent_id + order_id[-6:] + str('%08.0f' % int(round(float(order_value) * 100)))
   elif len(subent_id) == 2:
        #apenas serão considerados os 5 caracteres mais à direita do order_id
        chk_str = ent_id + subent_id + order_id[-5:] + str('%08.0f' % int(round(float(order_value) * 100)))
   else:
        chk_str = ent_id + subent_id + order_id[-4:] + str('%08.0f' % int(round(float(order_value) * 100)))
        
   chk_array = [3, 30, 9, 90, 27, 76, 81, 34, 49, 5, 50, 15, 53, 45, 62, 38, 89, 17, 73, 51];
   
   i = len(chk_str)
   
   for chk_item in chk_array:
        chk_val += (int(chk_str[i-1]) % 10) * chk_item
        i -= 1
   
   chk_val %= 97
   
   chk_digits = '%02.0f' % (98-chk_val)
   

   data={
       "Entidade":ent_id,
       "Referencia":chk_str[5:5+3]+chk_str[8:8+3]+chk_str[11:11+1] + chk_digits,
        "Valor":order_value

   }

   #print(f"dicitimlkjfd{data}")
   #print("Entidade: %s" % ent_id)
   #print("Referencia: %s %s %s" % (chk_str[5:5+3], chk_str[8:8+3], chk_str[11:11+1] + chk_digits))
   #print("Valor: %s" % order_value)

   return data
#response=mbway("dgfgdfg","20","965105224","fdsg@hjgk.com")
#time.sleep(3)
#print(verifyMbway("FzMgqBdSeVnLrQZD40J3"))
