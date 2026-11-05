"""Generates the Ulbrich Hidroavtomatika redesign pages into ./site."""
import os, re, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
I = "assets/img/"
E = html.escape

# ---------------------------------------------------------------- data
CATS = [
    dict(slug="kemicno-tehnicni-proizvodi", name="Kemično-tehnični proizvodi", short="Kemija",
         tag="Recepti za uspeh", icon="menu_11.jpg", hero="hf/01_grease.jpg", fit=False,
         float="hf/02_adhesive.jpg",
         intro="Maziva, lepila, tesnilne mase in elektro-kemikalije vodilnih svetovnih proizvajalcev. Molykote®, Dowsil™, Permabond, ThreeBond in drugi, z nasvetom, kateri izdelek je pravi za vaš proces.",
         bullets=["Maziva", "Lepila", "Tesnilno-lepilne mase", "Elektro-kemikalije", "Silikonski materiali", "Proizvodi za letalsko industrijo", "Spajke in paste"],
         subs=[("Maziva", "menu_40.jpg"), ("Lepila", "menu_38.jpg"), ("Tesnilno-lepilne mase", "menu_54.jpg"), ("Elektro-kemikalije", "menu_37.jpg"),
               ("Silikonski materiali", "menu_35.jpg"), ("Protikorozijska zaščita", "menu_41.jpg"), ("Spajke in paste", "menu_179.jpg"),
               ("Čistila in topila za lepila, tesnilne mase in maziva", "menu_180.jpg")],
         brands=["dupont", "dowcorning", "xiameter", "krytox", "permabond", "threebond", "plexus", "bostik", "hbfuller", "panacol", "electrolube", "mgchemicals", "elsold", "jax", "molydal", "lubrilog", "tectyl", "zipchem", "merbenit"]),
    dict(slug="uv-tehnologija", name="UV tehnologija", short="UV",
         tag="Visoko intenzivni viri za učinkovito delo", icon="menu_45.jpg", hero="hf/03_uv.jpg", fit=False, float="hf/03_uv.jpg",
         intro="UV sistemi za sušenje lepil, barv in zalivnih mas, simulacijo sončnega sevanja in testiranje PV panelov. Od UV LED do merilnikov intenzitete, v sodelovanju z Dr. Hönle AG.",
         bullets=["Naprave za sušenje lepil, barv in zalivnih mas", "Naprave za simulacijo sončnega sevanja", "Naprave za testiranje PV panelov", "UV metri za merjenje intenzitete UV sevanja", "UV LED"],
         subs=[("Naprave za sušenje lepil, barv in zalivnih mas", "menu_47.jpg"), ("Naprave za simulacijo sončnega sevanja", "menu_48.jpg"),
               ("Naprave za testiranje PV panelov", "menu_49.jpg"), ("Naprave za dezinfekcijo", "menu_50.jpg"),
               ("UV metri, naprave za merjenje intenzitete UV sevanja", "menu_51.jpg"), ("UV LED", "menu_52.jpg")],
         brands=["hoenle", "panacol"]),
    dict(slug="dozirna-tehnika", name="Dozirna tehnika", short="Doziranje",
         tag="Enostavno, natančno, učinkovito", icon="menu_159.jpg", hero="hf/04_dispense.jpg", fit=False, float="hf/04_dispense.jpg",
         intro="Od ročnih dozirnih pištol do XYZ dozirnih sistemov in 2K mešanja. Natančno nanašanje lepil, tesnilnih mas in maziv, ponovljivo pri vsakem kosu.",
         bullets=["Dozirne pištole", "Dozirni ventili", "2K mešalni sistemi", "Pripomočki in potrošni material", "Dispenzerji in kontrolerji za dozirne ventile"],
         subs=[("Dozirne pištole", "menu_161.jpg"), ("Dozirni ventili", "menu_162.jpg"), ("XYZ dozirni sistemi", "menu_163.jpg"), ("2K mešalni sistemi", "menu_164.jpg"),
               ("Pripomočki in potrošni material", "menu_165.jpg"), ("Dispenzerji in kontrolerji za dozirne ventile", "menu_170.jpg"),
               ("Odsesovalne naprave", "menu_183.jpg"), ("Lube Dispensing", "menu_243.jpg")],
         brands=["techconsystems", "metermix", "mycronic", "buehnen", "panacol"]),
    dict(slug="plazemska-tehnologija", name="Plazemska tehnologija", short="Plazma",
         tag="Sodobni in zanesljivi generatorji atmosferske plazme", icon="menu_230.jpg", hero="hf/05_plasma.jpg", fit=False, float="hf/05_plasma.jpg",
         intro="Uporaba plazme vse bolj postaja sodoben tehnološki standard v različnih vejah industrije in je eno najhitreje razvijajočih se tehnoloških področij.",
         bullets=["Aktivacija površin za boljše omočenje pred lepljenjem, tesnjenjem, tiskanjem in barvanjem", "Ultra fino čiščenje površin in odstranjevanje oksidov", "Učinkovito uničevanje klic in nevtralizacija vonjav", "Stimulacija regeneracije tkiv pri oskrbi ran", "Pospeševanje kemijskih reakcij"],
         products=[
             ("piezobrush® PZ3", "full_piezobrush_PZ3_with_transport_case_for_online.jpg", False, "Najmanjša ročna plazemska naprava na svetu. Kompaktna naprava za laboratorije, proizvodnje, montaže in prototipne delavnice, ki troši vsega 18 W."),
             ("piezobrush® PZ3-i", "full_piezobrush_PZ3i.jpg", False, "Enota za hladno plazmo, zasnovana za integracijo v nove in obstoječe proizvodne linije. Izjemno kompaktna, varna in učinkovita."),
             ("PB3/PS2000", "full_PB3_PS2000_High_performance_atmospheric_plasma_system.jpg", True, "Visokozmogljiv sistem atmosferske plazme v robustni industrijski izvedbi: 19-palčna visokonapetostna enota PS2000 in plazemski generator PB3."),
             ("Plasmatool", "full_Plasmatool.jpg", False, "Visoko učinkovita ročna naprava za aktivacijo in čiščenje površin s pomočjo atmosferske plazme."),
             ("Avtomatizacija plazmiranja", "full_Automation_solutions_for_plasma_applications.jpg", True, "ULBRICH Automation združuje tehnično kompetenco, tehnologijo avtomatizacije ter več kot 60 let inženirskih izkušenj."),
             ("Plasma Nozzles for PB3/PS2000", "full_PLASMA_NOZZLES.jpg", True, "Visokozmogljive šobe za delovanje s pulznim atmosferskim oblokom (PAA®) in napajalnikom PS2000."),
             ("3D tisk s plazemsko aktivacijo", "full_Maximum_Surface_Quality_in_3D_Printing_through_Plasma_Activation.jpg", False, "Najvišja kakovost površine pri 3D tisku FDM s plazemsko aktivacijo podlage."),
             ("Starter Kit Gas in Electrical", "full_Starter_Kit_Gas_Electrical.jpg", True, "Priklopite in začnite. Potrebujete le stisnjen zrak in električno vtičnico, s priborom sestavite celoten plazemski sistem v nekaj korakih."),
             ("Plasma Treatment Software", "full_Plasma_Treatment_Software.jpg", True, "Vse funkcije sistema na enem mestu. Primerno za servisiranje in oddaljeno vzdrževanje."),
             ("Testink-Pins", "full_Testink_Pins.jpg", True, "Za hitro in enostavno oceno površinske energije trdnih snovi. Netoksično, brez tveganja za zdravje uporabnika."),
         ],
         brands=["relyon_plasma", "stts"]),
    dict(slug="naprave-za-ciscenje", name="Naprave za čiščenje", short="Čiščenje",
         tag="V elektroniki in industriji", icon="menu_242.jpg", hero="hf/06_cleaning.jpg", fit=False, float="hf/06_cleaning.jpg",
         intro="Za zagotovitev daljše življenjske dobe in višje kvalitete izdelkov. DCT čistilne naprave obsegajo več kot dvajset tipov naprav za čiščenje tiskanih vezij po spajkanju, mask in sit, filtrov spajkalnih naprav in nosilnih okvirjev.",
         bullets=["Čiščenje tiskanih vezij po spajkanju", "Čiščenje mask, sit in rakelj", "Vzdrževalno čiščenje reflow peči", "Čistila, razvita skupaj z napravami"],
         products=[
             ("DCT čistilne naprave", "full_DCT_Cleaning_Machines.jpg", True, "Celovite rešitve čiščenja: čistilni sistemi in čistilna sredstva, razviti in proizvedeni v isti tovarni na Češkem."),
             ("DCT AirJet 4127 CRD", "full_DCT_AirJet_4127_CRD.jpg", True, "Za vzdrževalno čiščenje reflow peči in delov naprav za valovno spajkanje. Avtomatizirani procesi v treh ločenih komorah."),
             ("DCT InJet 388 CD", "full_InJet_388_CD.jpg", True, "Osnovna rešitev za odstranjevanje spajkalnih past s šablon, rakelj in enostranskih napačnih odtisov."),
             ("DCT InJet 388 CRD", "full_DCT_INJET_388_CRD.jpg", True, "Za odstranjevanje spajkalnih past in SMT lepil s šablon, PumpPrintov in rakelj. Primerna tudi za čiščenje tiskanih vezij."),
             ("DCT InJet 388 CRRD Combo", "full_DCT_InJet_388_CRRD_Combo.jpg", True, "Za natančno čiščenje plošč po spajkanju in kakovostno odstranjevanje spajkalnih past in SMT lepil."),
             ("DCT InJet 388 TWIN CRRD", "full_DCT_InJet_388_TWIN_CRRD.jpg", True, "Dvojna izvedba za visoko kapaciteto in natančno čiščenje plošč po spajkanju."),
         ],
         brands=["dct", "kolb", "electrolube"]),
    dict(slug="stroji-naprave-industrijska-hidravlika", name="Stroji, naprave in industrijska hidravlika", short="Hidravlika",
         tag="Proizvodnja na novi, višji ravni", icon="menu_44.jpg", hero="hf/07_press.jpg", fit=False, float="hf/07_press.jpg",
         intro="Lastni razvoj in proizvodnja. Hidravlične sklope, sisteme in naprave ter inteligentne stiskalnice za montaže in preizkušanja razvijamo in izdelujemo v Radljah ob Dravi.",
         bullets=["Stroji in naprave s hidravličnim pogonom in elektronskim krmiljenjem", "Naročniško specifični hidravlični sistemi in naprave", "Proporcionalna in servo tehnika", "Hidravlični agregati, ventili in bloki"],
         subs=[("Stroji in naprave s hidravličnim pogonom in elektronskim krmiljenjem", "menu_55.jpg"), ("Stroji in naprave za železniška vozila", "menu_229.jpg"),
               ("Visokotlačne komponente, kompresorji in sistemi za zrak, pline in tekočine", "menu_174.jpg"), ("Hidravlični cilindri", "menu_12.jpg"),
               ("Hidravlični agregati", "menu_13.jpg"), ("Hidravlični ventili", "menu_15.jpg"), ("Hidravlični krmilni bloki", "menu_16.jpg"),
               ("Proporcionalna in servo tehnika", "menu_17.jpg"), ("Filtri za hidravliko", "menu_19.jpg"), ("Hidravlični sistemi", "menu_14.jpg")],
         brands=["wandfluh", "argo_hytos", "maximator", "aeb_robotics"]),
    dict(slug="managment-hidravlicnih-tekocin", name="Managment hidravličnih tekočin", short="Tekočine",
         tag="Vzdrževanje in nadzor stanja hidravličnih tekočin", icon="menu_8.jpg", hero="hf/08_oil.jpg", fit=False, float="hf/08_oil.jpg",
         intro="Čisto olje pomeni daljšo življenjsko dobo strojev. Naprave za vzdrževanje olj, razvlaževanje in filtriranje ter senzorji, ki stanje tekočin spremljajo sproti.",
         bullets=["Naprave za vzdrževanje olj", "Naprave za razvlaževanje", "Obtočni filtrirni agregati", "Števci delcev", "Senzorji", "Programska oprema"],
         subs=[("Naprave za vzdrževanje in nadzor stanja hidravličnih tekočin", "menu_56.jpg"), ("Senzorji in merilna tehnika", "menu_171.jpg")],
         brands=["argo_hytos"]),
    dict(slug="hidravlicna-in-druga-orodja", name="Hidravlična in druga orodja", short="Orodja",
         tag="Izbira pravih profesionalcev", icon="menu_9.jpg", hero="hf/09_bolting.jpg", fit=False, float="hf/09_bolting.jpg",
         intro="Dvigalke, stiskalnice, snemalci in stroji za vijačenje Power Team in HYTORC. Orodja za montažo in vzdrževanje, kjer je potrebna velika, nadzorovana sila.",
         bullets=["Stroji za vijačenje", "Cilindri in dvigalke", "Stiskalnice", "Snemalci"],
         subs=[("Hidravlične dvigalke in dvigala", "menu_21.jpg"), ("Hidravlične črpalke za orodja", "menu_22.jpg"), ("Mehanski in hidravlični snemalci", "menu_23.jpg"),
               ("Delavniške stiskalnice", "menu_24.jpg"), ("POWER TEAM hidravlični stroji za vijačenje", "menu_27.jpg"), ("Namenska orodja", "menu_28.jpg"),
               ("Ventili", "menu_153.jpg"), ("Dodatki", "menu_26.jpg"), ("HYTORC hidravlični stroji za vijačenje", "menu_25.jpg"),
               ("HYTORC pnevmatski stroji za vijačenje", "menu_175.jpg"), ("HYTORC Electric Bolting Tools", "hytorc_electric.jpg")],
         brands=["hytorc", "ht_power_team", "equalizer"]),
    dict(slug="obvladovanje-gibanja", name="Obvladovanje gibanja", short="Gibanje",
         tag="Ustavljanje bremen še ni bilo lažje", icon="menu_10.jpg", hero="menu_30.jpg", fit=True, float="menu_31.jpg",
         intro="Industrijski amortizerji, oljne zavore, rotacijski dušilci in izolatorji vibracij Weforma. Za mehko zaustavljanje bremen, manj obrabe in tišje stroje.",
         bullets=["Amortizerji", "Oljne zavore", "Rotacijski dušilci", "Zračne vzmeti", "Izolatorji vibracij"],
         subs=[("Amortizerji", "menu_30.jpg"), ("Zračne in plinske vzmeti", "menu_31.jpg"), ("Heavy-duty amortizerji in odbojniki", "menu_34.jpg"),
               ("Rotacijski dušilci", "menu_33.jpg"), ("Oljne zavore in zaviralni cilindri", "menu_145.jpg"), ("Žičnate blazine in izolatorji vibracij", "menu_32.jpg")],
         brands=["weforma"]),
]

PARTNERS = [  # (logo file, name, url, description)
    ("aeb_robotics", "Alutec Robotics", "http://www.alutecsrl.it", "ALUTEC Robotics develops industrial robotic assembly systems, designed to ensure utmost flexibility of both the station itself and of the automated line to which they belong."),
    ("argo_hytos", "Argo-Hytos", "https://www.argo-hytos.com", "As a components and system supplier ARGO-HYTOS is an essential part in the supply chain of the world market leaders when it comes to mobile working machinery and mechanical engineering."),
    ("bostik", "Bostik", "https://www.bostik.com", "Bostik is a world-class leader in sealing and bonding technologies, creating smart adhesive solutions for automotive, high tech, general industry and electronics."),
    ("buehnen", "Bühnen", "https://www.buehnen.de", "BÜHNEN is a company with a success story dating back to 1922, today a specialist in hot melt adhesives and devices for manual and automated bonding."),
    ("dct", "DCT", "https://www.dct.cleaning", "DCT is specialized in providing complete cleaning solutions. DCT cleaning systems and cleaning agents are all developed and produced in the same factory in the Czech Republic."),
    ("dge", "DGE", "https://www.dge-europe.com", "Distributors Group Europe provides a single platform whereby suppliers can market their products throughout Europe through a network of specialty chemical distributors."),
    ("dowcorning", "Dow", "https://www.dow.com", "A global leader in silicones, silicon-based technology and innovation, offering more than 7,000 products and services."),
    ("dupont", "Molykote®", "https://www.molykote.com", "MOLYKOTE® Specialty Lubricants are trusted by engineers, OEMs and product designers worldwide for their ability to meet tough lubrication challenges."),
    ("electrolube", "Electrolube", "https://www.electrolube.com", "Electrolube is a leading manufacturer of electro-chemicals for electronics and industrial manufacturing."),
    ("elsold", "Elsold", "https://www.tamura-elsold.de", "ELSOLD® is a guarantee of premium quality that satisfies the finest connection geometries and enables optimum solderability and great recyclability."),
    ("equalizer", "Equalizer", "https://www.equalizerinternational.com", "Equalizer International was established in 1994 in North-east Scotland and has grown into a world leader in flange maintenance tools."),
    ("hbfuller", "H.B. Fuller", "https://www.hbfuller.com/en", "For 130 years, H.B. Fuller has been a leading global adhesives provider focusing on adhesives, sealants and other specialty chemical products."),
    ("hoenle", "Hönle", "https://www.hoenle.com", "Dr. Hönle AG is one of the world’s leading suppliers for industrial UV technology: UV systems, UV lamps and UV measurement equipment."),
    ("hytorc", "HYTORC", "https://www.hytorc.com", "HYTORC makes industrial bolting safer and simpler, with over 40 years of experience developing industrial torque and tension systems."),
    ("jax", "JAX", "https://www.jax.com", "JAX INC. je proizvajalec industrijskih maziv s sedežem v ZDA, specializiran za visoko zmogljiva sintetična in biološko razgradljiva maziva."),
    ("kolb", "Kolb", "https://www.kolb-ct.com", "Kolb is one of the world’s leading manufacturers of cleaning systems used in the electronics producing industry."),
    ("lubrilog", "Lubrilog", "https://www.lubrilog.fr", "Having joined the Total Group in 2020, LUBRILOG benefits from the power of one of the major players in the lubricants industry."),
    ("krytox", "Krytox®", "https://www.krytox.com", "Chemours™ Krytox® Performance Lubricants combine outstanding lubrication with highly desirable chemical properties."),
    ("maximator", "Maximator", "https://www.maximator.de", "MAXIMATOR GmbH is a leading supplier of high-pressure, testing, hydraulic and pneumatic systems."),
    ("merbenit", "Merz+Benteli", "https://www.merz-benteli.ch", "merz+benteli is an independent Swiss company since 1918, built on a row of technological innovations in adhesives and sealants."),
    ("metermix", "Meter Mix", "https://www.metermix.co.uk", "Meter Mix® Systems Ltd produces innovative, reliable machines for processing single and two-part resin systems."),
    ("mgchemicals", "MG Chemicals", "https://www.mgchemicals.com", "M.G. Chemicals operates an ISO 9001:2015 quality management system, designing products for the specific needs of customers."),
    ("molydal", "Molydal", "https://www.molydal.com", "Molydal is an independent French manufacturer established in 1958 that develops high-performance industrial lubricants and maintenance chemicals."),
    ("mycronic", "Mycronic", "https://www.mycronic.com", "Mycronic je vodilni svetovni ponudnik prilagodljivih, visoko natančnih proizvodnih rešitev za proizvodnjo elektronike."),
    ("panacol", "Panacol", "https://www.panacol.de", "Panacol is an international manufacturer of industrial adhesives, from UV adhesives through structural adhesives to silicones and dispensing devices."),
    ("permabond", "Permabond", "https://www.permabond.com", "Permabond is a leading manufacturer of engineering adhesives, supplying high-quality industrial adhesives to customers worldwide."),
    ("plexus", "ITW Plexus", "https://itwperformancepolymers.com/products/plexus", "ITW Plexus is world renowned for highly engineered fastening, joining and sealing technologies."),
    ("relyon_plasma", "Relyon Plasma", "https://www.relyon-plasma.com", "Relyon plasma iz Regensburga se ukvarja z razvojem in proizvodnjo inovativnih plazemskih tehnologij za industrijo in medicino."),
    ("ht_power_team", "Power Team", "https://hydraulictechnologies.com/brands/power-team/", "Power Team produces high-force tools, from jacks and torque wrenches to hydraulic pumps, cylinders and valves."),
    ("stts", "STTS", "https://www.stts-surface.fr", "STTS is a specialist of electrical discharge surface treatment: Corona and Plasma solutions that improve wettability and adhesion."),
    ("techconsystems", "Techcon", "https://www.techconsystems.com", "Techcon is a provider of precision fluid dispensing and adhesive dispensing equipment."),
    ("threebond", "ThreeBond", "https://www.threebond.co.jp", "Since its founding, ThreeBond’s desire has been to prevent the leakage of precious energy."),
    ("tectyl", "Tectyl", "https://www.valvolineeurope.com", "For more than 85 years, customers around the world have chosen Tectyl as the driving force in rust protection."),
    ("wandfluh", "Wandfluh", "https://www.wandfluh.com", "Wandfluh AG has a comprehensive range of hydraulic components and is a global leader with its special products."),
    ("weforma", "Weforma", "https://www.weforma.com", "Weforma is an innovative German manufacturer of deceleration and vibration dampening technology."),
    ("zipchem", "Zip-Chem", "https://www.zipchem.com", "Zip-Chem Aviation Products: globally approved aircraft chemicals, corrosion inhibitors, cleaners and speciality lubricants."),
    ("xiameter", "Xiameter", "https://www.xiameter.com", "Xiameter offers all the standard silicones you need, the way that works best for you."),
]
PNAME = {p[0]: p[1] for p in PARTNERS}

NEWS = [
    ("16.10.2026", "Industrijska plazemska obdelava površin: trajna vez se začne na površini", "full_linkedin-poszt-sablon-plazma.jpg",
     "Kakovost lepljenega, lakiranega ali potiskanega sestavnega dela ni odvisna le od lepila, laka ali črnila. Enako pomembnih je tistih nekaj vrhnjih mikrometrov površine."),
    ("05.10.2026", "Molykote G-3407: zanesljivo mazanje za vodilne zatiče zavornih čeljusti", "full_Molykote-G-3407-Brake-Caliper-Pin-Grease.jpg",
     "Visokozmogljivo sintetično mazivo na osnovi PAG za vodilne zatiče zavornih čeljusti. Delovno območje od -40 °C do +200 °C."),
    ("23.09.2026", "HÖNLE bluepoint LED: novo", "full_Bluepoint_LED.jpg",
     "Novi bluepoint LED se ponaša z zaslonom na dotik. Z enim zaslonom lahko upravljate do pet enot oziroma skupno 20 LED-glav."),
    ("11.09.2026", "MOLYKOTE P-3300 pasta za navoje", "full_Molykote_P_3300_in_use.jpg",
     "Visoko zmogljiva anti-seize vijačna pasta za zahtevne industrijske montaže in vzdrževalna dela."),
    ("07.10.2026", "Prevodne barve za EMI zaščito pri obrambnih dronih", "full_dow_aero_ENG.jpg",
     "Majhni droni postajajo ključno orodje pri vojaških operacijah in operacijah organov pregona. Prevodne barve jih ščitijo pred elektromagnetnimi motnjami."),
    ("28.08.2026", "Lepila za medicinske pripomočke", "full_01.jpg",
     "Permabond razvija lepila za medicinske pripomočke, kjer sta zanesljivost spoja in biokompatibilnost ključni."),
]

GROUP = [("International", "ulbrich-group.com", "https://www.ulbrich-group.com/"), ("Avstrija", "ulbrich.at", "https://www.ulbrich.at/"),
         ("Hrvaška", "ulbrich.hr", "https://www.ulbrich.hr/"), ("Češka", "ulbrich.cz", "https://www.ulbrich.cz/"),
         ("Nemčija", "ulbrich-gmbh.de", "https://www.ulbrich-gmbh.de/"), ("Madžarska", "ulbrich.hu", "https://www.ulbrich.hu/"),
         ("Slovaška", "ulbrich-sk.sk", "https://www.ulbrich-sk.sk/")]

ARROW = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M3 9h12m0 0-5-5m5 5-5 5" stroke="currentColor" stroke-width="1.8"/></svg>'
ARROW_UR = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 12 12 4m0 0H5m7 0v7" stroke="currentColor" stroke-width="1.7"/></svg>'
PLUS = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1v12M1 7h12" stroke="currentColor" stroke-width="1.7"/></svg>'


# ---------------------------------------------------------------- chrome
def header(active=""):
    cats = "".join(
        f'<a href="{c["slug"]}.html" data-pic="{I}{c["float"]}" class="{"is-on" if i == 0 else ""}"><span class="n">{i + 1:02d}</span>{E(c["name"])}</a>'
        for i, c in enumerate(CATS))
    subs = ""
    for i, c in enumerate(CATS):
        items = c.get("subs") or [(p[0], p[1]) for p in c.get("products", [])]
        links = "".join(f'<a href="{c["slug"]}.html">{E(n)}</a>' for n, _ in items[:10])
        subs += f'<div class="mega-subs {"is-on" if i == 0 else ""}">{links}<a class="all" href="{c["slug"]}.html">Vse o področju {E(c["short"].lower())} &rarr;</a></div>'
    mob = "".join(f'<a href="{c["slug"]}.html">{E(c["name"])}</a>' for c in CATS)
    def a(href, label, key):
        return f'<a href="{href}" class="{"is-active" if active == key else ""}">{label}</a>'
    return f'''
<div class="loader" aria-hidden="true"><div class="lg"><img src="{I}logo_hidro.png" alt=""></div></div>
<header class="hdr">
  <a class="logo" href="index.html" aria-label="Ulbrich Hidroavtomatika, domov"><img src="{I}logo_hidro.png" alt="Ulbrich Hidroavtomatika"></a>
  <nav class="nav">
    <button data-mega class="{"is-active" if active == "proizvodi" else ""}">Proizvodi</button>
    {a("novice.html", "Novice", "novice")}
    {a("partnerji.html", "Partnerji", "partnerji")}
    {a("o-podjetju.html", "O podjetju", "o-podjetju")}
    {a("kontakt.html", "Kontakt", "kontakt")}
    <span class="lang hide-m">SI</span>
    <a class="cta" href="#" data-inquiry="">Povpraševanje</a>
  </nav>
  <button class="burger" aria-label="Meni"><span></span><span></span></button>
</header>
<div class="mega" role="menu">
  <div class="mega-cats">{cats}</div>
  <div>{subs}</div>
  <div class="mega-pic"><img src="{I}{CATS[0]["float"]}" alt=""></div>
</div>
<div class="mega-scrim"></div>
<nav class="mnav">
  <details><summary>Proizvodi</summary><div class="msub">{mob}</div></details>
  <a href="novice.html">Novice</a><a href="partnerji.html">Partnerji</a><a href="o-podjetju.html">O podjetju</a><a href="kontakt.html">Kontakt</a>
  <a href="prosta-delovna-mesta.html">Zaposlitev</a>
  <p style="margin-top:40px"><a class="btn blue" href="#" data-inquiry="" style="font-size:18px;border:0">Pošlji povpraševanje</a></p>
</nav>'''


def footer():
    cl = "".join(f'<a href="{c["slug"]}.html">{E(c["name"])}</a>' for c in CATS[:5])
    cl2 = "".join(f'<a href="{c["slug"]}.html">{E(c["name"])}</a>' for c in CATS[5:])
    return f'''
<footer class="ftr">
  <div class="ftr-top">
    <div><a class="logo" href="index.html"><img src="{I}logo_hidro.png" alt="Ulbrich Hidroavtomatika"></a>
      <p class="muted" style="margin-top:28px;max-width:340px">ULBRICH HIDROAVTOMATIKA d.o.o.<br>Obrtniška ulica 8<br>SI-2360 Radlje ob Dravi</p></div>
    <div><h4>Proizvodi</h4>{cl}</div>
    <div><h4>&nbsp;</h4>{cl2}</div>
    <div><h4>Podjetje</h4><a href="o-podjetju.html">O podjetju</a><a href="partnerji.html">Partnerji</a><a href="novice.html">Novice</a><a href="prosta-delovna-mesta.html">Zaposlitev</a><a href="kontakt.html">Kontakt</a></div>
  </div>
  <a class="ftr-big" href="mailto:info@ulbrich.si">info@ulbrich.si</a>
  <div class="ftr-bot"><span>© 2026 Ulbrich Group</span>
    <nav><a href="https://www.ulbrich.si/iso-certifikat">ISO certifikat</a><a href="https://www.ulbrich.si/quality-policy">Quality policy</a><a href="https://www.ulbrich.si/politika-zasebnosti">Politika zasebnosti</a><a href="https://www.ulbrich.si/code-of-conduct">Code of Conduct</a><a href="https://www.ulbrich.si/piskotki">Piškotki</a></nav></div>
</footer>
<div class="drawer-scrim"></div>
<aside class="drawer" aria-label="Povpraševanje">
  <button class="x" aria-label="Zapri">&times;</button>
  <h2 class="h-l">Povpraševanje</h2>
  <p class="topic"></p>
  <form class="form">
    <input type="hidden" name="tema">
    <label>Ime in priimek<input required name="ime" autocomplete="name"></label>
    <label>Podjetje<input name="podjetje" autocomplete="organization"></label>
    <label>E-pošta<input required type="email" name="email" autocomplete="email"></label>
    <label>Telefon<input name="tel" autocomplete="tel"></label>
    <label>Opišite vaš izziv ali potrebo<textarea name="sporocilo"></textarea></label>
    <button class="btn blue" type="submit">Pošlji povpraševanje <span class="arr">{ARROW}</span></button>
  </form>
  <div class="form-ok"><p class="h-m">Hvala. Vaše povpraševanje smo prejeli.</p><p class="muted" style="margin-top:14px">Strokovnjak za izbrano področje vas bo kontaktiral v najkrajšem možnem času.</p></div>
</aside>
<script src="assets/js/gsap.min.js"></script>
<script src="assets/js/ScrollTrigger.min.js"></script>
<script src="assets/js/lenis.min.js"></script>
<script src="assets/js/main.js"></script>
</body></html>'''


def page(title, body, active="", desc="Ulbrich Hidroavtomatika: kemično-tehnični proizvodi, UV, dozirna in plazemska tehnologija, industrijska hidravlika in orodja. Radlje ob Dravi, od leta 1990."):
    return f'''<!doctype html>
<html lang="sl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex">
<link rel="icon" href="{I}fav512.png"><link rel="preload" href="assets/fonts/SeasonSans-TRIAL-Medium.otf" as="font" type="font/otf" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head><body>
{header(active)}
<main>{body}</main>
{footer()}'''


def lines(*ls):
    return "".join(f'<span class="line"><span>{l}</span></span>' for l in ls)


# ---------------------------------------------------------------- home
def home():
    reel = "".join(
        f'<div class="reel-card {"photo" if c["float"].startswith("hf/") else ""}"><img src="{I}{c["float"]}" alt="{E(c["name"])}"><div class="cap"><span>{E(c["short"])}</span><span>{i + 1:02d}</span></div></div>'
        for i, c in enumerate(CATS))
    rows = "".join(f'''
      <a class="tech-row" href="{c["slug"]}.html">
        <img class="ic" src="{I}{c["icon"]}" alt="">
        <span class="nm">{E(c["name"])}</span>
        <span class="tg">{E(c["tag"])}</span>
        <span class="go">{ARROW}</span>
      </a>''' for c in CATS)
    floats = "".join(f'<img class="{"photo" if c["float"].startswith("hf/") else ""}" src="{I}{c["float"]}" alt="">' for c in CATS)
    plasma = next(c for c in CATS if c["slug"] == "plazemska-tehnologija")
    pcards = "".join(f'''
      <article class="pcard"><div class="pic {"fit" if fit else ""}"><img src="{I}{img}" alt="{E(n)}" loading="lazy"></div>
        <h3>{E(n)}</h3><p>{E(d)}</p></article>''' for n, img, fit, d in plasma["products"][:7])
    logos = "".join(f'<a href="partnerji.html" title="{E(n)}"><img src="assets/logos/{f}.png" alt="{E(n)}" loading="lazy"></a>' for f, n, *_ in PARTNERS[:24])
    news = "".join(f'''
      <a href="novice.html"><div class="pic"><img src="{I}{img}" alt="" loading="lazy"></div><time>{d}</time><h3>{E(t)}</h3></a>''' for d, t, img, _ in NEWS[:4])
    countries = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}<span>{dom}</span></a>' for n, dom, u in GROUP)

    body = f'''
<section class="hero">
  <div class="wrap hero-top">
    <h1 class="h-mega">{lines("Tehnologije, ki", "industrijo držijo", "skupaj.")}</h1>
    <div class="hero-side">
      <p class="lead">Hidravlika, kemija in tehnologija površin. Lastni razvoj in proizvodnja v Radljah ob Dravi, rešitve 37 svetovnih partnerjev.</p>
      <a class="btn" href="#tehnologije">Raziščite področja <span class="arr">{ARROW}</span></a>
    </div>
  </div>
  <div class="hero-band"><div class="reel">{reel}</div></div>
</section>

<section class="statement sec wrap">
  <p class="h-xl">Od leta 1990 smo zanesljiv partner industrije, znan po individualnem pristopu, inventivnih rešitvah in spoštovanju dogovorov.</p>
  <div class="statement-meta">
    <p class="lead" style="color:#fff">Član skupine Ulbrich, ki je že leta 1952 postala prvi evropski distributer specialnih maziv Molykote®.</p>
    <a class="btn white" href="o-podjetju.html">O podjetju <span class="arr">{ARROW}</span></a>
  </div>
</section>

<section class="band" aria-hidden="true"><img data-par src="{I}hf/10_hall.jpg" alt=""></section>

<section class="sec wrap" id="tehnologije">
  <div class="tech-head">
    <h2 class="h-l split-lines">Devet področij.<br>En sogovornik.</h2>
    <p class="muted rv">Od maziva do stiskalnice. Svetujemo, dobavimo in vzdržujemo, z znanjem, ki ga nadgrajujemo z rednimi strokovnimi usposabljanji.</p>
  </div>
  <div class="tech-list">{rows}</div>
  <div class="tech-float">{floats}</div>
</section>

<section class="hscroll">
  <div class="hscroll-pin">
    <div class="wrap hscroll-head">
      <h2 class="h-l">Plazma.<br>Trajna vez se začne<br>na površini.</h2>
      <p class="muted">Aktivacija in ultra fino čiščenje površin pred lepljenjem, tesnjenjem, tiskanjem in barvanjem. Od najmanjše ročne naprave na svetu do popolnoma avtomatiziranih linij.</p>
    </div>
    <div class="track">{pcards}
      <article class="pcard intro"><a class="btn blue" href="plazemska-tehnologija.html">Vsa plazemska tehnologija <span class="arr">{ARROW}</span></a></article>
    </div>
  </div>
</section>

<section class="sec wrap">
  <div class="split">
    <div class="pic"><img data-par src="{I}menu_229.jpg" alt="Hidravlična stiskalnica Ulbrich za železniška vozila"></div>
    <div style="display:flex;flex-direction:column;justify-content:center">
      <h2 class="h-l split-lines">Razvito in izdelano v Radljah ob Dravi.</h2>
      <p class="lead muted rv" style="margin-top:28px">Naš proizvodni program temelji na lastnem tehničnem in tehnološkem razvoju. Leta 2009 smo se vselili v nov, sodobno opremljen poslovno proizvodni objekt.</p>
      <ul class="caps" data-stagger>
        <li><span>01</span><span>Inovativni hidravlični sklopi</span></li>
        <li><span>02</span><span>Hidravlični sistemi in naprave po meri naročnika</span></li>
        <li><span>03</span><span>Inteligentne stiskalnice za montaže in preizkušanja</span></li>
        <li><span>04</span><span>Stroji in naprave za železniška vozila</span></li>
      </ul>
      <p style="margin-top:36px"><a class="link" href="stroji-naprave-industrijska-hidravlika.html">Stroji in industrijska hidravlika {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="sec wrap" style="padding-top:0">
  <div class="nums">
    <div class="num"><div class="v"><span data-count="1949" data-from="1900">1949</span></div><p>Johann Ulbrich ustanovi podjetje, ki danes povezuje skupino Ulbrich po vsej srednji Evropi.</p></div>
    <div class="num"><div class="v"><span data-count="1952" data-from="1900">1952</span></div><p>Prvi evropski distributer specialnih maziv Molykote®.</p></div>
    <div class="num"><div class="v"><span data-count="37">37</span><sup>+</sup></div><p>Svetovnih proizvajalcev, katerih rešitve zastopamo, od Dow in Permabond do HYTORC in Hönle.</p></div>
    <div class="num"><div class="v"><span data-count="7">7</span></div><p>Držav, v katerih deluje skupina Ulbrich. Zanesljivost in prilagodljivost pri dobavah ter tehničnih rešitvah.</p></div>
  </div>
</section>

<section class="sec wrap" style="padding-top:0">
  <div class="tech-head">
    <h2 class="h-l split-lines">Partnerji, ki jim zaupamo.</h2>
    <a class="link rv" href="partnerji.html">Vseh 37 partnerjev {ARROW}</a>
  </div>
  <div class="logos" data-stagger>{logos}</div>
</section>

<section class="sec wrap" style="padding-top:0">
  <div class="tech-head">
    <h2 class="h-l split-lines">Novice</h2>
    <a class="link rv" href="novice.html">Vse novice {ARROW}</a>
  </div>
  <div class="news" data-stagger>{news}</div>
</section>

<section class="sec wrap" style="padding-top:0">
  <div class="group">
    <div class="map"><img src="{I}ulbrich_group.png" alt="Skupina Ulbrich v Evropi" loading="lazy"></div>
    <div>
      <h2 class="h-l split-lines">Skupina Ulbrich</h2>
      <p class="lead muted rv" style="margin-top:24px">Kot eno prvih zahodnih podjetij je Ulbrich v začetku 90. let ustanavljal hčerinska podjetja v srednji in vzhodni Evropi.</p>
      <div class="countries">{countries}</div>
    </div>
  </div>
</section>

{cta_band()}'''
    return page("Ulbrich Hidroavtomatika", body)


def cta_band():
    return f'''
<section class="cta-band sec wrap"><img class="cta-bg" src="{I}hf/11_fluid.jpg" alt="" loading="lazy">
  <div class="cta-grid">
    <h2 class="h-mega">Imate tehnični izziv?</h2>
    <div>
      <p class="lead" style="color:rgba(255,255,255,.8);margin-bottom:28px">Opišite ga. Strokovnjak za vaše področje se vam oglasi s predlogom rešitve.</p>
      <div class="contact-lines"><a href="tel:+38628879910">+386 2 887 99 10</a><a href="mailto:info@ulbrich.si">info@ulbrich.si</a></div>
      <p style="margin-top:32px"><a class="btn blue" href="#" data-inquiry="">Pošlji povpraševanje <span class="arr">{ARROW}</span></a></p>
    </div>
  </div>
  <div class="bar"></div>
</section>'''


# ---------------------------------------------------------------- category
def category(i, c):
    nxt = CATS[(i + 1) % len(CATS)]
    bul = "".join(f"<li>{E(b)}</li>" for b in c["bullets"])
    if c.get("products"):
        tiles = "".join(f'''
        <button class="sub" data-inquiry="{E(n)}"><div class="pic"><img src="{I}{img}" alt="{E(n)}" loading="lazy"></div>
          <div><h3>{E(n)}</h3><p>{E(d)}</p></div><span class="plus">{PLUS}</span></button>''' for n, img, fit, d in c["products"])
        tiles_head = "Izdelki"
    else:
        tiles = "".join(f'''
        <button class="sub" data-inquiry="{E(n)}"><div class="pic"><img src="{I}{img}" alt="{E(n)}" loading="lazy"></div>
          <h3>{E(n)}</h3><span class="plus">{PLUS}</span></button>''' for n, img in c["subs"])
        tiles_head = "Programi"
    brands = "".join(f'<a href="partnerji.html" title="{E(PNAME[b])}"><img src="assets/logos/{b}.png" alt="{E(PNAME[b])}" loading="lazy"></a>' for b in c["brands"])
    words = c["name"].split(" ")
    if len(c["name"]) > 22:
        half = (len(words) + 1) // 2
        h1 = lines(E(" ".join(words[:half])), E(" ".join(words[half:])))
    else:
        h1 = lines(E(c["name"]))
    body = f'''
<section class="phero wrap">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><a href="index.html#tehnologije">Proizvodi</a><span>/</span><span>{E(c["short"])}</span></div>
  <div class="phero-grid">
    <div>
      <h1 class="h-xl">{h1}</h1>
      <p class="lead tagline">{E(c["intro"])}</p>
      <p style="margin-top:36px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn blue" href="#" data-inquiry="{E(c["name"])}">Povpraševanje <span class="arr">{ARROW}</span></a></p>
    </div>
    <div class="phero-pic {"fit" if c["fit"] else ""}"><img src="{I}{c["hero"]}" alt="{E(c["name"])}"><span class="tag">{E(c["tag"])}</span></div>
  </div>
  <ul class="bullets" data-stagger>{bul}</ul>
</section>

<section class="sec wrap">
  <div class="tech-head"><h2 class="h-l split-lines">{tiles_head}</h2><p class="muted rv">Izberite program in nam pošljite povpraševanje. Pripravimo ponudbo in tehnični predlog za vašo aplikacijo.</p></div>
  <div class="subs" data-stagger>{tiles}</div>
</section>

<section class="sec wrap" style="padding-top:0">
  <div class="tech-head"><h2 class="h-l split-lines">Zastopamo</h2><a class="link rv" href="partnerji.html">Vsi partnerji {ARROW}</a></div>
  <div class="brandrow">{brands}</div>
</section>

<a class="nextcat" href="{nxt["slug"]}.html">
  <div><p class="muted" style="margin-bottom:12px">Naslednje področje</p><p class="h-xl">{E(nxt["name"])}</p></div>
  <span class="go" style="flex:none">{ARROW.replace('width="18" height="18"', 'width="56" height="56"')}</span>
</a>
{cta_band()}'''
    return page(f'{c["name"]} | Ulbrich Hidroavtomatika', body, "proizvodi", c["intro"])


# ---------------------------------------------------------------- other pages
def novice():
    items = "".join(f'''
      <a href="#" data-inquiry="{E(t)}"><div class="pic"><img src="{I}{img}" alt="" loading="lazy"></div><time>{d}</time><h3>{E(t)}</h3><p>{E(x)}</p></a>''' for d, t, img, x in NEWS)
    body = f'''
<section class="phero wrap">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Novice</span></div>
  <h1 class="h-mega">{lines("Novice in", "dogodki")}</h1>
</section>
<section class="sec wrap" style="padding-top:clamp(56px,6vw,110px)"><div class="news big" data-stagger>{items}</div></section>
{cta_band()}'''
    return page("Novice | Ulbrich Hidroavtomatika", body, "novice")


def partnerji():
    rows = "".join(f'''
    <div class="prow"><div class="lg"><img src="assets/logos/{f}.png" alt="{E(n)}" loading="lazy"></div><p>{E(d)}</p>
      <a class="link" href="{u}" target="_blank" rel="noopener">{E(n)} {ARROW_UR}</a></div>''' for f, n, u, d in PARTNERS)
    body = f'''
<section class="phero wrap">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Partnerji</span></div>
  <div class="phero-grid"><h1 class="h-mega">{lines("Partnerji")}</h1>
  <p class="lead muted">Dolgoletni partnerji, katerih izdelke zastopamo in jih uporabljamo tudi sami, za nemoteno delovanje naših naprav.</p></div>
</section>
<section class="sec wrap" style="padding-top:clamp(56px,6vw,110px)"><div class="plist" data-stagger>{rows}</div></section>
{cta_band()}'''
    return page("Partnerji | Ulbrich Hidroavtomatika", body, "partnerji")


def o_podjetju():
    body = f'''
<section class="phero wrap">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>O podjetju</span></div>
  <h1 class="h-mega">{lines("Več kot 30 let", "hidravlike Ulbrich.")}</h1>
  <div class="cols2" style="margin-top:clamp(48px,6vw,110px)">
    <p class="lead">Podjetje ULBRICH HIDROAVTOMATIKA je bilo ustanovljeno leta 1990 in je član skupine Ulbrich. Aktivno deluje na slovenskem tržišču in trgih nekdanje skupne države, del dejavnosti pa je usmerjen tudi na trge zahodne Evrope ter Severne Amerike.</p>
    <div class="muted"><p>Postali smo zanesljiv partner mnogih podjetij, znani po individualnem pristopu k reševanju problemov, inventivnih rešitvah in spoštovanju dogovorov.</p>
    <p>Ponosni smo na prehojeno pot in dosežene rezultate, a naš pogled je usmerjen v prihodnost. Vabimo vas, da se skupaj spoprimemo z izzivi prihodnosti.</p></div>
  </div>
</section>
<section class="sec wrap">
  <div class="timeline" data-stagger>
    <div class="tl"><span class="y">1949</span><p>Johann Ulbrich ustanovi podjetje Ing. Hans Ulbrich Maschinenbau und Export-Import Handelsg.m.b.H.</p></div>
    <div class="tl"><span class="y">1952</span><p>Distribucijska pogodba z Molykote®. Ulbrich postane prvi evropski distributer specialnih maziv Molykote®.</p></div>
    <div class="tl"><span class="y">1990</span><p>Ustanovitev ULBRICH HIDROAVTOMATIKA d.o.o. Skupina kot eno prvih zahodnih podjetij odpira hčerinska podjetja v srednji in vzhodni Evropi, matično podjetje postane holding.</p></div>
    <div class="tl"><span class="y">2009</span><p>Selitev v novo zgrajen, sodobno opremljen poslovno proizvodni objekt v Radljah ob Dravi.</p></div>
    <div class="tl"><span class="y">Danes</span><p>Lastni razvoj hidravličnih sklopov, sistemov in inteligentnih stiskalnic ter zastopstvo 37 svetovnih proizvajalcev.</p></div>
  </div>
</section>
<section class="sec wrap" style="padding-top:0">
  <div class="split">
    <div class="pic"><img data-par src="{I}menu_55.jpg" alt="Stroj s hidravličnim pogonom"></div>
    <div style="display:flex;flex-direction:column;justify-content:center;gap:28px">
      <h2 class="h-l split-lines">Filozofija podjetja</h2>
      <p class="lead rv">Naš osnovni moto je dolgoročni poslovni uspeh, grajen na partnerskem odnosu z našimi kupci.</p>
      <p class="muted rv">Z znanjem in izkušnjami, predvsem pa s kakovostjo naših aktivnosti, proizvodov in storitev se poskušamo čim bolj približati željam partnerjev. Težko je najti ravnotežje med različnimi pričakovanji, ni pa nemogoče, če odnosi slonijo na zaupanju.</p>
      <h2 class="h-m split-lines" style="margin-top:20px">Proizvodnja in trženje</h2>
      <p class="muted rv">Na področju industrijske hidravlike razvijamo in izdelujemo inovativne hidravlične sklope, sisteme in naprave ter inteligentne stiskalnice. Tržimo hidravlične komponente, orodja, industrijske amortizerje in visokotlačno pnevmatiko ter program tehničnih kemikalij in povezanih sistemov.</p>
    </div>
  </div>
</section>
{cta_band()}'''
    return page("O podjetju | Ulbrich Hidroavtomatika", body, "o-podjetju")


def kontakt():
    opts = "".join(f"<option>{E(c['name'])}</option>" for c in CATS)
    body = f'''
<section class="phero wrap">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Kontakt</span></div>
  <h1 class="h-mega">{lines("Pogovorimo se.")}</h1>
  <div class="kgrid" style="margin-top:clamp(48px,6vw,110px)">
    <dl class="kdata">
      <dt>Sedež podjetja</dt><dd>ULBRICH HIDROAVTOMATIKA d.o.o.<br>Obrtniška ulica 8<br>SI-2360 Radlje ob Dravi</dd>
      <dt>Telefon</dt><dd><a href="tel:+38628879910">+386 2 887 99 10</a></dd>
      <dt>Telefax</dt><dd>+386 2 887 99 19</dd>
      <dt>E-pošta</dt><dd><a href="mailto:info@ulbrich.si">info@ulbrich.si</a></dd>
      <dt>ID za DDV / Matična številka</dt><dd>SI61852295 / 5432731</dd>
      <dt>Bančni računi</dt><dd style="font-size:17px;font-weight:400;line-height:1.6">NLB d.d. Ljubljana, SWIFT LJBASI2X<br>SI56 0247 0001 7184 353<br>OTP d.d. Ljubljana, SWIFT KBMASI2X<br>SI56 0400 0027 8442 903</dd>
    </dl>
    <div class="formbox">
      <form class="form page-form" style="margin-top:0">
        <label>Področje<select name="podrocje"><option>Splošno</option>{opts}</select></label>
        <label>Ime in priimek<input required name="ime" autocomplete="name"></label>
        <label>Podjetje<input name="podjetje" autocomplete="organization"></label>
        <label>E-pošta<input required type="email" name="email" autocomplete="email"></label>
        <label>Sporočilo<textarea name="sporocilo"></textarea></label>
        <button class="btn blue" type="submit">Pošlji sporočilo <span class="arr">{ARROW}</span></button>
      </form>
      <div class="form-ok"><p class="h-m">Hvala. Sporočilo smo prejeli.</p><p class="muted" style="margin-top:14px">Odgovorimo v najkrajšem možnem času.</p></div>
    </div>
  </div>
</section>
<div class="wrap" style="padding-bottom:clamp(96px,11vw,220px)"><div class="mapbox"><iframe loading="lazy" title="Zemljevid" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2740.8004930907423!2d15.229127677256!3d46.61094557111595!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x476fed4f2ef3cce5%3A0x8119b3f10f7d03d0!2sULBRICH%20HIDROAVTOMATIKA!5e0!3m2!1ssl!2ssi!4v1705331135875!5m2!1ssl!2ssi"></iframe></div></div>'''
    return page("Kontakt | Ulbrich Hidroavtomatika", body, "kontakt")


def zaposlitev():
    body = f'''
<section class="phero wrap">
  <div class="crumbs"><a href="index.html">Domov</a><span>/</span><span>Zaposlitev</span></div>
  <h1 class="h-mega">{lines("Pridružite se", "ekipi.")}</h1>
  <p class="lead muted" style="max-width:760px;margin-top:32px">Smo inovativno družinsko podjetje. Če vas zanima delo v stimulativnem okolju in imate potrebna znanja, se veselimo vaše prijave.</p>
</section>
<section class="sec wrap" style="padding-top:clamp(56px,6vw,110px)">
  <div class="plist">
    <div class="prow" style="grid-template-columns:1fr 1.4fr auto"><h3 class="h-m">Inženir za hidravlične sisteme</h3>
      <p>Iščemo dinamičnega in motiviranega posameznika. Pričakujemo sposobnost komuniciranja in samostojnega dela, strokovna in organizacijska znanja, kreativnost in vozniški izpit B kategorije.</p>
      <a class="btn" href="#" data-inquiry="Prijava: Inženir za hidravlične sisteme">Prijava <span class="arr">{ARROW}</span></a></div>
  </div>
</section>
{cta_band()}'''
    return page("Zaposlitev | Ulbrich Hidroavtomatika", body)


# ---------------------------------------------------------------- write
def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)


write("index.html", home())
for i, c in enumerate(CATS):
    write(f'{c["slug"]}.html', category(i, c))
write("novice.html", novice())
write("partnerji.html", partnerji())
write("o-podjetju.html", o_podjetju())
write("kontakt.html", kontakt())
write("prosta-delovna-mesta.html", zaposlitev())
print("built", len(os.listdir(OUT)))
