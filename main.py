import yfinance as yf
import requests
from datetime import datetime

# 1. 메시지를 보내는 통합 창구입니다.
def send_telegram(text):
    token = "8554617786:AAH24mK4mZ7NTk1jK_EpgElJIMGtUN5gWCk"
    chat_id = "8324101961"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    try:
        requests.get(url, params=params)
    except Exception as e:
        print(f"텔레그램 전송 중 오류 발생: {e}")

def get_nifty_data():
    # [테스트 방법] 아래 티커 이름을 "WRONG_TICKER"로 바꾸고 저장해 보세요!
    ticker_symbol = "NIFTY_MIDCAP_100.NS" 
    
    try:
        df = yf.download(ticker_symbol, period="1mo", progress=False)
        
        # 데이터가 없으면(티커가 틀리면) 강제로 에러를 냅니다.
        if df.empty:
            raise ValueError(f"데이터가 비어있습니다. 티커({ticker_symbol})를 확인하세요.")
            
        last_price = float(df['Close'].iloc[-1])
        return last_price

    except Exception as e:
        # 에러가 나면 한글로 정돈된 메시지를 보냅니다.
        error_msg = f"❌ [Nifty-Alarm] 에러 발생!\n내용: {e}"
        send_telegram(error_msg) 
        return None

def send_message():
    price = get_nifty_data()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if price:
        text = f"📊 [Nifty Midcap 100]\n날짜: {now}\n현재 지수: {price:,.2f}"
        send_telegram(text)
    
    print(f"실행 완료: {now}")

if __name__ == "__main__":
    send_message()
