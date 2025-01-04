import request
from functools import wraps
from datetime import datetime
from flask import request
from discord_webhook import DiscordWebhook, DiscordEmbed
from funcs.string import str_equals, is_str_empty, sanitize

class RouteDecorators:
    @staticmethod
    def log(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_date = datetime.now().strftime("%B %d, %Y %I:%M%p")
            arguments = ""

            for x,y in request.args.items():
                arguments += f"[{x} - {y}]"

            print(f"[{request.remote_addr}] Accessed {request.path} with args {arguments} on {current_date}")

            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def discord_webbhook_log(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            webhook = DiscordWebhook(url='')

            embed = DiscordEmbed(title='API', color='100500')
            embed.set_timestamp()

            for x,y in request.args.items():
                embed.add_embed_field(name=x, value=y, inline=False)

            webhook.add_embed(embed)
            webhook.execute()
            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def blacklist_check():
        pass