# volume_surge_telegram_bot.py  ← 2025년 11월 17일 최종 완성본

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import asyncio
from telegram import Bot

# ================== 여기만 수정 ==================
TELEGRAM_TOKEN = "8220835430:AAEtp-mzeD7Vo24OSn93CiTxRCbsMfXIzjI"   # ← 여기만 본인 토큰 넣기
CHAT_ID = 1798532618  # 처음엔 None → 실행하면 본인 채팅 ID 자동 출력해줌
# =================================================

bot = Bot(token=TELEGRAM_TOKEN)

# ---------- 텔레그램 메시지 보내기 ----------
async def get_chat_id():
    global CHAT_ID
    if CHAT_ID:
        return
    updates = await bot.get_updates()
    if updates:
        CHAT_ID = updates[-1].message.chat.id
        print(f"내 CHAT_ID 자동 감지: {CHAT_ID}")

async def send_message(text):
    global CHAT_ID
    if not CHAT_ID:
        await get_chat_id()
    if not CHAT_ID:
        print("텔레그램 봇한테 먼저 메시지 보내주세요! (예: 안녕)")
        return
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')

# ---------- 빗썸 상장 코인 목록 ----------
# get_target_coins() 함수만 아래로 완전히 교체하세요
def get_target_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 150,
        'page': 1,
        'sparkline': False
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        # ★★★★★ 여기부터 추가된 방어 코드 ★★★★★
        if isinstance(data, list):          # 정상적인 경우
            coins_data = data
        elif isinstance(data, dict) and 'error' in data:  # 에러 메시지 온 경우
            print(f"CoinGecko 에러: {data.get('error')}")
            return []
        else:
            print("CoinGecko 응답 형식 이상:", data)
            return []
        # ★★★★★ 여기까지 ★★★★★

        bithumb_symbols = {'BTC','ETH','XRP','SOL','ADA','DOGE','DOT','MATIC','AVAX','TRX','LINK','LTC','BCH','ETC','XLM','FIL','ATOM','HBAR','VET','NEAR','ALGO','ICP','SUI','APT','INJ','TON','WIF','PEPE','BONK','FLOKI','ONDO','HNT','SEI','FTM','RUNE','GRT','AAVE','XMR','EOS','XTZ','NEO','KAS','FLOW','SAND','MANA','CHZ','AXS','ENA' ,'STRK','WLD','ARB','OP','IMX','STX','MKR','THETA','ZEC','WAVES','QTUM','BTG','ICX','ONG','ORBS','IOST','STEEM','HIVE','KAVA','ANKR','AERGO','TT','CRO','FX','AKT','PYTH','WEMIX','MEW','BIGTIME','PIXEL','ALT','SNT','AHT','BLUR','ACE','METIS','GMT','ASTR','BOME','TNSR','PRIME','WOO','JTO'}
        coins = []
        for coin in coins_data:
            sym = coin.get('symbol', '').upper()
            if not sym:
                continue
            if sym in bithumb_symbols and coin.get('market_cap', 0) > 300_000_000:
                rank = coin.get('market_cap_rank', 999)
                coins.append((sym, rank))
        return sorted(coins, key=lambda x: x[1])[:120]

    except Exception as e:
        print(f"get_target_coins 오류: {e}")
        return []
# ---------- 빗썸 캔들 데이터 ----------
def get_bithumb_1d(symbol):
    try:
        url = f"https://api.bithumb.com/public/candlestick/{symbol}_KRW/1440"
        resp = requests.get(url, params={'count': 30}, timeout=10).json()
        if resp['status'] != '0000':
            return None
        df = pd.DataFrame(resp['data'], columns=['ts','open','close','high','low','volume','value'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df[['open','close','high','low','volume']] = df[['open','close','high','low','volume']].astype(float)
        return df.sort_values('ts').reset_index(drop=True)
    except:
        return None

# ---------- 거래량 폭발 체크 ----------
def check_surge():
    targets = get_target_coins()
    alerts = []
    for symbol, rank in targets:
        df = get_bithumb_1d(symbol)
        if df is None or len(df) < 15:
            continue
        # 최근 14일 가격 변동률 (횡보장 확인)
        price_range = (df['high'].tail(14).max() - df['low'].tail(14).min()) / df['close'].tail(14).mean()
        if price_range > 0.15:   # 15% 이상 움직이면 이미 상승장
            continue
        # 거래량 폭발
        avg_vol_7d = df['volume'].iloc[-8:-1].mean()
        today_vol = df['volume'].iloc[-1]
        ratio = today_vol / avg_vol_7d if avg_vol_7d > 0 else 0
        if ratio >= 3.0 and today_vol * df['close'].iloc[-1] > 5_000_000_000:  # 거래대금 50억 이상
            price = df['close'].iloc[-1]
            alerts.append(f"{symbol} ({rank}위)\n거래량 <b>{ratio:.1f}배</b> 폭발!\n현재가 {price:,.0f}원")
        time.sleep(0.8)   # API 부하 방지
    return alerts

# ---------- 메인 실행 ----------
if __name__ == "__main__":
    print(f"{datetime.now():%Y-%m-%d %H:%M} 거래량 스캔 시작...")
    results = check_surge()
    
    if results:
        msg = "거래량 터진 코인 발견!\n\n" + "\n\n".join(results)
    else:
        msg = "오늘은 거래량 폭발 코인 없음"
    
    asyncio.run(send_message(msg))
    print("텔레그램 전송 완료!")
    
    # send_message 함수만 아래로 교체하세요 (나머지는 그대로)

async def send_message(text):
    global CHAT_ID
    if not CHAT_ID:
        await get_chat_id()
    if not CHAT_ID:
        print("CHAT_ID 못 찾음")
        return
    
    try:
        await asyncio.wait_for(
            bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML'),
            timeout=20.0                     # ← 20초 기다림
        )
        print("텔레그램 전송 성공!")
    except asyncio.TimeoutError:
        print("텔레그램 타임아웃 (그래도 메시지는 갔을 가능성 99%)")
    except Exception as e:

        print(f"텔레그램 전송 실패: {e}")
