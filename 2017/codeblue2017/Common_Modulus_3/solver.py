from Crypto.Util.number import *
from Crypto.Random.random import randint

import gmpy


def encrypt(pk, m):
  assert m < pk[0]
  return pow(m, pk[1], pk[0])


def common_modulus_attack(c1, c2, e1, e2, n):
    gcd, s1, s2 = gmpy.gcdext(e1, e2)
    if s1 < 0:
        s1 = -s1
        c1 = gmpy.invert(c1, n)
    elif s2 < 0:
        s2 = -s2
        c2 = gmpy.invert(c2, n)
    v = pow(c1, s1, n)
    w = pow(c2, s2, n)
    for i in xrange(1,1000):
        x = gmpy.invert(2**(8*i*17),n)
        tmp_m,t = gmpy.root((v*w*x)%n,17)
        yield tmp_m

if __name__ == "__main__":
    c1 = 421111161283346431452404838872906910488956231402567019627078538397015129219548039141380131693083805603634832115136344104821561027925864923901767159809798556819390401416411855168293007844311613426948800208007055064348403326803934387258467126612219000171854953396242427891713082121012531213725355828779993888182933907101893044052692649728535361366924432892126370724588453260805681821935597271080255619110465374127164951502400983809536186925456642086304791751551216044579863129291165009342909475237361181743987301745314378124693429484474503217504889965795409106282650296184945237152875186651795552666842345066169360660546054986708172417429052514059615434084086154415920830883055729609108788179781445658162049137989591033198225687070565856609516100367268190340309308157085784134411282761584130225746032198957351227779773001865341915642873414205377145922729731246073639219795924517066513774579919237687232502798978463575009663263447306363691670476046609459059167879832079562689979943552446917015778003739858532004479603764374411135699895655736013845369551111690464128448955486337191304960262873891918387298035244888743768954328136862535082300010994461970837930794524673040694310506226189740828318579439950518115967189869637345638498098713092489244636082588805772227797143449747153355341250697133905040459624514982099584435140538668878747129925880019957973864264834954951976218071371679757509297492047186840975743403271896047156768874314108910566561868784522463064748746223313798316236978642468003218086919263188950066989044210829301678555320837086377545741001736801163743516580353549217680694256032377932133575488109549594325464409000682442042651791171660390153162096538381581148625792618196174157168997050557100450557288143739840824092541232969307054965994887340364612034225310418659933594966854225109483090892335755747449339249960596843266176465016510244036725441439565001070917883074011690676911331738356675397441288471244334501091751395240775991013123686801229872759306547212076067886148629332008410208267030715989530663720054487572883736818402878156320070866728567321649066842627412668340251628750512807830348760198570727092664649603270152943231283098179852700308804060616603604109118233213539629764618927518884532667481665405755714542980086417296700138731812815602896287231173509006149715343922041354056256194681983557852276963918040964106582078239501915086320391282791023780691061950154312894926940866878046518974877055347229774579384836298084254309194742164500782L
    c2 =905336011260893181451937420601175770518313987534058470576409049452599974940736949020892631904955374029696187995214208522797070994604711663756814784706053753391830801248808142181434422224620348115969075398677162880328104668870990618955018212918253536803780269490731174871303579036880145367252409300321511403369634435527150000969450834032455903281526350857234024199221097951905683106432984567192925721856154512618509568221546898136983740670694848845816274649037002810596080076911851084982546841069002779200879395931456796911067433329924739943299552475793965462348342813683729525726622940637841204356613245154725191731818570068876251576706021876289420301350487275708440713574921631267131651109260124766475594710481161866254565495750886839979733888772439130815149472846472765436552529628205718020374215877005469575372812773398343007234021177110808440750777736752300216949812950208548770769356889084232841311299404061610926387440620373137543532240294565244268885021138356121583352086433040479579285669028705571672002026293450745788592556823683194951826864141604029265650908715426822940827714455571796485962047146479512064410497475912291097113335318214286537554114706858926411912595063427662813512257156617697572638072509013871077829931469009241562237896598800666350337578826848041056097241547835195327840625894306586665539851835002956883837883293039313345815320389859457247452362675082429215289259947007386622301346393036750250168159297672722825807855637539796284414040339895615478904699195785762873300869004533530925681372154050324943727448464697359515536114806520493724557784204316395281200493439754546212305945038548703862153513568552164320556554039878316192239576925690599059819274827811660423411125130527352853059068829976616766635622188402967122171283526317336114731850274527784991508989562864331372520028706424190362623058696630974348010681878756845430600722349325469186628612347668798617024215127322351935893754437838675067920448401031834465304168738463170328598024532652790234530162187677742373772610227011372650971705426850962132725369442443471111605896253734934335599889785048210986345764273409091402794347076211775580564523705131025788768349950799136508286891544854890654019681560870443838699627458034827040931554727774022911060988866035389927962128604944287104134091087855031454577661765552937836562030914936714391213421737277968877508252894207799747341644008076766221537325719773971004607956958298021339118374168598829394997802039272072755111105775037781715L
    e1 = 13218197
    e2 = 13325773

    n = 968303207185607392933798782387689522656147561712795299283882287440997111985337043607347852676675972362918419582716466493901827460706450708953088746657795254328535683015238473202723829157430427867421087226189467195646844668802837819623414935635764658530099227590830741510249221895574884771436827770318305551317176839494597881542410308108175111834839215570956517340899194288784858826431213509713952528866287993390613948062491441610747107348648602379185114554723774040662560407455840832110271813933032624805073788024993067973148443925303253795470847563536231692617336003345253420781728080545107013979989225215051608062044642404350318860297552684325830122651066498471494796197140830046228424107290568844093340204267361082742078820287806283549564233943675107998076566543352390069511549956964748416720763513751358887667167332126080075430087233981966806427580520370257808050907653401104327326631097877139317246068499669501296942050536122626128764679345686334508003799157031148558906404519754488943090430614449734145826672306815863417618237639635345018467258462900064790890385390508718602990300495726938127324285656651880960536234978827321187318512537049899040749483345012221361131129792213254633506153185302186568540749980375628514235030855807045314709882496753074374605804287524700316006092896795420448048753563680014346711220542647330945566829248331838201572696721484611259634434782075831402355726031168909134250473545733318680648535591393583591753681796583867361941369612638709097786386797652973805166862674686551290098101135899770942208220247225222462958306451292887778107274202080862990165408064372884914158792725013116440247234948462221463395579778209416361358418236648009499845276591742121866289571920719060295618309551857388542560147442529378101156132620061921583469878917947302508627776695573047820182057510772384875135795550437710313658255283287862276198618250884260442348343850066240114035518636573845052654416580159067713183299304803538785632234238046467384672538122045063632667757962772674939972792679509851714820791391542209183895101043149418861154827906828713093460640624918161442498432261330207213585143333235283987920999836862245963629061098253465280043891903366631221500293216287006734530837307036369234284523611530022158837165369780256375911835104289853776157817361701638375344905311830460059612259798600223588322136072986423796319913187356442617636479007538166981641749486826645166479345057550622122298936583765413411917302326827553940008588471939786317L
    # print c1
    # print c2
    tm = common_modulus_attack(c1,c2,e1,e2,n)
    f = False
    while f == False:
        try:
            m = hex(next(tm))[2:].decode('hex')
        except TypeError:
            continue
        if m.startswith('CBCTF{') == True:
            f = True
            print m