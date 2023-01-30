# chialisp-mojodice



# Example

receiver: 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107
存錢罐(created after curry treehash): b9a3a2f9b33d71c9775fb9600a10f7ea39fab91962d09a7302c7bb6c7ab1bbe5
標準地址:txch1hx3697dn84cuja6lh9sq5y8hagul4wgevtgf5uczc7akc743h0jsszcwpk
錢包public key:0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5
(after curry )0719ee4a74d34581244133c878202735c80b878524cc5f870781107cd05876ba

## create puzzle hash, set target amount 
創建一個裡面有0元的存錢罐
    cdv clsp build piggybank/piggybank.clsp
    cdv clsp curry piggybank/piggybank.clsp.hex -a 2200 -a 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107 --treehash
    cdv encode b9a3a2f9b33d71c9775fb9600a10f7ea39fab91962d09a7302c7bb6c7ab1bbe5 --prefix txch
    送錢給標準地址
    <!-- chia wallet send -a 0 -t txch1s2y960mc8dfk6htjdgpwjylqhxwa077rt0ykh7gnlzgjc959klaqa87nwm -m 0.000006 --override -->

## contributions spend (從自己的錢包分出一部分的錢 拿來存)
從錢包劃分出一個有x元的存錢罐
    cdv clsp build piggybank/contribution.clsp
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5 --treehash
    cdv encode e92932f02e9fbb6107074052f5757f7f69c27bd18ddd1a8bdc51ad770c7f7719 --prefix txch
    送錢給地址(700)
    chia wallet send -a 0.0000000007 -t txch1ay5n9upwn7akzpc8gpf02atl0a5uy7733hw34z7u2xkhwrrlwuvsqngtnr (--fee 0.000006)
## set spend bundle json
  
### coin1
    cdv rpc coinrecords --by puzhash b9a3a2f9b33d71c9775fb9600a10f7ea39fab91962d09a7302c7bb6c7ab1bbe5 -nd
    puzzle_reveal:
    cdv clsp curry piggybank/piggybank.clsp.hex -a 3000 -a 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107 -x
    solution:(my_amount new_amount puzzle_hash)
    opc '(200 900 0xa0a6659b200aef026393ff92f7fde6119a0fce985a68c4e5b7ea8bedd3d9afee)'

### coin2
    cdv rpc coinrecords --by puzhash e92932f02e9fbb6107074052f5757f7f69c27bd18ddd1a8bdc51ad770c7f7719 -nd
    puzzle_reveal:
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5 -x
    solution:(coin_id new_amount)
    opc '(0x8f540ee77a493b99ecee19b2ede43cbdc7854e83c2c166de6734ebae5b0e19ad 900)'
 
### aggregated_signature
    python3 piggybank/sign_contribution.py

## send tx (wait half a hour)
    cdv rpc pushtx spend_bundle.json 

# mojodice

vault: 2eb81c4a4ad015fa2138e6a0b33a860d72e3f3ef5432fe86616de96281a02a37 (txch196upcjj26q2l5gfcu6stxw5xp4ew8ul02se0apnpdh5k9qdq9gmswclytr)
劃分的coin:e92932f02e9fbb6107074052f5757f7f69c27bd18ddd1a8bdc51ad770c7f7719
(txch1ay5n9upwn7akzpc8gpf02atl0a5uy7733hw34z7u2xkhwrrlwuvsqngtnr)
## create puzzle hash, set target amount
    cdv clsp build piggybank/piggybank.clsp
    cdv clsp curry piggybank/piggybank.clsp.hex -a 2300 -a 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107 -a 40 -a 10000000  --treehash
    cdv encode 2eb81c4a4ad015fa2138e6a0b33a860d72e3f3ef5432fe86616de96281a02a37 --prefix txch
    送錢給標準地址

## contributions spend (從自己的錢包分出一部分的錢 拿來存)
    cdv clsp build piggybank/contribution.clsp
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5 --treehash
    cdv encode e92932f02e9fbb6107074052f5757f7f69c27bd18ddd1a8bdc51ad770c7f7719 --prefix txch
   送錢給標準地址

## set spend bundle json
  
### coin1
    cdv rpc coinrecords --by puzhash 2eb81c4a4ad015fa2138e6a0b33a860d72e3f3ef5432fe86616de96281a02a37 -nd
    puzzle_reveal:
    cdv clsp curry piggybank/piggybank.clsp.hex -a 2300 -a 0xeeda2dceabc6e970d30d2990177a9317d0301597c6ed552217d83aa07e1af107 -a 40 -a 10000000  -x
    solution:
       opc '(500 900 0x2eb81c4a4ad015fa2138e6a0b33a860d72e3f3ef5432fe86616de96281a02a37 40 60 140)'

### coin2
    cdv rpc coinrecords --by puzhash e92932f02e9fbb6107074052f5757f7f69c27bd18ddd1a8bdc51ad770c7f7719 -nd
      puzzle_reveal:
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb6d62517192be93313f6191249af1b139445b4842fa4c7930b9f3fe824661500db594ab76eb9c8ed8caef3ed0f0f59a5 -x
      solution:(piggybank token / new amount)
      opc '(0xdce4cde31dbe81939bf79a3b7cece965d7b50956d2822821f60496ebb5046567 900)'

### aggregated_signature
    python3 piggybank/sign_contribution.py

## send tx 
    cdv rpc pushtx spend_bundle.json 

# other 
 ->(ERROR)One or more of the specified objects was not a spend bundle: bytes object is expected to start with 0x
 ->refer: https://docs.chia.net/guides/chialisp-first-smart-coin/ to add 0x
 -> -m 0.000006 --override 

test:
- input: curry (o)
- input: multi input (o)
- contract: function without using (o)
- contract: main func