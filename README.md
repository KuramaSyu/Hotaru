# kuroyume
 Discord bot written with hikari + lightbulb


### Structure
```
.
└── src
    ├── core    # contains logic of the bot
    ├── db      # contains classes to access databases
    ├── ext     # contains Slash Commands
    ├── models  # contains models, used in services
    └── services    # contains services which are used in ext
        ├── api     # contains the definitions for the models
        └── impl    # contains the implementations for the models
```