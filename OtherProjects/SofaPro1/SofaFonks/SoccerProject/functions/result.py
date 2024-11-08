import http.client
import json
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def FullData(date):

    conn = http.client.HTTPSConnection('www.sofascore.com')
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'tr,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6,es;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': '_lr_retry_request=true; _lr_env_src_ats=false; __browsiSessionID=b7b86200-3306-4ccd-8fb8-5a17eb6d0ec1&false&SEARCH&tr&desktop-4.28.136&false; __browsiUID=6a56a669-d1a3-41a9-a34a-14881cc4b5d9; _ga=GA1.1.1496961110.1725713349; __qca=P0-2010655032-1725713348258; __gads=ID=0aab5560fdd047e5:T=1725713346:RT=1725713346:S=ALNI_MbCdw13CMcl6SndpWG3M_mEVzEfcA; __gpi=UID=00000ede7a0414d9:T=1725713346:RT=1725713346:S=ALNI_MbkBEvZZ3oc7xmvGVQekfYohbe2Sw; __eoi=ID=ff1ddb78af6fba8e:T=1725713346:RT=1725713346:S=AA-AfjaIrZWOkM_AaPL3N516P5pC; gcid_first=69f61960-e83b-46b2-84b2-948aa83451ac; FCNEC=%5B%5B%22AKsRol-6Agw9FKoOehBMSItXqsBvnFkb5cxleV1LSlXVjdk2YnG4jmoLLlK8q1XasCO2rxC3Rxm9pFMTlhAf5-uG35unf-7RT3SrMHTKEcbJ0W8g1DRWQCHkGtXur2--Ib97pqXYBPnKMn-UDYjNY6cp7TT4Gm687w%3D%3D%22%5D%5D; _ga_HNQ9P9MGZR=GS1.1.1725713348.1.1.1725713495.24.0.0',
        'if-none-match': 'W/"6256a43754"',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    conn.request('GET', '/api/v1/sport/football/scheduled-events/'+str(date), headers=headers)
    response = conn.getresponse()

    data = json.loads(response.read())["events"]
    data1 = pd.json_normalize(data, sep='_')
    columns_to_select = [
        'customId', 'id', 'startTimestamp', 'tournament_name', 'tournament_category_name',
        'season_name', 'season_year', 'tournament_uniqueTournament_id', 'season_id', 'roundInfo_round',
        'status_type', 'homeTeam_name', 'homeTeam_nameCode', 'homeTeam_id', 'awayTeam_name',
        'awayTeam_nameCode', 'awayTeam_id', 'homeScore_display', 'homeScore_period1',
        'homeScore_period2', 'awayScore_display', 'awayScore_period1', 'awayScore_period2'
    ]

    for column in columns_to_select:
        if column not in data1.columns:
            data1[column] = ""  
            
    df_selected = data1[columns_to_select]
    df_selected.insert(0, "Tarih", date)
    df_selected['startTimestamp'] = pd.to_numeric(df_selected['startTimestamp'], errors='coerce')
    df_selected = df_selected.dropna(subset=['startTimestamp']) 
    df_selected['startTimestamp'] = df_selected['startTimestamp'].astype(int)
    df_selected.loc[:, 'startTimestamp'] = pd.to_datetime(df_selected['startTimestamp'], unit='s')
    df_selected.loc[:, 'startTimestamp'] = df_selected['startTimestamp'] + pd.Timedelta(hours=3)
    
    return df_selected