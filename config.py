import os, datetime
import uuid

JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
basedir = os.path.abspath(os.path.dirname(__file__))


testing = os.environ.get("TEST")
if not testing:
    HOST_URL= "https://api.sandbox.transferwise.tech"
else:
    HOST_URL = "https://api.transferwise.com"
TRANSFERWISE_ACCESS_TOKEN = "b5e96042-27f9-4b72-bfde-355d24ec686f"
SECRET_KEY = b"hvmjvhgghfgsfhsdJYFTYFTYDEjfyhsaegrwteykrultgfyktrwu"
CORS_HEADERS = 'Content-Type'


def getSortCode(name):
    if not testing:
        return "403020"
    return bank_sortcode.get(name)

def getUUID():
    return str(uuid.uuid1())


bank_sortcode={
    "Access Bank Plc":"44150149",
    "Diamond Bank Plc":"63150162",
    "Ecobank Nigeria Plc":"50150311",
    "Enterprise Bank":"84150015",
    "Equitorial Trust Bank Limited":"40150101",
    "Fidelity Bank Plc":"70150003",
    "First Bank Of Nigeria Plc":"11152303",
    "First City Monument Bank Plc":"214150018",
    "Finbank Plc":"85151275",
    "Guaranty Trust Bank Plc":"58152052",
    "Keystone Bank":"82150017",
    "Mainstreet Bank":"14150030",
    "Nigeria International Bank (Citigroup)":"23150005",
    "ECOBank":"56080016",
    "Polaris Bank Plc":"76151006",
    "Stanbic-Ibtc Bank Plc":"221159522",
    "Standard Chartered Bank Nigeria Ltd":"68150057",
    "Sterling Bank Plc":"232150029",
    "United Bank For Africa Plc":"33154282",
    "Union Bank Of Nigeria Plc":"32156825",
    "Unity Bank Plc":"215082334",
    "Wema Bank Plc":"35150103",
    "Zenith Bank Plc":"57150013"   
}


for bank in list(bank_sortcode.keys()):
    bank_sortcode[bank.replace(" ","").casefold()]=bank_sortcode[bank]

