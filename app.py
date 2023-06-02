from api import JustNews
urls = [
        "https://tvn24.pl/tvnwarszawa/komunikacja/warszawa-tragiczny-wypadek-na-torach-nie-zyje-15-latka-utrudnienia-na-dworcu-gdanskim-6236826",
        "https://wydarzenia.interia.pl/zagranica/news-tragiczny-wypadek-w-australii-dzieci-utknely-w-samochodzie-n,nId,6502404",
        "https://www.rmf24.pl/regiony/lublin/news-tragiczny-wypadek-w-annopolu-zginela-64-latka,nId,6489231#crp_state=1",
        "https://wiadomosci.wp.pl/koszmarny-wypadek-tragedia-w-warszawie-6832508693797568a",
        "https://wiadomosci.wp.pl/ciezarowka-ze-zwierzetami-wywrocila-sie-wypadek-na-slowackiej-autostradzie-6845506349927136a",
        "https://www.rmf24.pl/regiony/trojmiasto/news-tragiczny-wypadek-w-bialym-blocie-zginely-dwie-osoby,nId,6436089#crp_state=1",
        "https://remiza.com.pl/wypadek-na-dk62-nie-zyje-jedna-osoba/",
        "https://dziennikzachodni.pl/wypadek-w-ustroniu-strazacy-jechali-do-wybuchu-gazu-zderzyli-sie-z-osobowka/ar/c1-17099979",
        "https://dziennikzachodni.pl/pijany-kierowca-wjechal-w-dabrowie-gorniczej-na-wysepke-ronda-z-auta-wyciagneli-go-przechodnie/ar/c1-17160473",
        # "https://torun.naszemiasto.pl/wypadek-w-czarnowie-na-dk-80-nad-ranem-samochod-staranowal/ar/c1-9116891",
        # "https://bialystok.naszemiasto.pl/bialystok-wypadek-przy-sadzieget_text-dwa-samochody-rozbite-dwie/ar/c16-9123509",
        # "https://remiza.com.pl/ustron-wybuch-gazu-w-domu-wielorodzinnym-trwa-dramatyczna-akcja-ratunkowa/",
        # "https://gloswielkopolski.pl/wypadek-w-deborzycach-na-drodze-wojewodzkiej-187-jedna-osoba-zginela-na-miejscu-droga-byla-zablokowana/ar/c16-17162949",
        # "https://wiadomosci.onet.pl/poznan/wypadek-miedzy-czaczem-a-karsnicami-21-latka-zmarla-po-rocznej-walce/l7wnl8p",
        # "https://24tp.pl/n/102136",
        # "https://wpr24.pl/wypadek-wiatrakowca-w-baranowie-foto/",
        # "https://doba.pl/dkl/artykul/wypadek-na-krajowej-osemce-na-wysokosci-lewina-klodzkiego-zderzenie-czolowe-interwencja-lpr/35264/15",
        # "https://gloswielkopolski.pl/wypadek-w-ostrowie-wielkopolskim-ranna-kobieta-trafila-do-szpitala-wideo/ar/c4-17164503",
        # "https://autokult.pl/dramatyczny-wypadek-pod-swiebodzinem-zginelo-dwoch-mezczyzn-z-auta-nic-nie-zostalo,6851198209600352a",
        # "https://wydarzenia.interia.pl/zagranica/news-peru-turysci-uciekaja-z-kraju-ogloszono-stan-wyjatkowy,nId,6534475",
        # "https://wydarzenia.interia.pl/swietokrzyskie/news-karambol-na-drodze-s74-zderzylo-sie-okolo-40-aut-sa-poszkodo,nId,6537495",
        # "https://wydarzenia.interia.pl/zagranica/news-wypadek-z-udzialem-tesli-silnik-wystrzelil-i-wyladowal-45-me,nId,6552006",
        # "https://tvn24.pl/tvnwarszawa/okolice/dawidy-bankowe-wypadek-radiowozu-z-nastolatkami-postepowanie-dyscyplinarne-trwa-sledczy-przesluchuja-swiadkow-6641361",
        # "https://olsztyn.tvp.pl/65830787/tragiczny-skutki-pozaru-nie-zyje-70latek",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/czujka-monitoringu-sklepu-w-jastrz%C4%99biu-da%C5%82a-stra%C5%BCakom-sygna%C5%82-o-po%C5%BCarze-na-miejsce-pojecha%C5%82y-cztery-stra%C5%BCackie-zast%C4%99py-co-si%C4%99-okaza%C5%82o/ar-AA16W18k",
        # "https://www.se.pl/poznan/policyjna-oblawa-i-poscig-za-morderca-w-poznaniu-podejrzany-zginal-w-wypadku-aa-smrg-oJJJ-ebVy.html",
        # "https://glos24.pl/wypadek-na-a4-pod-krakowem-utrudnienia-w-ruchu",
        # "https://twojepajeczno.pl/wiadomosci/wypadek-w-dzialoszynie-dwie-osoby-trafily-do-szpitala/",
        # "https://www.podkarpacie112.pl/wiadomosci/5156-81-latka-stracila-oszczednosci-zycia-i-bizuterie",
        # "https://gazetalubuska.pl/wypadek-podczas-policyjnej-oblawy-na-ulicy-opolskiej-w-poznaniu-nie-zyje-mezczyzna/ar/c1-17251391"
        # "https://gloswielkopolski.pl/grozny-wypadek-w-wielkopolsce-samochod-wypadl-z-drogi-kierowca-trafil-do-szpitala/ar/c1-17284413",
        # "https://epoznan.pl/news-news-136809-wypadek_w_lasku_na_naramowicach_sploszony_kon_zrzucil_amazonke_jest_apel_do_wlascicieli_psow",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/gro%C5%BAny-wypadek-na-dolnym-%C5%9Bl%C4%85sku-trzy-osoby-ranne-po-dachowaniu-pojazdu-zdj%C4%99cia/ar-AA17obPL?li=BBr5KbO",
        # "https://grodzisk.naszemiasto.pl/wypadek-na-trasie-kuznica-zbaska-boruja-koscielna-kierowca/ar/c1-9206695",
        # "https://wiadomosci.wp.pl/trojmiasto/tragedia-na-torach-nie-zyje-23-latek-6865702251461216a",
        # "https://gazetawroclawska.pl/grozny-wypadek-na-dolnym-slasku-trzy-osoby-ranne-po-dachowaniu-pojazdu-zdjecia/ar/c1-17284187",
        # "https://www.zawszepomorze.pl/23-latek-zginal-na-torach-tragiczne-potracenie-w-kartuzach",
        # "https://natemat.pl/468389,smierc-dziennikarki-anny-karbowniczak-nowa-opinia-bieglych-wina-kierowcy",
        # "https://info112.pl/2023/02/12/nie-zyje-mezczyzna-przygnieciony-przez-lodz-tragiczny-wypadek-w-stoczni-jachtowej-foto/",
        # "https://superbiz.se.pl/wiadomosci/quiz-prl-kartki-w-prl-u-pamietasz-takie-zakupy-aa-BMqb-ZsE3-5kJj.html",
        # "https://dziennikbaltycki.pl/tragiczny-wypadek-w-kartuzach-12022023-mlody-mezczyzna-zginal-na-torach/ar/c16-17284287",
        # "https://goniec.pl/pomorskie-dramat-na-torach-w-kartuzach-23-latek-zginal-potracony-przez-ar-wpd-120223",
        # "https://www.lublin112.pl/wjechal-quadem-w-ogrodzenie-poranna-akcja-sluzb-ratunkowych-zdjecia/",
        # "https://www.portalmorski.pl/wiadomosci/inne/52848-tragiczny-wypadek-w-stoczni-jachtowej-w-gdansku",
        # "https://kartuzy.naszemiasto.pl/tragiczny-wypadek-w-kartuzach-mlody-mezczyzna-potracony/ar/c16-9206609",
        # "https://lubelska.policja.gov.pl/lub/aktualnosci/132022,Smiertelny-wypadek-w-Siennicy-Nadolnej.html",
        # "https://www.tuwroclaw.com/wiadomosci,wroclaw-znow-o-wlos-od-tragedii-mezczyzna-wpadl-do-fosy-i-nie-mogl-sie-wydostac,wia5-3315-68926.html",
        # "https://remiza.com.pl/smiertelny-wypadek-na-drodze-wojewodzkiej-nr-812/",
        # "https://trojmiasto.wyborcza.pl/trojmiasto/7,35612,29457036,wypadek-w-stoczni-w-gdansku-mezczyzna-zginal-przygnieciony.html",
        # # "https://zw.lt/swiat/w-nowa-zelandie-uderzy-cyklon-gabrielle/",
        # "https://kuriergarwolinski.pl/garwolin-22173-wypadek-w-goclawiu-cztery-osoby-trafily-do-szpitala,2.html",
        # "https://kurierlubelski.pl/aktualizacja-krasnystaw-smiertelny-wypadek-w-siennicy-nadolnej/ar/c16-17283289",
        # "https://krakow.naszemiasto.pl/niecodzienny-wypadek-pod-krakowem-w-gminie-iwanowice/ar/c16-9206775",
        # "https://torun.naszemiasto.pl/tragiczny-wypadek-na-dk-91-auto-zderzylo-sie-z-tirem-nie/ar/c16-9206769",
        # "https://tenpoznan.pl/81-latka-o-malo-nie-stracila-kilkunastu-tysiecy-zlotych-oszusci-znow-w-akcji/",
        # "https://radioolsztyn.pl/rusza-proces-adwokata-od-trumien-na-kolach-w-wypadku-ktory-spowodowal-zginely-dwie-osoby/01680942",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/niezwyczajny-wypadek-w-gminie-iwanowice-samoch%C3%B3d-wpad%C5%82-do-rzeki-wyl%C4%85dowa%C5%82-na-samym-dnie-d%C5%82ubni-jedna-osoba-poszkodowana/ar-AA17oocC",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/niecodzienny-wypadek-w-gminie-iwanowice-samoch%C3%B3d-wpad%C5%82-do-rzeki-d%C5%82ubni-jedna-osoba-poszkodowana/ar-AA17ohJU",
        # "https://gloswielkopolski.pl/grozny-wypadek-w-wielkopolsce-samochod-wypadl-z-drogi-kierowca-trafil-do-szpitala/ar/c1-17284413",
        # "https://epoznan.pl/news-news-136809-wypadek_w_lasku_na_naramowicach_sploszony_kon_zrzucil_amazonke_jest_apel_do_wlascicieli_psow",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/gro%C5%BAny-wypadek-na-dolnym-%C5%9Bl%C4%85sku-trzy-osoby-ranne-po-dachowaniu-pojazdu-zdj%C4%99cia/ar-AA17obPL?li=BBr5KbO",
        # "https://grodzisk.naszemiasto.pl/wypadek-na-trasie-kuznica-zbaska-boruja-koscielna-kierowca/ar/c1-9206695",
        # "https://wiadomosci.wp.pl/trojmiasto/tragedia-na-torach-nie-zyje-23-latek-6865702251461216a",
        # "https://gazetawroclawska.pl/grozny-wypadek-na-dolnym-slasku-trzy-osoby-ranne-po-dachowaniu-pojazdu-zdjecia/ar/c1-17284187",
        # "https://www.zawszepomorze.pl/23-latek-zginal-na-torach-tragiczne-potracenie-w-kartuzach",
        # "https://natemat.pl/468389,smierc-dziennikarki-anny-karbowniczak-nowa-opinia-bieglych-wina-kierowcy",
        # "https://info112.pl/2023/02/12/nie-zyje-mezczyzna-przygnieciony-przez-lodz-tragiczny-wypadek-w-stoczni-jachtowej-foto/",
        # "https://superbiz.se.pl/wiadomosci/quiz-prl-kartki-w-prl-u-pamietasz-takie-zakupy-aa-BMqb-ZsE3-5kJj.html",
        # "https://dziennikbaltycki.pl/tragiczny-wypadek-w-kartuzach-12022023-mlody-mezczyzna-zginal-na-torach/ar/c16-17284287",
        # "https://goniec.pl/pomorskie-dramat-na-torach-w-kartuzach-23-latek-zginal-potracony-przez-ar-wpd-120223",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/nieszcz%C4%99%C5%9Bliwy-wypadek-w-opoczy%C5%84skim-lokalu-prokurator-bada-okoliczno%C5%9Bci-tragedii/ar-AA17omYE?li=BBr5KbO",
        # "https://newslubuski.pl/interwencje/13924-wypadek-na-obwodnicy-swiebodzina-osobowka-uderzyla-w-drzewo.html",
        # "https://expressbydgoski.pl/to-wydarzy-sie-w-serialu-przysiega-po-weekendzie-wielka-awantura-i-wypadek-narin-120223/ar/c11-17280159",
        # "https://www.radiopik.pl/2,107292,jedna-osoba-ranna-w-wypadku-na-drodze-krajowej-n",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/niecodzienny-wypadek-pod-krakowem-w-gminie-iwanowice-samoch%C3%B3d-wpad%C5%82-do-rzeki-d%C5%82ubni-jedna-osoba-poszkodowana/ar-AA17oi6c",
        # "https://gazetakrakowska.pl/gdzie-jest-wypadek-w-krakowie-12022023-najnowsze-informacje-z-drog/ar/c4p1-21781391",
        # "https://przegladsportowy.onet.pl/sporty-zimowe/narciarstwo-alpejskie/przerazajacy-wypadek-w-ms-to-wygladalo-naprawde-groznie-wideo/ln5bvsf",
        # "https://opoczno.naszemiasto.pl/wypadek-w-opoczynskim-lokalu-prokurator-bada-okolicznosci/ar/c1-9206735",
        # "https://goniec.pl/pomorskie-smiertelny-wypadek-na-budowie-26-latek-poniosl-smierc-na-miejscu-ar-wpd-120223",
        # "https://gwiazdy.wp.pl/halle-berry-miala-wypadek-wyglada-to-koszmarnie-6865720550447712a",
        # "https://wpoznaniu.pl/nocny-wypadek-w-wielkopolsce/",
        # "https://terazgostynin.pl/wiadomosci-gostynin/wypadek-na-drodze-do-gostynina-samochod-dachowal-byli-ranni/yUeUViU3jzAeZ6n1CmC6",
        # "https://radioolsztyn.pl/rusza-proces-adwokata-od-trumien-na-kolach-przez-niego-zginely-dwie-osoby/01680942",
        # "https://kuriergarwolinski.pl/garwolin-22173-wypadek-w-goclawiu-cztery-osoby-trafily-do-szpitala,2.html",
        # "https://kurierlubelski.pl/aktualizacja-krasnystaw-smiertelny-wypadek-w-siennicy-nadolnej/ar/c16-17283289",
        # "https://torun.naszemiasto.pl/tragiczny-wypadek-na-dk-91-auto-zderzylo-sie-z-tirem-nie/ar/c16-9206769",
        # "https://belsat.eu/pl/news/12-02-2023-jest-niski-ukrainski-general-ocenil-stopien-zagrozenia-inwazja-ze-strony-bialorusi/",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/niezwyczajny-wypadek-w-gminie-iwanowice-samoch%C3%B3d-wpad%C5%82-do-rzeki-wyl%C4%85dowa%C5%82-na-samym-dnie-d%C5%82ubni-jedna-osoba-poszkodowana/ar-AA17oocC",
        # "https://www.msn.com/pl-pl/wiadomosci/polska/niecodzienny-wypadek-w-gminie-iwanowice-samoch%C3%B3d-wpad%C5%82-do-rzeki-d%C5%82ubni-jedna-osoba-poszkodowana/ar-AA17ohJU",
        # "https://piensk.naszemiasto.pl/czy-beda-planowane-wylaczenia-pradu-w-piensku-1202/ar/c1p1-20594716",
        # "https://www.iturek.net/rozmaitosci/malanow-wypadek-w-czachulcu-dwie",
]

jn = JustNews(urls=urls, sync=False, parser_name="lxml")
jn.run()
