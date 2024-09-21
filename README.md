# Anonymous telegram bot

![GitHub top language](https://img.shields.io/github/languages/top/NewMrPotato/Anonymous_bot)
![GitHub](https://img.shields.io/github/license/NewMrPotato/Anonymous_bot)
![GitHub Repo stars](https://img.shields.io/github/stars/NewMrPotato/Anonymous_bot)
![GitHub issues](https://img.shields.io/github/issues/NewMrPotato/Anonymous_bot)

## About

This is a telegram bot for anonymous communication. In this bot, statistics on conversations are compiled, and you can also specify your age and gender in it. You can try out the bot [here](https://t.me/AnonymsRuChat_bot)

## Starting

The `aiogram` library was used to create the bot. Therefore, you will need to install all the necessary dependencies to work:

```
pip install -r requirements.txt
```

After installing requirements you need fill `data/text/config.txt`:
```
123456789 \ telegram token
123,123 \ telegram id admins, separated by commas
https://telegra.ph/Pravila-obshcheniya-v-anonimnom-chate-08-15 \ rules in the bot
123,123 \ telegram tutors ids, separated by commas
```

Now, you can start the bot by entering the following command in the console:

```commandline
python main.py
```

---

## Administration

- As for administration, if you send command `/admin`, you will see all information about admins possibilities
![13](data/images/readme/13.PNG)

### Commands

1. `bi/id/amount` - will increase user balance, id - profile number (telegram id)
2. `/users` - will show you certain count bot users
3.  `createre/id` - will show you all creatures of certain user
4. `blacklist/id` - will add user to blacklist
5. `verify/id` - will verify user profile
