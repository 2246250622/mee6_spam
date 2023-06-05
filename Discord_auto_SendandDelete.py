from lovebaby import selfbot
import time
import random
 
token = ""
 
bot = selfbot(token=token)
 
#927180910661623880 Chinese
#968516355265532014 English
#968517958982860820 Malaysia
#968518009637462066 Indonesia
#968518050603229274 Thailand
#968518088939159552 Vietnam
#993873548303151166 Philippines



mylist = [968517958982860820, 968518009637462066, 968518050603229274, 968518088939159552, 993873548303151166]

while True:
    try:
        channel = bot.get_channel(random.choice(mylist))
        print(channel) 
        message_id = channel.send_message(' ㅤ')
        print("Message Sent")
        channel.delete_message(message_id)
        print("Message Deleted")
        time.sleep(60)
    except:
        pass
        print("Something went wrong")