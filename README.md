## Auto Item Claimer StreamElements
This project is an automated item claimer for Stream Elements store. It allows users to automatically redeem items from a store without manual intervention. The script interacts with the store’s API to select and claim items based on predefined conditions.

### Installation

1. Clone the repo
    ```sh
   git clone https://github.com/Gabriel-6/Auto-Claimer-StreamElements.git
    ```
2. Install dependencies  
    ```sh
   pip3 install -r requirements.txt
    ```
   or
    ```sh
   pip install -r requirements.txt
    ```
3. Generate Webhook on discord
    ```sh 
    Hover your mouse over the discord channel and click on the gear > Integrations > Webhooks > New webhook > Copy WebHook URL
    ```
4. Get your JWT Token in 
    ```sh
   https://streamelements.com/dashboard/account/channels
    ```
5. Enter settings in `app/config.py`
   ```py
    CHANNEL = "" (STR)
    DISCORDWEBHOOK = "" (STR)
    JWTTOKEN = "" (STR)
    MESSAGE = "" (STR)
    TIMEOUT = 30 (INT)
   ```
6. Run `main.py`

### Usage
1. Inform the StreamElements channel in "CHANNEL"
2. Create the Discord Webhook
3. Insert your JWT Token
4. Type the message you want to send to the streamer (You will only send the message if the type of item redeemed is “perk”, if the type of item is “code” the code redeemed will be sent in the discord room where the Webhook was configured)
5. Set the TIMEOUT according to what you want (I don't recommend less than 30 seconds)
   
### Features
- Automatically claims items from a store’s inventory.
- Configurable to target specific items in the store and automatically redeem.
- Runs in the background with minimal user input.
- Ideal for redeeming rewards and items.

### Technologies Used
- Python
- asyncio, aiohttp (for asynchronous operations)
- JSON (for data handling)
