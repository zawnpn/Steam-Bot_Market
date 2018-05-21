# Steam-Bot_Market
Simple tool to help find good price on steam market.

## Usage
    usage: main.py [-h] [--game GAME] [--sleep SLEEP] [--itemnum ITEMNUM]
                   [--range RANGE RANGE] [--thresh THRESH] [--counts COUNTS]
                   [--save] [--print] [--mail]

## Arguments
    optional arguments:
      -h, --help           show this help message and exit
      --game GAME          Choose a game
      --sleep SLEEP        Sleep time
      --itemnum ITEMNUM    Amount of items
      --range RANGE RANGE  Price range
      --thresh THRESH      Threshold of ratio
      --counts COUNTS      Transactions counts
      --save, -s           Save an output file
      --print, -p          Instant output
      --mail, -m           Send result by mail

## Examples
    python3 main.py --game dota -m -s --days 8 --thresh 0.65
    
## Tips
 - Make sure to modify parameters in config/config.py before using this program.
 - You can use `crontab` to set up scheduled tasks
      
## Author
Blog:[Wanpeng Zhang](http://www.oncemath.com)

E-mail:zawnpn@gmail.com
