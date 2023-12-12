logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

cards = ["1a", "1b", "1c", "1d", "2a", "2b", "2c", "2d", "3a", "3b", "3c", "3d", "4a", "4b", "4c", "4d", "5a", "5b", "5c", "5d", "6a", "6b", "6c", "6d", "7a", "7b", "7c", "7d", "8a", "8b", "8c", "8d", "9a", "9b", "9c", "9d", "10a", "10b", "10c", "10d", "ja", "jb", "jc", "jd", "qa", "qb", "qc", "qd", "ka", "kb", "kc", "kd"]

cheap = {
"1a":"""
 _____ 
|A .  |
| /.\ |
|(_._)|
|  |  |
|____V|""",
"2a":"""
 _____
|2    | 
|  ^  |
|     |
|  ^  |
|____Z|""",
"3a":"""
 _____ 
|3    |
| ^ ^ |
|     |
|  ^  |
|____E|""",
"4a":"""
 _____ 
|4    |
| ^ ^ |
|     |
| ^ ^ |
|____h|""",
"5a":"""
 _____ 
|5    |
| ^ ^ |
|  ^  |
| ^ ^ |
|____S|""",
"6a":"""
 _____ 
|6    |
| ^ ^ |
| ^ ^ |
| ^ ^ |
|____9|""",
"7a":"""
 _____ 
|7    |
| ^ ^ |
|^ ^ ^|
| ^ ^ |
|____L|""",
"8a":"""
 _____ 
|8    |
|^ ^ ^|
| ^ ^ |
|^ ^ ^|
|____8|""",
"9a":"""
 _____ 
|9    |
|^ ^ ^|
|^ ^ ^|
|^ ^ ^|
|____6|""",
"10a":"""
 _____ 
|10 ^ |
|^ ^ ^|
|^ ^ ^|
|^ ^ ^|
|___OI|""",
"ja":"""
 _____ 
|J  ww|
| ^ {)|
|(.)% |
| | % |
|__%%[|""",
"qa":"""
 _____ 
|Q  ww|
| ^ {(|
|(.)%%|
| |%%%|
|_%%%O|""",
"ka":"""
 _____ 
|K  WW|
| ^ {)|
|(.)%%|
| |%%%|
|_%%%>|""", # fim de espadas
"1b":"""
 _____ 
|A _  |
| ( ) |
|(_._)|
|  |  |
|____V|""",
"2b":"""
 _____
|2    | 
|  &  |
|     |
|  &  |
|____Z|""",
"3b":"""
 _____ 
|3    |
| & & |
|     |
|  &  |
|____E|""",
"4b":"""
 _____ 
|4    |
| & & |
|     |
| & & |
|____h|""",
"5b":"""
 _____ 
|5    |
| & & |
|  &  |
| & & |
|____S|""",
"6b":"""
 _____ 
|6    |
| & & |
| & & |
| & & |
|____9|""",
"7b":"""
 _____ 
|7    |
| & & |
|& & &|
| & & |
|____L|""",
"8b":"""
 _____ 
|8    |
|& & &|
| & & |
|& & &|
|____8|""",
"9b":"""
 _____ 
|9    |
|& & &|
|& & &|
|& & &|
|____6|""",
"10b":"""
 _____ 
|10 & |
|& & &|
|& & &|
|& & &|
|___OI|""",
"jb":"""
 _____ 
|J  ww|
| o {)|
|o o% |
| | % |
|__%%[|""",
"qb":"""
 _____ 
|Q  ww|
| o {(|
|o o%%|
| |%%%|
|_%%%O|""",
"kb":"""
 _____ 
|K  WW|
| o {)|
|o o%%|
| |%%%|
|_%%%>|""", # fim de paus
"1c":"""
 _____ 
|A_ _ |
|( v )|
| \ / |
|  v  |
|____V|""",
"2c":"""
 _____
|2    | 
|  v  |
|     |
|  v  |
|____Z|""",
"3c":"""
 _____ 
|3    |
| v v |
|     |
|  v  |
|____E|""",
"4c":"""
 _____ 
|4    |
| v v |
|     |
| v v |
|____h|""",
"5c":"""
 _____ 
|5    |
| v v |
|  v  |
| v v |
|____S|""",
"6c":"""
 _____ 
|6    |
| v v |
| v v |
| v v |
|____9|""",
"7c":"""
 _____ 
|7    |
| v v |
|v v v|
| v v |
|____L|""",
"8c":"""
 _____ 
|8    |
|v v v|
| v v |
|v v v|
|____8|""",
"9c":"""
 _____ 
|9    |
|v v v|
|v v v|
|v v v|
|____6|""",
"10c":"""
 _____ 
|10 v |
|v v v|
|v v v|
|v v v|
|___OI|""",
"jc":"""
 _____ 
|J  ww|
|   {)|
|(v)% |
| v % |
|__%%[|""",
"qc":"""
 _____ 
|Q  ww|
|   {(|
|(v)%%|
| v%%%|
|_%%%O|""",
"kc":"""
 _____ 
|K  WW|
|   {)|
|(v)%%|
| v%%%|
|_%%%>|""", # fim de copas
"1d":"""
 _____ 
|A ^  |
| / \ |
| \ / |
|  v  |
|____V|""",
"2d":"""
 _____
|2    | 
|  o  |
|     |
|  o  |
|____Z|""",
"3d":"""
 _____ 
|3    |
| o o |
|     |
|  o  |
|____E|""",
"4d":"""
 _____ 
|4    |
| o o |
|     |
| o o |
|____h|""",
"5d":"""
 _____ 
|5    |
| o o |
|  o  |
| o o |
|____S|""",
"6d":"""
 _____ 
|6    |
| o o |
| o o |
| o o |
|____9|""",
"7d":"""
 _____ 
|7    |
| o o |
|o o o|
| o o |
|____L|""",
"8d":"""
 _____ 
|8    |
|o o o|
| o o |
|o o o|
|____8|""",
"9d":"""
 _____ 
|9    |
|o o o|
|o o o|
|o o o|
|____6|""",
"10d":"""
 _____ 
|10 o |
|o o o|
|o o o|
|o o o|
|___OI|""",
"jd":"""
 _____ 
|J  ww|
| /\{)|
| \/% |
|   % |
|__%%[|""",
"qd":"""
 _____ 
|Q  ww|
| /\{(|
| \/%%|
|  %%%|
|_%%%O|""",
"kd":"""
 _____ 
|K  WW|
| /\{)|
| \/%%|
|  %%%|
|_%%%>|""",
"secret":"""
 _____ 
|?    |
|     |
|  ?  |
|     |
|____?|"""
}