from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID of the spreadsheet.
SAMPLE_SPREADSHEET_ID = "1p1V-H-WANZfj074Dg8LNmzeE2ZpC0cFl-gB9dkzvB3E"

service = build("sheets", "v4", credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = (
    sheet.values()
    .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="applied!A1:I10")
    .execute()
)
values = result.get("values", [])

aoa = [["1/1/2020", 4000], ["4/4/2020", 3000], ["7/12/2020", 7000]]

request = (
        sheet.values()
        .update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="Sheet2!B2",
            valueInputOption="USER_ENTERED",
            body={"values": aoa},
        )
        .execute()
    )

print(request)