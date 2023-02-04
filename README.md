# chialisp-mojodice



# Example

receiver: 0x574cfa983d0e24354484db66a68a2e5e11711bf74192056a256eeee09576c968

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

vault: eb3f76bd4f51d601f4d2c58690ffca7ba9b4ec7e222c693eca7829fe260d0f16 (txch1avlhd02028tqraxjckrfpl720w5mfmr7ygkxj0k20q5lufsdputq8qalk9)
劃分的coin:b40dcf127f4cfaf7f922ff53d49a08ffbf003e276fb1936fb1fc2fa95674b909
(txch1ksxu7ynlfna007fzlafafxsgl7lsq038d7cexma3lsh6j4n5hyysv4f07g)
## create puzzle hash, set target amount
    cdv clsp build piggybank/piggybank.clsp
    cdv clsp curry piggybank/piggybank.clsp.hex -a 0x574cfa983d0e24354484db66a68a2e5e11711bf74192056a256eeee09576c968 -a 40 -a 10000000  --treehash
    cdv encode eb3f76bd4f51d601f4d2c58690ffca7ba9b4ec7e222c693eca7829fe260d0f16 --prefix txch
    送錢給標準地址

## contributions spend (從自己的錢包分出一部分的錢 拿來存)
    cdv clsp build piggybank/contribution.clsp
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb94a99bd56f43b5d4ab1a3eae5919ed29d897fdc662ba0cab8013a5a9d05d31ccd56c9b24bbd7cf9509f98c88ada438d --treehash
    cdv encode b40dcf127f4cfaf7f922ff53d49a08ffbf003e276fb1936fb1fc2fa95674b909 --prefix txch
   送錢給標準地址

## set spend bundle json
  
### coin1
    cdv rpc coinrecords --by puzhash eb3f76bd4f51d601f4d2c58690ffca7ba9b4ec7e222c693eca7829fe260d0f16 -nd
    puzzle_reveal:
    cdv clsp curry piggybank/piggybank.clsp.hex -a 0x574cfa983d0e24354484db66a68a2e5e11711bf74192056a256eeee09576c968 -a 40 -a 10000000  -x
    solution:
       opc '(46 500 0xeb3f76bd4f51d601f4d2c58690ffca7ba9b4ec7e222c693eca7829fe260d0f16 40 90 130)'

### coin2
    cdv rpc coinrecords --by puzhash b40dcf127f4cfaf7f922ff53d49a08ffbf003e276fb1936fb1fc2fa95674b909 -nd
      puzzle_reveal:
    cdv clsp curry piggybank/contribution.clsp.hex -a 0xb94a99bd56f43b5d4ab1a3eae5919ed29d897fdc662ba0cab8013a5a9d05d31ccd56c9b24bbd7cf9509f98c88ada438d -x
      solution:(piggybank token / new amount)
      opc '(0xf5921e8a28057056e312359a1623c9956350188e1c568b055cde88f4587fc144 900)'

### aggregated_signature
    python3 piggybank/sign_contribution.py

## send tx 
    cdv rpc pushtx spend_bundle.json 

## check
### withdraw
1. receiver receive withdraw_amount
   cdv rpc coinrecords --by puzhash 574cfa983d0e24354484db66a68a2e5e11711bf74192056a256eeee09576c968
   has a coin with "spent_block_index": 0 / amount: withdraw_amount
2. vault remain vault_after_withdraw_amount
   cdv rpc coinrecords --by puzhash 6a0326da0282f6d521f2f80d9b96c120fd5fd1bd7a20d49c75bf7490e07e345d
   has a coin with "spent_block_index": 0 / amount: vault_after_withdraw_amount

### deposit

# test code (driver)
cdv test
# other 
 ->(ERROR)One or more of the specified objects was not a spend bundle: bytes object is expected to start with 0x
 ->refer: https://docs.chia.net/guides/chialisp-first-smart-coin/ to add 0x
 -> -m 0.000006 --override 
 -> spent_block_index has value: means "spent true"

TODO:
- input: curry (o)
- input: multi input (o)
- contract: function without using (o)
- contract: main func (o)
- test withdraw: vault:100 user send: 40 withdraw_amount: 40 vault_after_withdraw_amount:100 (o)
- test withdraw: vault:100 user send: 30 withdraw_amount: 40 vault_after_withdraw_amount:90 (o)
- test deposit: vault:100 user send:40 vault_after_deposit_amount:140 
- success_number : hash by user name / secret key (o)
- delete all comment (o)
- drivers code
- test code
- recover deleted comment