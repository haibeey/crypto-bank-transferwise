import requests
import config
import json
import utils

class req:
    def __init__(self,url,method="GET"):
        self.url = url
        self.headers= {}
        self.method = method
        self.datas={}

    def addHeader(self,key,value):
        self.headers[key]=value

    def addData(self,key,value):
        self.datas[key]=value

    def request(self):
        if self.method == "GET":
            res =requests.get(self.url,headers=self.headers,data=self.datas)
            if res.status_code == 403:
                if res.headers.get("x-2fa-approval-result")=="REJECTED":
                    ott = self.headers.get("x-2fa-approval")
                    self.headers["x-2fa-approval"]=ott
                    self.headers["X-Signature"]= utils.signData(ott)
                    return requests.get(self.url,headers=self.headers,data=self.datas)
            return res
        elif self.method=="POST":
            res = requests.post(self.url,headers=self.headers,json=self.datas)
            if res.status_code == 403:
                if res.headers.get("x-2fa-approval-result")=="REJECTED":
                    ott = self.headers.get("x-2fa-approval")
                    self.headers["x-2fa-approval"]=ott
                    self.headers["X-Signature"]= utils.signData(ott)
                    return requests.post(self.url,headers=self.headers,data=self.datas)
            return res
        else:
            raise ValueError("method not supported")

def getProfile():
    pr_req= req("{}/v1/profiles".format(config.HOST_URL))
    pr_req.addHeader("Authorization","Bearer {}".format(config.TRANSFERWISE_ACCESS_TOKEN))
    pr_req.addHeader("Content-Type","application/json")
    response = pr_req.request()
    if response.status_code != requests.codes.ok:
        return {"error":"something went wrong","code":response.text}
    return json.loads(response.text)

def transfer(account_number,account_name,amount,bank_name,source_currency="NGN",target_currency="NGN"):
    
    profile_id = 0
    profile = getProfile()
    if profile is dict and profile.get("error"):
        profile["error"]= "error occured while fetching profile"
        return profile
            
    for pr in profile:
        profile_id = pr.get("id")
        if pr.get("type")=="business":
            break

    def create_qoute():

        qoute_req = req("{}/v1/quotes".format(config.HOST_URL),method="POST")
        qoute_req.addHeader("Authorization","Bearer {}".format(config.TRANSFERWISE_ACCESS_TOKEN))
        qoute_req.addHeader("Content-Type","application/json")

        qoute_req.addData("profile",profile_id)
        qoute_req.addData("source",source_currency)
        qoute_req.addData("target",target_currency)
        qoute_req.addData("rateType","FIXED")
        qoute_req.addData("targetAmount",amount)
        qoute_req.addData("type","BALANCE_PAYOUT")


        response = qoute_req.request()
        if response.status_code != requests.codes.ok:
            return {"error":"error creating qoute","code":response.status_code}
        
        return json.loads(response.text)

    def create_recipent_account():
        #TODO handle recipent for diffent countries for instance canada request about four fields to be filed
        # while other countries just required one

        quote =  create_qoute()
        if quote.get("error"):
            return quote
        recipent_account_req = req("{}/v1/accounts".format(config.HOST_URL),method="POST")
        recipent_account_req.addHeader("Authorization","Bearer {}".format(config.TRANSFERWISE_ACCESS_TOKEN))
        recipent_account_req.addHeader("Content-Type","application/json")

        sort_code = config.getSortCode(bank_name.replace(" ","").casefold())
        if sort_code is None:
            return {"error":"invalid bank name","code":400}

        recipent_account_req.addData("currency",target_currency)
        recipent_account_req.addData("type","sort_code")
        recipent_account_req.addData("profile",profile_id)
        recipent_account_req.addData("accountHolderName",account_name)
        recipent_account_req.addData("legalType","PRIVATE")
        recipent_account_req.addData("details",{
            "sortCode":sort_code,
            "accountNumber":account_number
        })


        response = recipent_account_req.request()


        if response.status_code != requests.codes.ok:
            return {"error":"creating recipent account","code":response.status_code}
        
        res = json.loads(response.text)
        res["res_qoute"]=quote
        return res

    def create_transfer():
        recipent =  create_recipent_account()
        if recipent.get("error"):
            return recipent
        transfer_req = req("{}/v1/transfers".format(config.HOST_URL),method="POST")
        transfer_req.addHeader("Authorization","Bearer {}".format(config.TRANSFERWISE_ACCESS_TOKEN))
        transfer_req.addHeader("Content-Type","application/json")

        transfer_req.addData("targetAccount",recipent.get("id"))
        transfer_req.addData("quote",recipent.get("res_qoute").get("id"))
        transfer_req.addData("customerTransactionId",config.getUUID())
        transfer_req.addData("details",{
            "reference":"cryptobank payout",
            "transferPurpose":"verification.transfers.purpose.pay.bills",
            "sourceOfFunds": "verification.source.of.funds.other"
        })

        response = transfer_req.request()

        if response.status_code != requests.codes.ok:
            return {"error":"something went wrong","code":response.status_code}
        
        res = json.loads(response.text)
        res["res_transfer"]=recipent
        return res

    def fund_tranfer():
        transfer =  create_transfer()

        if transfer.get("error"):
            return transfer

        transfer_funds_req \
        = req(
            "{}/v3/profiles/{}/transfers/{}/payments".
            format(
                config.HOST_URL,profile_id,
                transfer.get("id")
                ),
            method="POST"
        )
        transfer_funds_req.addHeader("Authorization","Bearer {}".format(config.TRANSFERWISE_ACCESS_TOKEN))
        transfer_funds_req.addHeader("Content-Type","application/json")

        transfer_funds_req.addData("type","BALANCE")

        response = transfer_funds_req.request()

        if response.status_code != requests.codes.ok:
            return {"error":"something went wrong","code":response.status_code,"response":response.text}
        return transfer

    return fund_tranfer()
        

        
    
        


