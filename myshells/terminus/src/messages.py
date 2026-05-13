from typing import *

class Messages:
    table = {
            "male": {
                "^@": "a",
                "^#": "essa",
                "^§": "le",
                "^*": "a",
                "^ç": "lle",
                "^£": "trice",
                "@": "o",
                "#": "e",
                "§": "gli",
                "*": "",
                "ç": "i",
                "£": "tore"
            },
            "famale": {
                "^@": "o",
                "^#": "e",
                "^§": "gli",
                "^*": "",
                "^ç": "i",
                "^£": "tore",
                "@": "a",
                "#": "essa",
                "§": "le",
                "*": "a",
                "ç": "lle",
                "£": "trice"
            }

        }

    def __init__(self, gender: str):
        if gender == 'm':
            self.gender = 'male'
        elif gender == 'f':
            self.gender = 'famale'
        else:
            raise ValueError(f"Gender error: {gender}")

    def __translate(self, message: str) -> str:
        # table = {ord(key): ord(value) for key, value in self.table[self.gender].items()}
        # return message.translate(table)
        for char, translation in self.table[self.gender].items():
            message = message.replace(char, translation)
        return message

    @staticmethod
    def __message(function) -> Callable[[], None]:
        def wrapper(self) -> None:
            msg = function(self)
            print(self.__translate(msg)
                  )
        return wrapper

    @staticmethod

    def __text(function) -> Callable[[], str]:
        def wrapper(self) -> str:
            msg = function(self)
            return self.__translate(msg)
        return wrapper

    @__message
    def welcome_letter(self):
        return """
        Benvenut@! Se è la prima volta che fai questo gioco, ecco alcuni consigli:
        - Osserva ciò che ti circonda utilizzando il comando "ls"
        - Spostati in un nuovo luogo utilizzando il comando "cd NOME_LUOGO"
        - Puoi tornare indietro nel luogo in cui eri prima con il comando "cd .."
        - Interagisci con gli oggetti nel mondo con il comando "less NOME_OGGETTO"
        - Se ti dimentichi in che luogo ti trovi, usa il comando "pwd"
        - Se vuoi fare un po di pulizia usa il comando "clear"
        
        Adesso prosegui. Esplora. Speriamo che ti piaccia quello che troverai. 
        Usa "ls" come primo comando.
        """

    @__message
    def home_message(self):
        return """
        Sei tornat@ a casa.
        """

    @__message
    def western_forest(self):
        return """
        Ti sei spostat@ nella ForestaDell'Ovest. Entri e ti addentri in profondità nella foresta.
        Alla fine, il percorso porta ad una radura con un edificio incredibilmente grande.
        Un'insegna recita: Accademia di Incantesimi: Élite delle Scuole di Magia.
        """

    @__message
    def sign(self):
        return """
        Accademia di Incantesimi: Élite delle Scuole di Magia. Solo per oggi: lezioni introduttive
        gratuite! I novizi sono ben accetti!
        """

    @__message
    def backsign(self):
        return """
        Se mai volessi tornare direttamente a casa puoi usare 'cd ~' o semplicemente 'cd'. 
        Anche se poi tornare dov'eri potrebbe risultare più difficile...
        """

    @__message
    def northern_meadew(self):
        return """
        Ti sei spostat@ nel PratoDelNord. Si tratta di un meraviglioso prato verde. Un pony maestoso e paffuto
        ci saltella sopra felice.
        """

    @__message
    def pony(self):
        return """
        Vai dal poni e cerchi di cavalcarlo. Lui accetta quindi cavalchi il poni in cerchio per un po di tempo.
        Dopo un po' inizia a stancarsi di averti come peso sulla schiena e ti fa scendere. A questo punto si mette
        a guardare verso Est, come se volesse suggerirti di proseguire in quella direzione.
        """

    @__message
    def spell_casting_accademy(self):
        return """
        Ti sei spostat@ all'AccademiaDiIncantesimi. Le sale e i corridoi sono piene degli studenti
        che si affrettano verso le aule. L'interno dell'accademia è impressionante quanto l'esterno, con 
        altissimi soffiti e archi gotici. Sembra addirittura più grande all'interno che all'esterno.
        """

    @__text
    def hurryng_student_name(self):
        return "Student^#Affrettat^@"

    @__message
    def hurryng_student(self):
        return """
        Un^@ student^# di corsa finisce contro di te e cade per terra. Ti chiede immediatamente scusa e se stai
        bene. Tu sei più robust@ di quanto sembri e non ti sei fatt@ niente. "Mi dispiace tanto, ero talmente di fretta
        che non avevo visto che eri li... Senti ma, non ti ho mai visto qui prima d'ora. Sei nuov@ non è vero?".
        L^@ student^# ti fa l'occhiolino, "Non preoccuparti, ci sono centinaia di novizi in giro oggi, perché
        non provi a dare un'occhiata a una delle lezioni introduttive gratuite? Ti farei vedere io dove andare, ma 
        devo correre in classe. Prova ad andare nella stanza Lezioni e sono sicur^@ che qualcuno ti aiuterà. 
        Ci vediamo in giro!". L^@ student^# ti supera di corsa. Hai notato che l^@ student^# è molto carin^@, e probabilmente
        ha la tua età. Sfortunatamente, l^@ student^# è sparit^@ dietro l'angolo, anche prima che potessi cheder^§ il nome.
        """


    @__message
    def lessons(self):
        return """
        Ti sei spostat@ nell'aula Lezioni. Entri nell'aula curios@ è pront@ ad imparare. C'è molto meno 
        trambusto qui, dal momento che la maggior parte delle lezioni è già cominciata. Ti intrufoli velocemente
        alla Lezione Introduttiva, che è già cominciata. Entri nella classe dell'incantesimo "sposta".
        """

    @__message
    def professor(self):
        return """
        Il professore è difficile da capire, ma hai ascoltato abbastanza da aver capito 3 cose:
        1. Puoi usare il comando 'mv' per spostare le cose nel mondo
        2. Devi indicare l'oggetto che vuoi spostare e la nuova posizione (ad esempio "mv OGGETTO NUOVA_POSIZIONE")
        3. Questo incantesimo funziona solo su alcuni oggetti, come ad esempio i Manichini nella StanzaDellaProva
        
        Non hai prestato abbastanza attenzione per imparare quali tipi di oggetti non possono essere spostati. 
        Oh beh, alla fine sperimentare è sempre stato nelle tue corde no? Ma fa attenzione!
        """

    @__message
    def practice_room(self):
        dummy = self.dummy_name()[:-1] + ['e', 'i'][self.gender == 'male']
        return f"""
        Ti sei spostat@ nella StanzaDellaProva. La stanza è piena di {dummy} che gli studenti usano per 
        testare i nuovi incantesimi che hanno appena imparato.
        """

    def dummy_name(self):
        return ["Bambola", "Soldatino"][self.gender == 'male']

    @__message
    def dummy(self):
        return f"""
        È un* {self.dummy_name()} per fare pratica
        """

    @__message
    def instructions(self):
        dummy = self.dummy_name()[:-1] + ['e', 'i'][self.gender == 'male']
        return f"""
        Benvenut@ nella Stanza della Prova. Qui potrai provare i nuovi incantesimi che hai imparato suç 
        {dummy}. Coraggio, fai un tentativo! Se ancora non conosci alcun incantesimo, torna indietro e prova a 
        seguire qualche Lezione.
        """

    @__message
    def box(self):
        return """
        Sei troppo grande per entrare nella scatola
        """

    @__message
    def eastern_mountains(self):
        return """
        Sei arrivat@ alle MontagneDell'Est. Hai viaggiato attraverso il percorso della montagna, il quale, alla fine, 
        conduce all'entrata di una Caverna. All'ingresso della caverna è seduto un uomo anziano.
        """

    @__message
    def old_man(self):
        return """
        Parli con l'uomo anziano. Lui ti saluta calorosamente, come se foste vecchi amici. Ti senti a tuo agio con lui.
        "Ciao avventurier@! Magnifica giornata, non è vero? Sembri un* giovane esplorat£ pien@ di energie!
        Se sei abbastanza coraggios@, il tuo destino ti aspetta all'interno di questa caverna. Il tuo destino si 
        manifesterà come un portale. Entra in questo portale e inizia un nuovo capitolo della tua vita."
        L'uomo vede la paura nei tuoi occhi e ti sorride con sguardo confortante. "Io ormai sono vecchio, e stanco...
        non posso accompagnarti attraverso la caverna, ma c'è una cosa che posso fare! Nel mio AnticoManoscritto c'è un
        incantesimo che può aiutarti lungo il percorso, leggilo pure. Buona fortuna avventurier@!
        """

    @__message
    def old_manuscripts(self):
        return """
        Se mai dovessi dimenticare un incantesimo, usa "help", e davanti a te apparirà una lista di incantesimi 
        disponibili.
        Se hai bisogno sapere a cosa serve uno specifico incantesimo, usa "man" seguito dal comando dell'incantesimo.
        Ad esempio, se fossi interessat@ a sapere come usare l'incantesimo "mv" ti basterebbe scrivere "man mv"
        """

    @__message
    def cave(self):
        return """
        Ti sei spostat@ nella Caverna. È la tipica caverna, buia e umida.
        """

    @__message
    def staircase(self):
        return """
        Ti sei spostat@ sulla ScalaRocciosa. La scala rocciosa porta ad un vicolo cieco indicato da un cartello
        """

    @__message
    def dead_end(self):
        return """
        Vicolo Cieco
        """

    @__message
    def dark_corridor(self):
        return """
        Ti sei spostat@ nel CorridoioOscuro. Cammini attraverso il corridoio oscuro fino a trovare una piccola stanza
        umida alla fine.
        """

    @__message
    def boulder(self):
        return """
        Senti una leggera brezza provenire da dietro il masso.
        """

    @__message
    def small_hole(self):
        return """
        È una fossa, non c'è niente di interessante da fare qui dentro.
        """

    @__message
    def tunnel(self):
        return """
        Ti sei spostat@ nel Tunnel. È piuttosto umido qui dentro. Con la coda dell'occhio scorgi il rapido movimento
        di un piccolo animale peloso, probabilmente un ratto. Un grosso ratto... probabilmente una mangusta.
        Alla fine del tunnel trovi la CameraDellaPietra
        """

    @__message
    def rat(self):
        return """
        Dopo attenta analisi, ti rendi conto che l'animale è effettivamente un ratto... con le dimenzioni di in 
        piccolo cane. Ti morde. Sei molto infastidit@.
        """

    @__message
    def stone_chamber(self):
        return """
        Ti sei spostat@ nella CameraDellaPietra. L'intera stanza è illuminata da un pallido bagliore azzurro. La fonte di 
        questa luce è il portale posizionato al centro della stanza. Chiaramente è il portale di cui ha parlato
        l'uomo anziano all'ingresso della caverna.
        """

    @__message
    def portal(self):
        return """
        Ti sei spostat@ nel Portale. Vieni scagliat@ in un viaggio nello spazio e nel tempo...
        """

    @__message
    def town_square(self):
        return """
        Ti sei spostat@ alla PiazzaCentrale. Ti trovi nella piazza soleggiata e spaziosa di una città. C'è un 
        piedistallo al centro, ma nessuna statua su di esso. L'architettura è affascinante, ma ognuno sembra
        nervoso per qualche ragione.
        """

    @__message
    def random_citizen1(self):
        return """
        "Mi scusi" dici. L'uomo si gira spaventato. "Oh, salve! Benvenut@ nella città di Terminus. Deve scusarmi ma
        siamo tutti un pochino al limite recentemente, o almeno da quando il Mago Nero ha cominciato a diffondere la 
        corruzione lungo la costa. Dovrebbe fare attenzione!"
        """

    @__message
    def random_citizen2(self):
        return """
        L'uomo seduto alza lo sguardo dal giornale e nota che lo stai osservando. "Hai letto?" esclama agitandoti 
        l'ultimo numero della rivista "L'Ultima Parola" davanti alla faccia. "Qui dice che la corruzione del Mago si sta
        diffondendo da Oston fino al sud, e New Console ormai è completamente irrecuperabile! Questi sono tempi 
        pericolosi" borbotta, scuotendo la testa per poi tornare alla sua lettura...
        """

    @__message
    def distraught_lady(self):
        return """
        La donna sta singhiozzando incontrollabilmente, nascondendo il volto tra le mani. 
        "La mia bambina!" grida piangendo, "Hanno rapito la mia bambina! Di sicuro c'è dietro quel maledetto Mago! sigh"
        """

    @__message
    def library(self):
        return """
        Ti sei spostat@ nella Biblioteca. La biblioteca è flebilmente illuminata e odora un po di muffa. Ad ogni modo, 
        la temperatura è piacevole e un soffice tappeto rosso le da un'aria accogliente.
        """

    @__message
    def totally_rad_spellbock(self):
        return """
        La leggenda narra di una grande parola di potere che permette a chi la pronuncia di poter eseguire qualsiasi
        azione su qualunque oggetto. "sudo", come veniva chiamata dagli anziani, conferisce la completa padronanza 
        degli elementi. Purtroppo, o forse per fortuna, la mistica password è stata perduta nelle sabbie del tempo...
        """

    @__message
    def paperbackRomance(self):
        return """
        Prendi il libricino e lo apri ad una pagina a caso. "... piove su i pini scagliosi ed irti, 
        piove su i mirti divini, su le ginestre fulgenti di fiori accolti, su i ginepri folti di coccole aulenti--"
        Chiudi il libro, disinteressat@, e lo rimetti al suo posto sullo scaffale. 
        """

    @__message
    def history_of_terminus(self):
        return """
        Sembra un libro interessante, ma un po' troppo lungo e scritto un po troppo piccolo. Però c'è un estratto:
        '...leggende metropolitane dicono che il MagoNero frammenterà la terra...
        ...solo il creatore-dei-mondi può impedire al virus del MagoNero di...
        ...il potere del "sudo" può essere l'unica debolezza del MagoNero...'
        """

    @__message
    def inconspicuous_lever(self):
        return """
        Trovi una leva seminascosta dietro agli scaffali. Curios@, la tiri e un pannello scorre rivelando una stanza 
        segreta.
        """

    @__message
    def backroom(self):
        return """
        Ti sei spostat@ nella StanzaSegreta. Trovi una misteriosa stanza segreta. Trovi un bibliotecario con un 
        piccolo elfo. Speri di non disturbare.
        """

    @__message
    def grep(self):
        return """
        L'elfo singolarmente brutto si gira verso di te con un'espressione acida. "Greeeeeeeep", dice imbronciato.
        """

    @__message
    def librarian_before_quest(self):
        return """
        Mh? Oh, ciao. Perdonami per il casino, ma sono molto occupato a fare ricerche sul mago nero. 
        Mi faresti un favore? Vai a cercare tutti i rifermenti al mago nero nella Storia di Terminus.
        Il mio assistente Grep può aiutarti." Grep ti guarda malinconico "Greeeeeep".
        
        "Per cercare una parola o una frase in un libro, scrivi semplicemente "grep PAROLA LIBRO", dove PAROLA è la 
        parola o la frase che vuoi cercare nel libro scritta tra virgolette, e LIBRO è il libro in cui cercare.
        
        Prova con il LibroDegliEsercizi qui, vedi se riesci a trovare le righe che contengono una parola che finisce 
        per 'embre' al suo interno."
        """

    @__message
    def practice_book(self):
        return """"
        Trenta dì
        conta novembre,
        con april,
        giugno e settembre.
        Di ventotto
        ce n'è uno,
        tutti gli altri
        ne han trentuno.
        """

    @__message
    def librarian_after_quest(self):
        return """
        "Grazie, sei stat@ di grande aiuto! Ecco, tieni questi per il disturbo. È il minimo che posso fare". 
        Il bibliotecario ti da 5 monete d'oro.
        """

    













if __name__ == '__main__':
    msg = Messages('f').welcome_letter()
    print(msg)