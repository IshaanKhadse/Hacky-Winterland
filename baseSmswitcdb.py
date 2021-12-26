from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import psycopg2
import random

def connector():
    # cockroachstring = "dbname='wet-dingo-838.defaultdb' user='muntaser' password='get your own password' host='free-tier.gcp-us-central1.cockroachlabs.cloud' port='26257'"
    cockroachstring = os.environ.get('COCKROACHSTR')
    conn=psycopg2.connect(cockroachstring)
    return conn

app = Flask(__name__)


def setcreds(nc):
    global cred
    cred = nc

    return "success"

def getquiz(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, question, answer, hint FROM quizzes")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        questions = []


        for row in rows:
            q = {}
            q['question'] = row[1]
            q['answer'] = row[2]
            q['hint'] = row[3]
            
            questions.append(q)
            
        return random.choice(questions)



@app.route("/merryquiz", methods=['POST'])
def smerry_quiz():
    """Respond to incoming calls with a simple text message."""

    global cred

    incoming = request.values['Body']

    print("incoming text is " + incoming)


    # Start our TwiML response
    resp = MessagingResponse()

    flag = 0
    outstring = "Merry Christmas from the merry quizbot! Also, i did not understand the following message ..." + incoming + " Please use the following keywords:  Question or Answer or Hint"

    incoming = incoming.lower()
    
    conn = connector()
    
    q = getquiz(conn)
    
    if "answer" in incoming:
        if q['answer'] in incoming:
            outstring =  "thats correct!! thank you for using the merry quizbot"
        else:
            outstring =  "sorry try again!! good try though, better luck next time"
        flag = 1    


    if "question" in incoming:

        outstring =  q['question']
        flag = 1 

    if "hint" in incoming:
    
        outstring =  q['hint']
        flag = 1 
        


    # Add a message
    if flag ==0:
        outstring = "Merry Christmas from the merry quizbot! Also, i did not understand the following message ..." + incoming + " Please use the following keywords:  Question or Answer"
    
    resp.message(outstring)

    return str(resp)




@app.route("/smsbase", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    global cred

    incoming = request.values['Body']

    print("incoming text is " + incoming)


    # Start our TwiML response
    resp = MessagingResponse()

    flag = 0
    outstring = "Merry Christmas from the merry quizbot! Also, i did not understand the following message ..." + incoming + " Please use the following keywords:  Question or Answer or Hint"

    incoming = incoming.lower()
    
    if "answer" in incoming:
        if 'north pole' in incoming:
            outstring =  "thats correct!! thank you for using the merry quizbot"
        else:
            outstring =  "sorry try again!! good try though, better luck next time"
        flag = 1    


    if "question" in incoming:

        outstring =  "Where does Santa live?"
        flag = 1 

    if "hint" in incoming:
    
        outstring =  "Santa's workshop is also where he lives"
        flag = 1 
        
            





    # Add a message
    if flag ==0:
        outstring = "Merry Christmas from the merry quizbot! Also, i did not understand the following message ..." + incoming + " Please use the following keywords:  Question or Answer"
    
    resp.message(outstring)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host = '45.79.199.42', port = 8004)
