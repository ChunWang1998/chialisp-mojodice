# chialisp-mojodice

receiver: 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107
存錢罐(created after curry treehash): 82885d3f783b536d5d726a02e913e0b99dd7fbc35bc96bf913f8912c1685b7fa
標準地址:txch1s2y960mc8dfk6htjdgpwjylqhxwa077rt0ykh7gnlzgjc959klaqa87nwm
錢包public key:b6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5
(after curry )0719ee4a74d34581244133c878202735c80b878524cc5f870781107cd05876ba

# step
## create puzzle hash, set target amount
    cdv clsp build piggybank/piggybank.clsp
    cdv clsp curry piggybank/piggybank.clsp.hex -a 1000 -a 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107 --treehash
    cdv encode 82885d3f783b536d5d726a02e913e0b99dd7fbc35bc96bf913f8912c1685b7fa --prefix txch
    送錢給標準地址: 
    chia wallet send -a 0 -t txch1s2y960mc8dfk6htjdgpwjylqhxwa077rt0ykh7gnlzgjc959klaqa87nwm --override

## contributions spend
 ` cdv clsp build piggybank/contribution.clsp.hex`
`    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5 --treehash`
`    cdv encode 0719ee4a74d34581244133c878202735c80b878524cc5f870781107cd05876ba --prefix txch`
    送錢給地址(0.000000000001: 1001 - 1000)
   ` chia wallet send -a 0.000000000001 -t txch1quv7ujn56dzczfzpx0y8sgp8xhyqhpu9ynx9lpc8syg8e5zcw6aqjvx3te`
## set spend bundle json
  
### coin1
    cdv rpc coinrecords --by puzhash 82885d3f783b536d5d726a02e913e0b99dd7fbc35bc96bf913f8912c1685b7fa -nd
    puzzle_reveal:
    cdv clsp curry piggybank/piggybank.clsp.hex -a 1000 -a 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107 -x
    solution:(my_amount new_amount puzzle_hash)
    opc '(1000 1001 0x82885d3f783b536d5d726a02e913e0b99dd7fbc35bc96bf913f8912c1685b7fa)'

### coin2
    cdv rpc coinrecords --by puzhash 0719ee4a74d34581244133c878202735c80b878524cc5f870781107cd05876ba -nd
    puzzle_reveal:
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5 -x
    solution:(coin_id new_amount)
    opc '(0x201700dab002f5136eb2ef9e9dd8a255c327501c373036d25e64e0ec9806cf80 1001)'
 
### aggregated_signature
    python3 piggybank/sign_contribution.py

## send tx 
    cdv rpc pushtx spend_bundle.json 

# other 
 ->(ERROR)One or more of the specified objects was not a spend bundle: bytes object is expected to start with 0x
 ->refer: https://docs.chia.net/guides/chialisp-first-smart-coin/ to add 0x

