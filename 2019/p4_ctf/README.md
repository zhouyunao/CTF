p4 team手かけた(?)CTFをチームm1z0r3として参加しました。  
自分は暗号の二問を解いた。  

[:contents]  
# 競技中解いた問題  
## Count me in!  (crypro 59pts)  
ある意味の総当たり  
まずは問題文  
```
import multiprocessing

from Crypto.Cipher import AES

# from secret import key, flag
key = "0"*16
counter = 0
aes = AES.new(key, AES.MODE_ECB)


def chunk(input_data, size):
    return [input_data[i:i + size] for i in range(0, len(input_data), size)]


def xor(*t):
    from functools import reduce
    from operator import xor
    return [reduce(xor, x, 0) for x in zip(*t)]


def xor_string(t1, t2):
    t1 = map(ord, t1)
    t2 = map(ord, t2)
    return "".join(map(chr, xor(t1, t2)))


def pad(data):
    pad_byte = 16 - len(data) % 16
    return data + (chr(pad_byte) * pad_byte)


def worker_function(block):
    global counter
    print "start worker {} ".format(counter)
    key_stream = aes.encrypt(pad(str(counter)))
    result = xor_string(block, key_stream)
    counter += 1
    print "end worker {}".format(counter-1)
    print result.encode("hex")
    return counter-1


def distribute_work(worker, data_list, processes=8):
    pool = multiprocessing.Pool(processes=processes)
    result = pool.map(worker, data_list)
    pool.close()
    return result


def encrypt_parallel(plaintext, workers_number):
    print 'start parallel'
    chunks = chunk(pad(plaintext), 16)
    results = distribute_work(worker_function, chunks, workers_number)
    return results


# def main():
    plaintext = """The Song of the Count

You know that I am called the Count
Because I really love to count
I could sit and count all day
Sometimes I get carried away
I count slowly, slowly, slowly getting faster
Once I've started counting it's really hard to stop
Faster, faster. It is so exciting!
I could count forever, count until I drop
1! 2! 3! 4!
1-2-3-4, 1-2-3-4,
1-2, i love couning whatever the ammount haha!
1-2-3-4, heyyayayay heyayayay that's the sound of the count
I count the spiders on the wall...
I count the cobwebs in the hall...
I count the candles on the shelf...
When I'm alone, I count myself!
I count slowly, slowly, slowly getting faster
Once I've started counting it's really hard to stop
Faster, faster. It is so exciting!
I could count forever, count until I drop
1! 2! 3! 4!
1-2-3-4, 1-2-3-4, 1,
2 I love counting whatever the
ammount! 1-2-3-4 heyayayay heayayay 1-2-3-4
That's the song of the Count!
"""
#     encrypted = encrypt_parallel(plaintext, 32)
    # print(encrypted.encode("hex"))


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

```
出力は↓  
```
9d5c66e65fae92af9c8a55d9d3bf640e8a5b76a878cbf691d3901392c9b8760ebd5c62b22c88dca9d1c55098cbbb644ae9406ba32c8293bdd29139bbc2b4605bba51238f2cb399a9d0894ad9cbb8774be9406ce66fae89a6c8ef7ad9c4b87442ad1470af78e19da6d8c55096d2b9750ea8586fe668a085c2ef8a5e9cd3be6c4bba144ae66ba488e8df84418bceb2650ea84362bf0688dcabd3905d8d87a46d414626be04a58215b84263a620de3203fa4626be08e2940da35c61b82c98201ce15438cd67eb921cf77c28a969de321bf4433ea24ca59216a25b7bb662996106e11639e75ae09015bb4c2fb76d8c254fe15e6ab45cea817391547cab698c6d4ff35039b34df7df599e412fb67fde3200b55432a441f19817b01405962c9d2e1af9556aa447f09f0df75360ad6988241db91129a85deb8559a25b7bb660de084ff1cc3a0e8041bc71d71fb29883931d9d3e8f784ca743b065c91ea386909e1a9100925f4fa742b1718c1efec4d4d609df5bcb3b17e417bd268d5fe6ced4d65b9c40d6305eeb1df03e9050e68bcad241dd15b46453b85dae7cd112b2c3c7ca50dd4ddf2c1ff350f5349c5febcadbd2509c40d6340aad03bd258d5bb2d8cdc647d814d1335efe18f8718651e7c5d6b9609c57d12010fe50e939801ee1dbcbd74cce4739c1eeceba8ef87360b629ed82a6eb9d508ee381bb88e97363bf20a1cfe7a7e07cccf3cea788bd277fb265e9cde4a9b937808aa7ee85f22679a365f5c4ede5f478c0e482ab95bd3c79f731e9c9a8b6ff7cc2e6c0e0c897047fb22ba1e5afa8b778c2ef80abcabd1a37b42af4c2fce5fa60dde582a8c7971a37b42af4c2fce5e475c1f782b7cabd207bb832edd5a4e5e4130a976ad4a2fe86ac99c18491f9f6c86adae59cc4a9f33072f70ca6daede5e40b049272c8e6b980b798c69e9fb7f7891611c7758df0fc82b481d1ca9eb8e2cd5f118f26def6f693d2abc99982bce2855f038175d9e7ebcdf8a4dcca9faab0da1045857eceebed8ab68a89e0bff9f3c60a098426ceedec8daccdce8584bce6cc0d49c065c2f7f797f898c69e9fb5b0e05f019269dd88a8c2f8df89cac5f8b09d00ad16dc760ead7c3518baed47603c5b5251cc269cae93d1f8a4888699aff58942c8529f304af0362143f2bd1e37670d538753992129ff3c6c5befb21e7331590c950ac26917be39644dfba50b2b70117fcbccba57b209ae95721a1c9d36073d934b75014109102be14fb6a044a7cf9e468748976457f6342177f5a9042630622f97d2ba5a8c04a7890d4e5fcb445b7600d7c1be71b711b6b32b4444f078557ef82e4f0559225437b455aa9a0bbaff89c834531a45115125c933d6cd6cdca8f8
```  
問題文を眺めてみたら、`multiprocess`の一個のprocessが終わった度に`counter`が1を増やすというシステムでした。よって、`keystream`が被る可能性があります。ですから前のkeystreamを使って最後の暗号文とxor取ればflagが降ってくる.
```
from count import *

ct = "9d5c66e65fae92af9c8a55d9d3bf640e8a5b76a878cbf691d3901392c9b8760ebd5c62b22c88dca9d1c55098cbbb644ae9406ba32c8293bdd29139bbc2b4605bba51238f2cb399a9d0894ad9cbb8774be9406ce66fae89a6c8ef7ad9c4b87442ad1470af78e19da6d8c55096d2b9750ea8586fe668a085c2ef8a5e9cd3be6c4bba144ae66ba488e8df84418bceb2650ea84362bf0688dcabd3905d8d87a46d414626be04a58215b84263a620de3203fa4626be08e2940da35c61b82c98201ce15438cd67eb921cf77c28a969de321bf4433ea24ca59216a25b7bb662996106e11639e75ae09015bb4c2fb76d8c254fe15e6ab45cea817391547cab698c6d4ff35039b34df7df599e412fb67fde3200b55432a441f19817b01405962c9d2e1af9556aa447f09f0df75360ad6988241db91129a85deb8559a25b7bb660de084ff1cc3a0e8041bc71d71fb29883931d9d3e8f784ca743b065c91ea386909e1a9100925f4fa742b1718c1efec4d4d609df5bcb3b17e417bd268d5fe6ced4d65b9c40d6305eeb1df03e9050e68bcad241dd15b46453b85dae7cd112b2c3c7ca50dd4ddf2c1ff350f5349c5febcadbd2509c40d6340aad03bd258d5bb2d8cdc647d814d1335efe18f8718651e7c5d6b9609c57d12010fe50e939801ee1dbcbd74cce4739c1eeceba8ef87360b629ed82a6eb9d508ee381bb88e97363bf20a1cfe7a7e07cccf3cea788bd277fb265e9cde4a9b937808aa7ee85f22679a365f5c4ede5f478c0e482ab95bd3c79f731e9c9a8b6ff7cc2e6c0e0c897047fb22ba1e5afa8b778c2ef80abcabd1a37b42af4c2fce5fa60dde582a8c7971a37b42af4c2fce5e475c1f782b7cabd207bb832edd5a4e5e4130a976ad4a2fe86ac99c18491f9f6c86adae59cc4a9f33072f70ca6daede5e40b049272c8e6b980b798c69e9fb7f7891611c7758df0fc82b481d1ca9eb8e2cd5f118f26def6f693d2abc99982bce2855f038175d9e7ebcdf8a4dcca9faab0da1045857eceebed8ab68a89e0bff9f3c60a098426ceedec8daccdce8584bce6cc0d49c065c2f7f797f898c69e9fb5b0e05f019269dd88a8c2f8df89cac5f8b09d00ad16dc760ead7c3518baed47603c5b5251cc269cae93d1f8a4888699aff58942c8529f304af0362143f2bd1e37670d538753992129ff3c6c5befb21e7331590c950ac26917be39644dfba50b2b70117fcbccba57b209ae95721a1c9d36073d934b75014109102be14fb6a044a7cf9e468748976457f6342177f5a9042630622f97d2ba5a8c04a7890d4e5fcb445b7600d7c1be71b711b6b32b4444f078557ef82e4f0559225437b455aa9a0bbaff89c834531a45115125c933d6cd6cdca8f8"

cct = chunk(ct.decode('hex'),16)

plaintext = plaintext + 'flag'*16
ppt = chunk(plaintext,16)


for c in range(57,61):
    print '-'*64
    for k in range(57):
        ks = xor_string(cct[k],ppt[k])
        print xor_string(cct[c],ks)

```
## Bro,do you even lift  (crypro 85pts)  
モニック多項式からflagを計算する
まず問題文から
```
#lift.sage
flag = int(open('flag.txt','r').read().encode("hex"),16)
ranges = int(log(flag,2))
p = next_prime(ZZ.random_element(2^15, 2^16))
k = 100
N = p^k
d = 5
P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
pol = 0
for c in range(d):
    pol += ZZ.random_element(2^ranges, 2^(ranges+1))*x^c
print(pol)
remainder = pol(flag)
print(remainder)
pol = pol - remainder
print(pol(flag))
assert pol(flag) == 0

print(p)
print(pol)

```  
```
# out.txt
35671
12172655049735206766902704703038559858384636896299329359049381021748*x^4 + 11349632906292428218038992315252727065628405382223597973250830870345*x^3 + 9188725924715231519926481580171897766710554662167067944757835186451*x^2 + 8640134917502441100824547249422817926745071806483482930174015978801*x + 170423096151399242531943631075016082117474571389010646663163733960337669863762406085472678450206495375341400002076986312777537466715254543510453341546006440265217992449199424909061809647640636052570307868161063402607743165324091856116789213643943407874991700761651741114881108492638404942954408505222152223605412516092742190317989684590782541294253512675164049148557663016927886803673382663921583479090048005883115303905133335418178354255826423404513286728
```  
最初はよくわからなかった。  
問題文はsageファイルだからまずその線で調べてみても何もわからなかった。
後半ちょっとRSAに対するcoppersmith攻撃を見てみたところ<b>モニック多項式</b>ということを気付いた。

モニック多項式の一般形は:  
<img src="http://chart.googleapis.com/chart?cht=tx&chl=\Large x^{n} %2B c_{n-1}x^{n-1} %2B .... %2B c_{2}x^2 %2B c_{1}x %2B c_0" style="border:none;">  
今回のout.txtをみると  
<img src="http://chart.googleapis.com/chart?cht=tx&chl=\Large c_4x^{4} %2B c_{3}x^{3} %2B c_{2}x^2 %2B c_{1}x %2B c_0" style="border:none;">  
というあと一歩のところの感じがします。  
ですので`c4`の逆数をかけてまず一般形に変換してsage特有の`small_roots`という関数を使って答えを求める。  
あと気を付けるものとしては解`x`の上限を設定しなくては行けないらしいので。問題文から以下のような式で解の上限を計算しました`int(log(c0,2))+1=223`  
```
# solver.py
#flag = int(open('flag.txt','r').read().encode("hex"),16)
flag = int('p4{fffffffffffffffffffffff}'.encode("hex"),16)
ranges = int(log(flag,2))
p = 35671
k = 100
N = p^k
d = 5
P.<x> = PolynomialRing(Zmod(N), implementation='NTL')
pol = 12172655049735206766902704703038559858384636896299329359049381021748*x^4 + 11349632906292428218038992315252727065628405382223597973250830870345*x^3 + 9188725924715231519926481580171897766710554662167067944757835186451*x^2 + 8640134917502441100824547249422817926745071806483482930174015978801*x + 170423096151399242531943631075016082117474571389010646663163733960337669863762406085472678450206495375341400002076986312777537466715254543510453341546006440265217992449199424909061809647640636052570307868161063402607743165324091856116789213643943407874991700761651741114881108492638404942954408505222152223605412516092742190317989684590782541294253512675164049148557663016927886803673382663921583479090048005883115303905133335418178354255826423404513286728
# a0 = 170423096151399242531943631075016082117474571389010646663163733960337669863762406085472678450206495375341400002076986312777537466715254543510453341546006440265217992449199424909061809647640636052570307868161063402607743165324091856116789213643943407874991700761651741114881108492638404942954408505222152223605412516092742190317989684590782541294253512675164049148557663016927886803673382663921583479090048005883115303905133335418178354255826423404513286728
c0 = 12172655049735206766902704703038559858384636896299329359049381021748
d = inverse_mod(c0,N)
pol = pol * d
print(pol.is_monic())
# pol = pol - N
print(pol)
print(len(str(N^(1/4))))

xx = 2**223 # xxは解の上限int(log(c0,2))+1=223
print(pol.small_roots(xx))
# print(p)
# print(pol)
# flag p4{Th4t5_50m3_h34vy_l1ft1n9}

```
