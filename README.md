# Discord Intro Bot

Bot Discord untuk intro member dengan command `/intro`.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Discord Bot
1. Pergi ke [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Beri nama bot (misal: "Intro Bot")
4. Go ke tab "Bot" dan click "Add Bot"
5. Di bagian TOKEN, click "Copy" untuk copy token bot
6. Edit file `.env` dan replace `YOUR_BOT_TOKEN_HERE` dengan token yang sudah dicopy

### 3. Setup Channel Intro
1. Buat channel baru di server (misal: #intro)
2. Klik channel tersebut, lihat URL atau cek Channel ID
3. Copy Channel ID dan paste ke `.env` di `INTRO_CHANNEL_ID`
   - Cara dapetin Channel ID: Enable Developer Mode di Discord (User Settings > Advanced > Developer Mode), terus klik kanan channel pilih "Copy Channel ID"

### 4. Setup Bot Permissions
Di Discord Developer Portal, pergi ke OAuth2 > URL Generator:
- Scopes: `bot`
- Permissions:
  - `Send Messages`
  - `Embed Links`
  - `Use Application Commands`

Copy generated URL dan akses di browser untuk add bot ke server mu.

### 5. Run Bot
```bash
python main.py
```

## Cara Pakai

1. Setup `.env` dengan `DISCORD_TOKEN` dan `INTRO_CHANNEL_ID`
2. Run bot: `python main.py`
3. Di Discord, ketik `/intro`
4. Bot akan post embed ke channel intro dengan button "Isi Intro"
5. Member klik button tersebut
6. Modal form muncul dengan field:
   - Nama
   - Umur
   - Hobby
   - Tentang Kamu
7. Member isi dan submit
8. Bot akan post intro mereka di channel intro

## Features

✅ Slash command `/intro`
✅ Dropdown untuk pilih umur
✅ Modal form yang cantik
✅ Response dalam bentuk embed

## Customization

Kamu bisa customize:
- Warna embed (ganti value di `color=discord.Color.purple()`)
- Field form (tambah/kurangi di class `IntroModal`)
- Dropdown options (edit di `AgeView`)
