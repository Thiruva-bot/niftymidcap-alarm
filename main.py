import yfinance as yf
import requests
from datetime import datetime

def get_nifty_data():
    ticker_symbol = "NIFTY_MIDCAP_100.NS"
    try:
        # 1. 넉넉하게 최근 1개월치를 가져옵니다.
        df = yf.download(ticker_symbol, period="1mo", progress=False)
        
        if not df.empty:
            # 2. 가장 마지막 날(최신)의 종가를 가져옵니다.
            # 데이터 구조가 복잡할 수 있어 확실하게 숫자로 변환합니다.
            last_price = float(df['Close'].iloc[-1])
            return last_price
        else:
            return None
    except Exception as e:
        print(f"데이터 추출 에러: {e}")
        return None

def send_message():
    token = "8554617786:AAH24mK4mZ7NTk1jK_EpgElJIMGtUN5gWCk"
    chat_id = "8324101961"
    
    price = get_nifty_data()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if price:
        # 데이터가 있으면 성공 메시지
        text = f"📊 [Nifty Midcap 100]\n날짜: {now}\n현재 지수: {price:,.2f}"
    else:
        # 데이터가 없으면 안내 메시지
        text = f"⚠️ 지수 데이터를 가져올 수 없습니다.\n티커(^NSEMDCP100)를 다시 확인하거나,\n잠시 후 다시 시도해 주세요."
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    
    requests.get(url, params=params)
    print(f"실행 완료: {now}")

if __name__ == "__main__":
    send_message()